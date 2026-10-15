import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

// Opt-in workspace guard. Only computer_use captures; not a general sandbox.
export function createGuard(root, now = Date.now) {
  const marker = path.join(root, '.scirender-visual-review.json');
  function load() {
    if (!fs.existsSync(marker)) return null;
    const c = JSON.parse(fs.readFileSync(marker, 'utf8'));
    if (typeof c.run_id !== 'string' || !c.run_id.trim()) throw Error('Visual review needs nonempty run_id');
    const key = createHash('sha256').update(c.run_id).digest('hex');
    const dir = path.join(root, '.scirender-review-state'); fs.mkdirSync(dir,{recursive:true});
    const file = path.join(dir,key+'.json');
    const s = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file,'utf8')) :
      {run_id:c.run_id,started_ms:now(),status:'INCOMPLETE',targets:{},digests:{},events:[],total:0};
    return {file,s};
  }
  function save(x) { const tmp=x.file+'.tmp'; fs.writeFileSync(tmp,JSON.stringify(x.s,null,2)+'\n'); fs.renameSync(tmp,x.file); }
  function stop(x,reason) {x.s.status='NEEDS_EXTERNAL_REVIEW';x.s.reason=reason;save(x);return reason;}
  function expired(x) {return now()-x.s.started_ms >=180000;}
  return {
    call(p) {
      if(p.name!=='computer_use'||p.args?.action!=='capture')return {allow:true};
      const x=load();if(!x)return {allow:true};
      if(x.s.status==='NEEDS_EXTERNAL_REVIEW')return {allow:false,reason:x.s.reason};
      const target=JSON.stringify([p.args.pid??null,p.args.window_id??null,p.args.target??null]);
      if(expired(x)||x.s.total>=12||(x.s.targets[target]??0)>=3) {
        const reason=stop(x,'Visual review budget exhausted: at most 3 captures per target, 12 total, 180 seconds. Preserve checkpoint; pixels remain UNVERIFIED.');
        return {allow:false,reason};
      }
      x.s.total++;x.s.targets[target]=(x.s.targets[target]??0)+1;
      x.s.events.push({at_ms:now(),toolUseId:p.toolUseId,target,attempt:x.s.targets[target]});save(x);
      return {allow:true};
    },
    result(p) {
      if(p.name!=='computer_use'||p.args?.action!=='capture')return {};
      const x=load();if(!x)return {};
      const d=p.result?.structured?.image?.digest;
      if(d){x.s.digests[d]=(x.s.digests[d]??0)+1;save(x);
        if(x.s.digests[d]>=3)stop(x,'Identical image received 3 times without completing review. Stop capture loop; pixels remain UNVERIFIED.');}
      return {};
    },
    step() {
      const x=load();if(!x)return {};
      if(expired(x)&&x.s.status!=='NEEDS_EXTERNAL_REVIEW')stop(x,'Visual review exceeded 180 seconds; resume from saved checkpoint with a new explicitly recorded review run.');
      if(x.s.status==='NEEDS_EXTERNAL_REVIEW')return {block:true,reason:x.s.reason};
      return {};
    }
  };
}
export const visualGuard={inject:['extension'],apply(ctx){
  const agnes=ctx.extension();
  const guard=h=>createGuard(h.session.workspaceRoot);
  agnes.registerHook('tool_call',(p,h)=>guard(h).call(p));
  agnes.registerHook('tool_result',(p,h)=>guard(h).result(p));
  agnes.registerHook('before_step',(_,h)=>guard(h).step());
}};
