#!/usr/bin/env python3
"""全站校对轮：数据交叉一致性 + dist 内链爬取 + 图像存在性。只报告，不自动改数据。"""
import json, re, os, sys, glob

ROOT = os.path.join(os.path.dirname(__file__), "..")
os.chdir(ROOT)
issues, warns = [], []

def J(p): return json.load(open(p, encoding="utf-8"))

def _norm_name(n):
    import re as _r
    return _r.sub(r"（[^）]*）", "", n).strip()

emps = J("src/data/emperors/emperors.json")
events = J("src/data/events/events.json")["events"]
secs = J("src/data/first-secretaries.json")["secretaries"]
figs = J("src/data/figures/figures.json")["figures"]
rels = J("src/data/figures/figure-relations.json")
cons = J("src/data/consorts/consorts.json")
gloss = J("src/data/glossary.json")["terms"]
man = J("assets/images/manifest.json")

# A. 帝王字段一致性
emp_ids = {e["id"] for e in emps["emperors"]}
for e in emps["emperors"]:
    if e["birth"] and e["death"] and e["death"] <= e["birth"]: issues.append(f"A 帝王 {e['id']} 死年≤生年")
    if e["birth"] and e["death"] and e.get("lifespan") and e["lifespan"] not in (e["death"]-e["birth"], e["death"]-e["birth"]+1):
        warns.append(f"A 帝王 {e['id']} 享年 {e['lifespan']} 与生卒差({e['death']-e['birth']})不一致")
    for k in ("eraStart","eraEnd"):
        if e.get(k) and not (e["reignStart"]-1 <= e[k] <= e["reignEnd"]+1):
            issues.append(f"A 帝王 {e['id']} 年号{k}={e[k]} 超出在位区间")
    if e.get("eras"):
        for x in e["eras"]:
            if not (e["reignStart"] <= x["eraStart"] and x["eraEnd"] <= e["reignEnd"]):
                issues.append(f"A 帝王 {e['id']} 段年号 {x} 超出在位")

# B. 事件引用完整性 + 年代合法性
import re as _re
def _norm(n): return _re.sub(r"（[^）]*）", "", n).strip()
fig_names = {_norm(f["name"]) for f in figs}
emp_names = {e["name"]: e["id"] for e in emps["emperors"]}
south_names = {r["name"] for r in emps["southernMing"]["rulers"]}
reign = {}
for e in emps["emperors"]:
    reign.setdefault((e["reignStart"], e["reignEnd"]), []).append(e["id"])
ev_ids = {e["id"] for e in events}
for ev in events:
    y = ev["year"]
    if not any(a <= y <= b for a, b in reign):
        if y > 1644 and y <= 1662: pass
        else: issues.append(f"B 事件 {ev['id']} 年 {y} 不在任何帝王在位区间")
    for n in ev.get("figures", []):
        if _norm(n) not in fig_names and _norm(n) not in emp_names and _norm(n) not in south_names and _norm(n) not in cons:
            warns.append(f"B 事件 {ev['id']} 人物「{n}」未建档（显示为纯文本）")
    c = ev.get("location", {}).get("coord")
    if c and not (15 <= c[1] <= 55 and 73 <= c[0] <= 145):
        issues.append(f"B 事件 {ev['id']} 坐标越界 {c}")

# C. 首辅任期合法性
for s in secs:
    for t in s["terms"]:
        if t["end"] is not None and t["start"] > t["end"]:
            issues.append(f"C 首辅 {s['id']} 任期起讫倒置 {t}")
        if s.get("jinshi") and t["start"] < s["jinshi"]:
            issues.append(f"C 首辅 {s['id']} 任期早于中进士年")

# D. 人物
stages = {"B1","B2","B3","B4","B5","B6","B7","B8","B9"}
for f in figs:
    if f.get("stage") not in stages: issues.append(f"D 人物 {f['id']} stage 非法: {f.get('stage')}")
    if f.get("birth") and f.get("death") and f["death"] < f["birth"]: issues.append(f"D 人物 {f['id']} 死年<生年")
    if f.get("birth") and f.get("death") and (f["death"]-f["birth"]) > 105: warns.append(f"D 人物 {f['id']} 寿命 >105 岁，请复核")

# E. 关系边
known = {f["id"] for f in figs} | emp_ids | {c["id"] for c in cons["consorts"]}
ph_map_src = open("src/data/figure-names.js", encoding="utf-8").read()
ph_map = set(re.findall(r'"([a-z][a-z0-9-]*)":', ph_map_src))
for a, ty, b in rels["edges"]:
    for n in (a, b):
        if n not in known and n not in ph_map:
            issues.append(f"E 关系边节点 {n} 无映射（figure-names.js 缺条目）")
    if ty not in rels["meta"]["edgeTypes"]:
        issues.append(f"E 关系边类型非法: {ty}")

# F. 图像存在性
for img in man["images"]:
    p = f"public/images/{img['file']}"
    if not os.path.exists(p): issues.append(f"F 图像缺失 {p}")
for src in {i["file"] for i in man["images"]}:
    if not os.path.exists(f"assets/images/{src}"): warns.append(f"F 源图缺失 assets/images/{src}")

# G. 术语
ids = [t["id"] for t in gloss]
if len(ids) != len(set(ids)): issues.append("G 术语 id 重复")
idset = set(ids)
for t in gloss:
    for r in t.get("related", []):
        if r not in idset: issues.append(f"G 术语 {t['id']} related 悬空 → {r}")

# H. 专题/学习线/教材引用的事件 id
sys_path = "src/data/topics.js"
st = open(sys_path, encoding="utf-8").read()
for mid in re.findall(r'events:\s*\[([^\]]*)\]', st):
    for x in re.findall(r'"([a-z0-9-]+)"', mid):
        if x not in ev_ids: issues.append(f"H topics.js 引用不存在的事件 {x}")
for fn, key in [("src/data/stages.js", "stages"), ("src/data/learn.js", "learn"), ("src/pages/learn/textbook.astro", "textbook")]:
    txt = open(fn, encoding="utf-8").read()
    for x in re.findall(r'/events/([a-z0-9-]+)', txt):
        if x not in ev_ids: issues.append(f"H {fn} 引用不存在的事件 {x}")

# I. dist 内链爬取
bad_links = {}
html_files = glob.glob("dist/**/*.html", recursive=True)
seen = set()
for hf in html_files:
    html = open(hf, encoding="utf-8", errors="ignore").read()
    for href_raw in re.findall(r'href="(/[^"#]*?)(?:#[^"]*)?"', html):
        href = href_raw.split("?")[0] or "/" 
        if href.startswith("/images/") or href.startswith("/geojson/") or href.startswith("/vendor/") or href.startswith("/styles/") or href.startswith("/_astro/"): continue
        if href in seen: continue
        seen.add(href)
        target = "dist" + href
        if not href.endswith("/") and "." not in os.path.basename(href): target += "/"
        if href == "/": target = "dist/index.html"
        if not os.path.exists(target):
            bad_links.setdefault(href, []).append(os.path.relpath(hf, "dist"))
for href, srcs in sorted(bad_links.items()):
    issues.append(f"I 死链 {href} ← {', '.join(srcs[:3])}{'…' if len(srcs)>3 else ''}")

print(f"=== 校对轮报告 ===\n问题 {len(issues)} 条 / 提示 {len(warns)} 条")
for i in issues: print("✗", i)
for w in warns[:25]: print("△", w)
if len(warns) > 25: print(f"△ …另有 {len(warns)-25} 条提示")
