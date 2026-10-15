import assert from 'node:assert/strict';
import fs from 'node:fs';import os from 'node:os';import path from 'node:path';
import {createGuard,visualGuard} from './index.mjs';
const root=fs.mkdtempSync(path.join(os.tmpdir(),'scirender-guard-'));let time=0;
const marker=path.join(root,'.scirender-visual-review.json');
const arm=id=>fs.writeFileSync(marker,JSON.stringify({run_id:id}));
const call=(id,w)=>({name:'computer_use',toolUseId:id,args:{action:'capture',pid:1,window_id:w}});
try{
 let g=createGuard(root,()=>time);assert.equal(g.call(call('unarmed',1)).allow,true);
 arm('limit');for(let i=0;i<3;i++)assert.equal(g.call(call('a'+i,1)).allow,true);
 assert.equal(g.call(call('a4',1)).allow,false);assert.equal(g.step().block,true);
 g=createGuard(root,()=>time);assert.equal(g.call(call('restart',1)).allow,false);
 assert.equal(g.call({name:'read',args:{}}).allow,true);
 arm('digest');for(let i=0;i<3;i++){g.call(call('d'+i,i));g.result({...call('d'+i,i),result:{structured:{image:{digest:'same'}}}});}
 assert.equal(g.step().block,true);
 arm('total');for(let i=0;i<12;i++)assert.equal(g.call(call('t'+i,i)).allow,true);
 assert.equal(g.call(call('overflow',99)).allow,false);
 arm('timeout');g.call(call('t',1));time=180001;assert.equal(g.step().block,true);
 arm('new-run');assert.equal(g.call(call('new',1)).allow,true);
 fs.writeFileSync(marker,'broken');assert.throws(()=>g.call(call('bad',1)));
 const hooks={};visualGuard.apply({extension:()=>({registerHook:(name,fn)=>hooks[name]=fn})});
 assert.deepEqual(Object.keys(hooks),['tool_call','tool_result','before_step']);
 fs.unlinkSync(marker);assert.deepEqual(hooks.before_step({}, {session:{workspaceRoot:root}}),{});assert.deepEqual(hooks.tool_result({name:'read'}, {session:{workspaceRoot:root}}),{});
 console.log('PASS: unarmed, per-target limit, persistent restart, unrelated tool, digest dedup, total limit, timeout, explicit new run, corrupt state, hook registration');
}finally{fs.rmSync(root,{recursive:true,force:true});}
