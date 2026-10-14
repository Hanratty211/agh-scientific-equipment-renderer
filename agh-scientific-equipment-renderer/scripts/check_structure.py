#!/usr/bin/env python3
"""
check_structure.py — v1.1 独立发布包结构、链接、安全清单及合成反例核查
===============================================================
检查项（不只是字符串黑名单）：
  1. 必需通用文件与 SKILL.md frontmatter 存在且有效
  2. 包内所有 Markdown 引用不越界；发布清单无论文/媒体/缓存/逐篇证据
  3. legacy 默认值检查仅用于防旧代码对象名混入
  4. 抽象教学反例与真实 Blender 合成 T1–T4 行为检查
     —— 不能只靠字符串黑名单宣称通用性通过，行为验证为强校验。
退出码：全通过 0；任一失败 1。
"""
import os, re, sys, subprocess, yaml
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # skill 根
BLENDER = os.environ.get('AGH_BLENDER','/Applications/Blender.app/Contents/MacOS/Blender')

# Legacy regression: historical names must not become general modeling defaults.
CASE1_NAMES = [
    "cool_bm_1", "cool_bm_2", "mot_opt_win_n", "mot_opt_win_p",
    "lat_fiber_flange", "vac_shell", "sapph_window", "dichroic_mir",
    "mot_coil_L", "cam_mot_entrance", "cam_rw_interface",
]
HARDCODED_COORDS = [
    "RT_WALL_OUT_X", "MOT_CONV_X", "AXIS_Z = 0.020", "CAV_X  = -0.080",
    "CHAM_W, CHAM_D, CHAM_H = 0.200", "-0.156",
]

def check_generic(path):
    bad = []
    txt = open(path, encoding='utf-8').read()
    for n in CASE1_NAMES:
        if n in txt:
            bad.append(f"case-1 对象名 {n}")
    for c in HARDCODED_COORDS:
        if c in txt:
            bad.append(f"硬编码坐标/常量 {c}")
    return bad

def parse_frontmatter(md_path):
    """解析 SKILL.md 的 YAML frontmatter（--- 包裹）。返回 dict 或 None。"""
    txt = open(md_path, encoding='utf-8').read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.DOTALL)
    if not m:
        return None
    return yaml.safe_load(m.group(1))

def referenced_files(skill_txt):
    """Paths in inline code OR local Markdown links (not remote URLs)."""
    refs = re.findall(r"`((?:references|scripts)/[A-Za-z0-9_./-]+)`", skill_txt)
    link_start = chr(93) + chr(40)
    for chunk in skill_txt.split(link_start)[1:]:
        target = chunk.split(chr(41), 1)[0]
        if target.startswith(('references/', 'scripts/')) or target == 'PROVENANCE.md':
            refs.append(target)
    return sorted(set(refs))

def main():
    failures = []
    print("=== 结构检查 ===")
    required = ["SKILL.md", "README.md", "PROVENANCE.md", "CHANGELOG.md",
                "references/identity_port_gate_v11.md", "references/source_render_and_demo_v11.md",
                "references/physical_equipment_and_interfaces.md", "references/workflow_checklist.md",
                "references/domain_checks.md", "references/project_record.md",
                "scripts/blender_core.py", "scripts/test_v11_workflow.py", "scripts/check_release_package.py", "behavior_tests.py"]
    for f in required:
        p = os.path.join(ROOT, f)
        ok = os.path.exists(p)
        print(f"  [{'OK' if ok else '缺失'}] {f}")
        if not ok:
            failures.append(f"缺少文件 {f}")

    # frontmatter 元数据
    print("\n=== SKILL.md frontmatter ===")
    fm = parse_frontmatter(os.path.join(ROOT, "SKILL.md"))
    if fm is None:
        print("  [缺失] 无有效 YAML frontmatter")
        failures.append("SKILL.md 无 YAML frontmatter")
    else:
        for field in ("name", "description"):
            v = fm.get(field, "")
            ok = isinstance(v, str) and len(v.strip()) > 0
            print(f"  [{'OK' if ok else '无效'}] {field}: {(v[:60] + '…') if len(v) > 60 else v}")
            if not ok:
                failures.append(f"frontmatter {field} 无效")
        print(f"  其他 frontmatter 键: {sorted(k for k in fm if k not in ('name','description')) or '无'}")

    # 检查反引号路径与实际 Markdown 链接；v0.2 只检查前者。
    print("\n=== 引用文件存在性 ===")
    skill_txt = open(os.path.join(ROOT, "SKILL.md"), encoding='utf-8').read()
    uniq = referenced_files(skill_txt)
    for r in uniq:
        p = os.path.join(ROOT, r)
        ok = os.path.exists(p)
        print(f"  [{'OK' if ok else '缺失'}] {r}")
        if not ok:
            failures.append(f"引用文件缺失 {r}")
    if not uniq:
        print("  （SKILL.md 未引用 references/scripts 路径）")

    # Independently check every Markdown link and the entire release package.
    from check_release_package import inspect_release
    for issue in inspect_release(Path(ROOT)):
        failures.append(issue)
    # v1.1: abstract route/port/image negative examples (not Blender hardware validation).
    v11 = os.path.join(ROOT, 'scripts/test_v11_workflow.py')
    if not os.path.isfile(v11):
        failures.append('v1.1 门槛反例脚本缺失')
    else:
        proc11 = subprocess.run([sys.executable, v11], capture_output=True, text=True, timeout=30)
        print('\n=== v1.1 文档门槛与正反例 ===')
        print(proc11.stdout.strip())
        if proc11.returncode:
            failures.append('v1.1 门槛反例未通过：'+proc11.stderr[-300:])

    # Historical regression only: abstract package has no article-specific defaults.
    print("\n=== 历史默认值反例（不得混入通用默认）===")
    for g in ("SKILL.md", "scripts/blender_core.py"):
        bad = check_generic(os.path.join(ROOT, g))
        print(f"  {g}: {'无混入' if not bad else '混入 -> ' + '; '.join(bad)}")
        failures += [f"{g} 混入 {b}" for b in bad]

    # 反例行为验证（强校验，不靠字符串黑名单）
    print("\n=== 反例行为验证（真实 Blender 运行 behavior_tests.py）===")
    bt = os.path.join(ROOT, "behavior_tests.py")
    if not os.path.exists(bt):
        failures.append("behavior_tests.py 缺失，无法做行为验证")
        print(f"  [缺失] behavior_tests.py")
    else:
        try:
            env=os.environ.copy();env['PYTHONPYCACHEPREFIX']=env.get('PYTHONPYCACHEPREFIX','/tmp/agh-equipment-pycache')
            proc = subprocess.run([BLENDER, "-b", "--factory-startup", "--python", bt],
                                  capture_output=True, text=True, timeout=180, env=env)
            # 抓汇总行
            tail = [l for l in (proc.stdout + proc.stderr).splitlines()
                    if ("PASS" in l or "FAIL" in l or "行为验证汇总" in l or "总体" in l)]
            for l in tail[-8:]:
                print("  | " + l)
            # 行为结果文件也保留
            print('  行为结果写系统临时目录或 AGH_BEHAVIOR_REPORT 指定的包外路径')
            overall = "总体: 全部 PASS" in (proc.stdout + proc.stderr)
            if proc.returncode != 0 or not overall:
                failures.append(f"行为验证未全通过（exit={proc.returncode}；见 behavior_results.txt）")
            print(f"  行为验证: {'全 PASS' if overall else '存在 FAIL'}")
        except Exception as e:
            failures.append(f"行为验证运行失败: {e}")
            print(f"  [失败] 行为验证运行: {e}")

    print("\n=== 结论 ===")
    if failures:
        for f in failures:
            print(f"  [FAIL] {f}")
        print(f"共 {len(failures)} 项未通过（退出码 1）")
        return 1
    print("全部通过（独立包结构/全部本地链接/无媒体证据 + frontmatter + 抽象反例 + Blender 合成行为）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
