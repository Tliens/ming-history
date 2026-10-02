#!/usr/bin/env python3
"""
R8 图像素材抓取：Wikimedia Commons（台北故宫藏明代图像为主，公有领域）
产物：assets/images/*.jpg + assets/images/manifest.json（逐图版权元数据）

用法： python3 scripts/images/fetch_commons.py
原则：只收 PD / CC；每图记录 Artist/License/来源页；400px 内缩图不入库（统一 800px）
"""
import json, os, time, urllib.request, urllib.parse, sys

UA = {"User-Agent": "MingHistorySite/0.1 (educational; contact via repo)"}
API = "https://commons.wikimedia.org/w/api.php"
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "images")
os.makedirs(OUT, exist_ok=True)

def api(params, retries=3):
    params.update({"format": "json"})
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < retries - 1:
                time.sleep(8 * (i + 1)); continue
            raise

def search(q, limit=8):
    d = api({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": limit})
    return [x["title"] for x in d.get("query", {}).get("search", [])]

def get_meta(titles):
    """批量 imageinfo：url、800px 缩图、extmetadata"""
    out = {}
    for i in range(0, len(titles), 20):
        chunk = titles[i:i+20]
        d = api({"action": "query", "titles": "|".join(chunk), "prop": "imageinfo",
                 "iiprop": "url|extmetadata|size", "iiurlwidth": "800"})
        for p in d.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            def g(k): return (em.get(k, {}) or {}).get("value", "")
            out[p.get("title")] = {
                "url800": ii.get("thumburl") or ii.get("url"),
                "orig": ii.get("url"),
                "size": ii.get("size"),
                "artist": g("Artist"),
                "license": g("LicenseShortName"),
                "credit": g("Credit"),
                "descurl": ii.get("descriptionurl"),
            }
        time.sleep(2)
    return out

def dl(url, path):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
        f.write(r.read())
    return os.path.getsize(path)

# ---------- 1. 已确认的精选清单 ----------
PICKS = {
    "emperor-hongwu":   "File:明太祖坐像（一） 軸.jpg",
    "emperor-yongle":   "File:Anonymous-Ming Chengzu.jpg",
    "emperor-hongxi":   "File:明仁宗坐像 軸.jpg",
    "emperor-xuande":   "File:明宣宗坐像（一） 軸.jpg",
    "emperor-yingzong": "File:明英宗坐像 軸.jpg",
    "emperor-hongzhi":  "File:Hongzhi1.jpg",
    "emperor-zhengde":  "File:Ming Wuzong.jpg",
    "emperor-jiajing":  "File:明世宗坐像.tif",
    "emperor-longqing": "File:明穆宗画像.jpg",
    "emperor-wanli":    "File:MingShenzong1.jpg",
    "emperor-taichang": "File:明光宗皇帝.jpg",
    "consort-xiaohe":   "File:明代帝后半身像（二） 冊 孝和皇后；孝純皇后.jpg",
}

# ---------- 2. 待搜索的缺项（限速串行） ----------
SEARCH_MAP = {
    "emperor-chenghua": ["明宪宗坐像", "Ming Xianzong portrait"],
    "emperor-jingtai":   ["明代宗 画像", "景泰帝 像"],
    "emperor-chongzhen": ["明思宗 坐像", "崇祯皇帝 像"],
    "emperor-tianqi":    ["明熹宗 像"],
    "scene-gugong-map":  ["北京宫城图", "Beijing palace city painting Ming"],
    "scene-chujing-rubi": ["出警入跸图"],
    "scene-taihedian":   ["Hall of Supreme Harmony front view"],
    "scene-xiaoling":    ["明孝陵 神道"],
    "scene-changling":   ["明长陵 祾恩殿"],
    "scene-wokou":       ["倭寇図巻", "抗倭图卷"],
}
for img_id, queries in SEARCH_MAP.items():
    found = None
    for q in queries:
        try:
            hits = search(q)
        except Exception as e:
            print(f"  search {q} 失败: {e}"); time.sleep(6); continue
        # 过滤 djvu/pdf/矢量等非图像
        hits = [h for h in hits if h.lower().endswith((".jpg", ".jpeg", ".png", ".tif"))]
        if hits:
            found = hits[0]; print(f"{img_id}: {found}"); break
        time.sleep(3)
    if found:
        PICKS[img_id] = found
    else:
        print(f"{img_id}: 未找到（记录为缺项，走自绘/二期）")
    time.sleep(3)

# ---------- 3. 批量元数据 ----------
metas = get_meta(list(PICKS.values()))

# ---------- 4. 下载 + manifest ----------
manifest = []
for img_id, title in PICKS.items():
    m = metas.get(title)
    if not m or not m.get("url800"):
        print(f"  [skip] {img_id} {title} 无元数据"); continue
    ext = ".jpg"
    path = os.path.join(OUT, img_id + ext)
    try:
        size = dl(m["url800"], path)
        manifest.append({
            "id": img_id, "file": img_id + ext, "commonsTitle": title,
            "artist": m["artist"][:200], "license": m["license"],
            "credit": m["credit"][:200], "source": m["descurl"],
            "downloadedKB": size // 1024,
        })
        print(f"  [ok] {img_id}  {size//1024}KB  {m['license']}")
    except Exception as e:
        print(f"  [fail] {img_id}: {e}")

with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump({"meta": {"fetched": time.strftime("%Y-%m-%d"), "policy": "仅收录 PD/CC 内容；来源与许可逐图记录"},
               "images": manifest}, f, ensure_ascii=False, indent=2)
print(f"\n共入库 {len(manifest)} 图 → manifest.json")
