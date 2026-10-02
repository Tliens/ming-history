# 地理数据来源与署名（ATTRIBUTION）

本目录所有数据文件必须能回溯到下表来源。 MapCore 地图页脚注自动引用本文件。

| 文件 | 来源 | 许可 | 加工 |
|---|---|---|---|
| `ming_garrisons.json` | Military Wei (Guards) and Suo (Battalions) of the Ming Dynasty (1368-1644), PI: Michael Szonyi, ed. John Wong, CHGIS 分发, DOI: [10.7910/DVN/5RUXK8](https://doi.org/10.7910/DVN/5RUXK8)。底本：Liew Foon Ming《明史兵志英译注》(Hamburg, 1998)；地理定位基于 CHGIS V3 | 学术使用（README 标注 GPL） | SHP→GeoJSON，坐标 4 位小数；仅「卫」级 375 点，字段保留 beg_yr/end_yr 供时间过滤 |
| `ming_courier_stations.json` | V6 Ming Dynasty Courier Routes and Stations, ed. Lex Berman（据杨正泰《明代驿站考》+ 1903 邮政图集）, CHGIS 分发, DOI: [10.7910/DVN/SB8ZTM](https://doi.org/10.7910/DVN/SB8ZTM) | 学术使用（CHGIS 条款） | SHP→GeoJSON 1000 点；保留 2010 年所在县（county_2010）作古今对照 |
| `ming_courier_routes.json` | 同上 | 同上 | SHP→GeoJSON 1043 段，MAJ_MINOR 转布尔 major |
| `ming_provinces_1391.json`（257KB，首屏层） | Hartwell China HGIS v5 时间切片 1391（洪武二十四年），CHGIS V5 (2010), DOI: [10.7910/DVN/29302](https://doi.org/10.7910/DVN/29302), © Harvard Fairbank Center & 复旦史地所 | **CC BY-NC-SA 3.0** | 305 府级面按省级 unary_union→simplify(0.012°)；西安80/GK19→WGS84；21 省级面；命名考据警示见 research/R10（展示层须用 display_name 覆盖「京師→北平」等时代错位） |
| `ming_prefectures_1391.json`（3.2MB，LOD 高层懒加载） | 同上 | 同上 | simplify(0.008°)，含繁简双名/拼音/类型/层级 geocode；发布前转 TopoJSON 压缩（E9 MapCore 任务） |

## 使用条款（重要）

- CHGIS 系列条款：**免费用于学术研究；禁止商业使用、转售与再分发**。
  本站定位为非商业教育/知识网站并逐图署名，属学术使用范畴；**若未来商业化或要求完全开放再分发，须替换为自绘边界**（见 docs/PLAN §8 风险表）。
- CHGIS V6 主库（政区时间序列）许可同上且更严格——明代政区切片的取舍见 docs/content/06 号文档「数据源」节与 TODO R10 备注。
- 引用格式：每张使用上述数据的地图，页脚标注 `Data: CHGIS, Harvard University and Fudan University (CC BY-NC 学术使用)` 及对应 DOI。
