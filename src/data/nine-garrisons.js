// V8 九边重镇数据（镇城坐标为通说治所；概述据《明史·兵志》③与赵现海《明代九边长城军镇史》③）
export const GARRISON_TOWNS = [
  { id: "liaodong", name: "辽东镇", seat: "广宁／辽阳", coord: [122.2, 41.3], garrison: "总兵驻广宁，巡抚驻辽阳", note: "九边之首，防蒙古与女真；努尔哈赤起于其辖下建州，萨尔浒在其东", events: ["salahu-1619", "ningyuan-1626", "songjin-1640"] },
  { id: "jizhou", name: "蓟州镇", seat: "三屯营", coord: [117.96, 40.19], garrison: "拱卫京师东翼", note: "戚继光练兵修空心敌台十六年；己巳之变皇太极自此段破边墙", events: ["jisi-1629"] },
  { id: "xuanfu", name: "宣府镇", seat: "宣化", coord: [115.05, 40.6], garrison: "京师西北门户", note: "「九边要冲居其半」；土木堡在其辖区（怀来土木）", events: ["tumu-crisis-1449"] },
  { id: "datong", name: "大同镇", seat: "大同", coord: [113.3, 40.08], garrison: "极冲之首", note: "俺答封贡的谈判与互市前沿（得胜堡）", events: ["anda-ennoblement-1571", "geng-xu-1550"] },
  { id: "shanxi", name: "山西镇（三关）", seat: "偏头关", coord: [111.5, 39.44], garrison: "雁门、宁武、偏头外三关", note: "宁武关是 1644 年周遇吉死守之地", events: ["sun-chuanting-1643"] },
  { id: "yansui", name: "延绥镇（榆林）", seat: "榆林", coord: [109.73, 38.28], garrison: "边墙重镇", note: "明末民变的爆发区之一（陕北）", events: ["shaanxi-uprising-1627"] },
  { id: "ningxia", name: "宁夏镇", seat: "银川", coord: [106.27, 38.47], garrison: "河套防区", note: "1592 年哱拜之变即在此镇城", events: ["ningxia-1592"] },
  { id: "guyuan", name: "固原镇", seat: "固原", coord: [106.24, 36.0], garrison: "陕西三边总督驻节", note: "内层指挥中枢，辖西北诸卫", events: [] },
  { id: "gansu", name: "甘肃镇", seat: "甘州（张掖）", coord: [100.45, 38.93], garrison: "河西走廊", note: "嘉峪关为极西锁钥", events: [] },
];
