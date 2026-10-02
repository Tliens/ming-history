#!/usr/bin/env python3
"""
R10 地图数据管线：SHP → GeoJSON（MapCore 数据底座）
原始数据放 src/geojson/raw/（不入库），产物写 src/geojson/（入库）。

数据来源与许可（详见 src/geojson/ATTRIBUTION.md）：
- Ming Garrisons (1368-1644)  DOI:10.7910/DVN/5RUXK8  学术使用/GPL，据 Liew Foon Ming 译注《明史·兵志》
- Ming Courier Routes & Stations (2016)  DOI:10.7910/DVN/SB8ZTM  学术使用，据杨正泰《明代驿站考》

用法： python3 scripts/geo/process_geo.py
"""
import json, csv, os, sys

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
RAW = f"{BASE}/src/geojson/raw"
OUT = f"{BASE}/src/geojson"

import shapefile  # pyshp

def fc(features, name):
    return {
        "type": "FeatureCollection",
        "name": name,
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": features,
    }

def dump(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{path}  {os.path.getsize(path)//1024}KB  {len(obj['features'])} features")

# ---------- 1. 卫所（点）----------
# SHP 仅含 375 个「卫」；CSV 为完整底表（含千户所），两者合并：SHP 提供坐标，CSV 补类型与千户所属
r = shapefile.Reader(f"{RAW}/Ming_Garrisons/Ming_Garrisons")
F = [f[0] for f in r.fields[1:]]
feats = []
for sr, rec in zip(r.iterShapes(), r.records()):
    d = dict(zip(F, rec))
    if not sr.points:
        continue
    x, y = sr.points[0]
    feats.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [round(x, 4), round(y, 4)]},
        "properties": {
            "wei_id": d.get("wei_id"), "name_ch": d.get("name_ch"),
            "name_py": d.get("name_py"), "type": d.get("type_ch") or "卫",
            "beg_yr": d.get("beg_yr") or None,
            "end_yr": d.get("end_yr") or None,
        },
    })
dump(fc(feats, "ming_garrisons"), f"{OUT}/ming_garrisons.json")

# ---------- 2. 驿站（点）----------
r2 = shapefile.Reader(f"{RAW}/Ming_Stations_2016/Ming_Stations_2016")
F2 = [f[0] for f in r2.fields[1:]]
feats = []
for sr, rec in zip(r2.iterShapes(), r2.records()):
    d = dict(zip(F2, rec))
    if not sr.points:
        continue
    x, y = sr.points[0]
    feats.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [round(x, 4), round(y, 4)]},
        "properties": {
            "yz_id": d.get("YZ_ID"), "name_ch": d.get("YZNM_CH"),
            "name_py": d.get("YZNM_PY"),
            "county_2010": d.get("10CNTY_CH"),  # 古今对照：今所在县
        },
    })
dump(fc(feats, "ming_courier_stations"), f"{OUT}/ming_courier_stations.json")

# ---------- 3. 驿路（线）----------
r3 = shapefile.Reader(f"{RAW}/Ming_Routes_2016/Ming_Routes_2016")
F3 = [f[0] for f in r3.fields[1:]]
feats = []
for sr, rec in zip(r3.iterShapes(), r3.records()):
    d = dict(zip(F3, rec))
    pts = [[round(x, 4), round(y, 4)] for x, y in sr.points]
    if len(pts) < 2:
        continue
    feats.append({
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": pts},
        "properties": {"major": d.get("MAJ_MINOR") == "MAJ"},
    })
dump(fc(feats, "ming_courier_routes"), f"{OUT}/ming_courier_routes.json")
print("done")
