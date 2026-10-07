// V10 郑和航线数据（航点坐标为今地约位；航线为示意连线，非复原航路）
// 依据：《明史·郑和传》①、时珍? 不——依据《明史·郑和传》①与《瀛涯胜览》《星槎胜览》②（地名考订采学界通说）
export const WAYPOINTS = {
  liujiagang: { n: "刘家港", now: "江苏太仓", c: [121.1, 31.45], note: "集结出海港" },
  changle: { n: "长乐太平港", now: "福建福州", c: [119.52, 25.96], note: "候风开洋（福建基地）" },
  zhancheng: { n: "占城", now: "越南归仁", c: [108.2, 13.8], note: "首站属国" },
  javaya: { n: "爪哇", now: "印尼泗水一带", c: [112.75, -7.25], note: "下东西洋分航处" },
  jiugang: { n: "旧港", now: "印尼巨港", c: [104.75, -2.99], note: "剿陈祖义、设旧港宣慰司" },
  manlajia: { n: "满剌加", now: "马来西亚马六甲", c: [102.25, 2.2], note: "官厂（基地港）" },
  xilan: { n: "锡兰山", now: "斯里兰卡", c: [80.4, 6.6], note: "擒其王之战（1411）" },
  guli: { n: "古里", now: "印度卡利卡特", c: [75.78, 11.25], note: "西洋大码头；郑和卒地（1433）" },
  hurumosi: { n: "忽鲁谟斯", now: "伊朗霍尔木兹", c: [56.45, 26.2], note: "波斯湾口大集" },
  banggel: { n: "榜葛剌", now: "孟加拉吉大港一带", c: [91.83, 22.33], note: "麒麟（长颈鹿）经由" },
  mugudushu: { n: "木骨都束", now: "索马里摩加迪沙", c: [45.34, 2.04], note: "东非首站" },
  malin: { n: "麻林", now: "肯尼亚马林迪", c: [40.12, -3.22], note: "麻林贡麒麟（1415）" },
  tianfang: { n: "天方", now: "沙特麦加", c: [39.83, 21.42], note: "第七次分舡往（通事往）" },
};
// 七次航次的骨干航段（节点 id 序列；示意）
export const VOYAGES = [
  { n: "第一次", years: "1405–1407", legs: [["liujiagang", "changle"], ["changle", "zhancheng"], ["zhancheng", "javaya"], ["javaya", "jiugang"], ["jiugang", "manlajia"], ["manlajia", "xilan"], ["xilan", "guli"]] },
  { n: "第二次", years: "1407–1409", legs: [["liujiagang", "changle"], ["changle", "zhancheng"], ["zhancheng", "javaya"], ["javaya", "manlajia"], ["manlajia", "guli"]] },
  { n: "第三次", years: "1409–1411", legs: [["liujiagang", "changle"], ["changle", "zhancheng"], ["zhancheng", "manlajia"], ["manlajia", "xilan"], ["xilan", "guli"]] },
  { n: "第四次", years: "1413–1415", legs: [["liujiagang", "changle"], ["changle", "zhancheng"], ["zhancheng", "manlajia"], ["manlajia", "guli"], ["guli", "hurumosi"], ["manlajia", "banggel"]] },
  { n: "第五次", years: "1417–1419", legs: [["liujiagang", "changle"], ["changle", "zhancheng"], ["zhancheng", "manlajia"], ["manlajia", "guli"], ["guli", "hurumosi"], ["guli", "mugudushu"], ["mugudushu", "malin"]] },
  { n: "第六次", years: "1421–1422", legs: [["liujiagang", "changle"], ["changle", "zhancheng"], ["zhancheng", "manlajia"], ["manlajia", "guli"], ["guli", "hurumosi"], ["guli", "mugudushu"]] },
  { n: "第七次", years: "1430–1433", legs: [["liujiagang", "changle"], ["changle", "zhancheng"], ["zhancheng", "manlajia"], ["manlajia", "guli"], ["guli", "hurumosi"], ["hurumosi", "tianfang"], ["guli", "mugudushu"]] },
];
