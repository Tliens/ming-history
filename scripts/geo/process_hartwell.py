#!/usr/bin/env python3
"""
R10 收尾：Hartwell 1391 切片 → 明初府级/省级 GeoJSON（V7 燃料）

来源：Hartwell China HGIS, CHGIS V5 (2010), DOI: 10.7910/DVN/29302
许可：CC BY-NC-SA 3.0（详见 src/geojson/ATTRIBUTION.md）
原始层：v5_1391_chin_chn_1391_p（305 个府级面，BIG5，西安80/GK19 带）

处理：
1. 反投影 Xian1980 GK z19 → WGS84（无严密基准转换参数，整体误差约百余米，全国尺度显示无碍）
2. 府级层：shapely simplify(0.008°) 保留主体形状
3. 省级层：按 H_CHINPROV 分组 unary_union → simplify(0.003°)
4. 繁体原名保留（name_cht），另出简体（name_ch，opencc 转写）

用法： python3 scripts/geo/process_hartwell.py
依赖： pip3 install --user pyshp pyproj shapely opencc-python-reimplemented
"""
import json, os, sys
import shapefile, pyproj
from shapely.geometry import shape as shp_shape, mapping
from shapely.ops import transform as shp_transform, unary_union
from opencc import OpenCC

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
SHP = f"{BASE}/src/geojson/raw/v5_Hartwell/v5_1391_chin_chn_1391_p"
OUT = f"{BASE}/src/geojson"
T2S = OpenCC("t2s").convert
# BIG5 解码伪字修正（如「ㄦ」为「儿」之误读）
FIX = {"ㄦ": "兒", "陜": "陝"}  # BIG5 伪字通配修正（ㄦ→兒；陜→陝）
# 无省级归属的单位（关西七卫、西域政权、小琉球等）统一归组标签
FALLBACK_GROUP = "關西諸衛·外邦"

def fix(s):
    for k, v in FIX.items():
        s = s.replace(k, v)
    return s

# ---- 投影 ----
crs_src = pyproj.CRS.from_wkt(open(SHP + ".prj").read())
T = pyproj.Transformer.from_crs(crs_src, pyproj.CRS("EPSG:4326"), always_xy=True)

def to_wgs84(geom):
    return shp_transform(lambda x, y, z=None: T.transform(x, y), geom)

def rnd(geom_mapping, nd=3):
    """仅对 coordinates 递归取整，保留 GeoJSON 结构"""
    def rr(c):
        if isinstance(c, (list, tuple)) and len(c) >= 2 and isinstance(c[0], (int, float)) and isinstance(c[1], (int, float)):
            return [round(c[0], nd), round(c[1], nd)]
        if isinstance(c, (list, tuple)):
            return [rr(i) for i in c]
        return c
    m = dict(geom_mapping)
    m["coordinates"] = rr(m["coordinates"])
    return m

r = shapefile.Reader(SHP, encoding="big5")

# ---- 1. 府级层 ----
prefs = []
for sr, rec in zip(r.iterShapes(), r.iterRecords()):
    d = rec.as_dict()
    if sr.shapeType == shapefile.NULL:
        continue
    geom = shp_shape(sr.__geo_interface__).simplify(0.008, preserve_topology=True)
    geom = to_wgs84(geom).buffer(0)  # buffer(0) 修自相交
    prov = d.get("H_CHINPROV") or d.get("H_CHINCIR") or FALLBACK_GROUP
    name_cht = fix(d.get("H_UNICODE_") or d.get("H_CHIN_DPR") or d.get("H_CHIN_PRF") or "?")
    prefs.append({
        "type": "Feature",
        "geometry": rnd(mapping(geom)),
        "properties": {
            "code": d.get("CODE"),
            "name_ch": T2S(name_cht),
            "name_cht": name_cht,
            "name_py": d.get("H_PINYIN_N"),
            "admin_type": d.get("H_ADMIN_TY"),
            "province_cht": fix(prov),
            "province_ch": T2S(fix(prov)),
            "year": 1391,
        },
    })

fc = {"type": "FeatureCollection", "name": "ming_prefectures_1391", "features": prefs}
with open(f"{OUT}/ming_prefectures_1391.json", "w", encoding="utf-8") as f:
    json.dump(fc, f, ensure_ascii=False, separators=(",", ":"))
print(f"ming_prefectures_1391.json  {os.path.getsize(f'{OUT}/ming_prefectures_1391.json')//1024}KB  {len(prefs)} features")

# ---- 2. 省级层（布政司/都司区划聚合）----
groups = {}
for sr, rec in zip(r.iterShapes(), r.iterRecords()):
    d = rec.as_dict()
    if sr.shapeType == shapefile.NULL:
        continue
    prov = d.get("H_CHINPROV") or d.get("H_CHINCIR") or FALLBACK_GROUP
    groups.setdefault(prov, []).append(shp_shape(sr.__geo_interface__))

feats = []
for prov, geoms in groups.items():
    try:
        g = to_wgs84(unary_union(geoms)).simplify(0.012, preserve_topology=True).buffer(0)
        feats.append({
            "type": "Feature",
            "geometry": rnd(mapping(g), nd=2),  # 省级层首屏加载：2位小数（~1km）够用
            "properties": {"name_ch": T2S(fix(prov)), "name_cht": fix(prov), "units": len(geoms), "year": 1391},
        })
    except Exception as e:
        print(f"  [warn] {prov} 合并失败: {e}", file=sys.stderr)

fc2 = {"type": "FeatureCollection", "name": "ming_provinces_1391", "features": feats}
with open(f"{OUT}/ming_provinces_1391.json", "w", encoding="utf-8") as f:
    json.dump(fc2, f, ensure_ascii=False, separators=(",", ":"))
print(f"ming_provinces_1391.json  {os.path.getsize(f'{OUT}/ming_provinces_1391.json')//1024}KB  {len(feats)} features")
for ft in sorted(feats, key=lambda x: -x["properties"]["units"]):
    p = ft["properties"]
    print(f"  {p['name_ch']}（{p['name_cht']}）{p['units']} 单位")
