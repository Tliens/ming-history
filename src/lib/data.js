// 数据加载层：全部内容数据的单一入口（构建期导入）
import emperors from "../data/emperors/emperors.json";
import events from "../data/events/events.json";
import offices from "../data/offices.json";
import secretaries from "../data/first-secretaries.json";
import consorts from "../data/consorts/consorts.json";
import figures from "../data/figures/figures.json";
import relations from "../data/figures/figure-relations.json";
import glossary from "../data/glossary.json";
import manifest from "../../assets/images/manifest.json";

export { emperors, events, offices, secretaries, consorts, figures, relations, glossary, manifest };

// 十六朝年号表（时间锚 / 年号换算；与 emperors.json 同步维护）
export const ERAS = [
  { name: "洪武", start: 1368, end: 1398, emperor: "hongwu", color: "#A02C2C" },
  { name: "建文", start: 1399, end: 1402, emperor: "jianwen", color: "#8A6D3B" },
  { name: "永乐", start: 1403, end: 1424, emperor: "yongle", color: "#8A6D3B" },
  { name: "洪熙", start: 1425, end: 1425, emperor: "hongxi", color: "#C6A664" },
  { name: "宣德", start: 1426, end: 1435, emperor: "xuande", color: "#C6A664" },
  { name: "正统", start: 1436, end: 1449, emperor: "yingzong", color: "#9E5B3C" },
  { name: "景泰", start: 1450, end: 1457, emperor: "jingtai", color: "#9E5B3C" },
  { name: "天顺", start: 1457, end: 1464, emperor: "yingzong", color: "#9E5B3C" },
  { name: "成化", start: 1465, end: 1487, emperor: "chenghua", color: "#3E7C59" },
  { name: "弘治", start: 1488, end: 1505, emperor: "hongzhi", color: "#3E7C59" },
  { name: "正德", start: 1506, end: 1521, emperor: "zhengde", color: "#5A4A6E" },
  { name: "嘉靖", start: 1522, end: 1566, emperor: "jiajing", color: "#5A4A6E" },
  { name: "隆庆", start: 1567, end: 1572, emperor: "longqing", color: "#2E5A88" },
  { name: "万历", start: 1573, end: 1620, emperor: "wanli", color: "#2E5A88" },
  { name: "泰昌", start: 1620, end: 1620, emperor: "taichang", color: "#2B2620" },
  { name: "天启", start: 1621, end: 1627, emperor: "tianqi", color: "#2B2620" },
  { name: "崇祯", start: 1628, end: 1644, emperor: "chongzhen", color: "#2B2620" },
];

export function eraOf(year) {
  let cur = ERAS[0];
  for (const e of ERAS) if (e.start <= year) cur = e;
  const num = year - cur.start + 1;
  return { era: cur, text: `${cur.name}${num === 1 ? "元年" : num + "年"}` };
}

export const emperorById = (id) => emperors.emperors.find((e) => e.id === id);
export const portraitOf = (id) => manifest.images.find((i) => i.id === `emperor-${id}`);

export const eventsByYear = () =>
  [...events.events].sort((a, b) => a.year - b.year);

export const eventsOfEmperor = (emp) => {
  const breaks = emp.reignBreak ? [emp.reignBreak] : [];
  return events.events.filter((ev) => {
    if (ev.year >= emp.reignStart && ev.year <= emp.reignEnd) {
      const br = breaks.find((b) => ev.year >= b.start && ev.year <= b.end);
      return !br;
    }
    return false;
  });
};

export const secretariesOf = (emp) => {
  const out = [];
  for (const s of secretaries.secretaries)
    for (const t of s.terms)
      if (t.start <= emp.reignEnd && (t.end ?? t.start) >= emp.reignStart)
        out.push({ name: s.name, start: t.start, end: t.end ?? t.start, note: t.note });
  return out.sort((a, b) => a.start - b.start);
};

export const figuresById = Object.fromEntries(figures.figures.map((f) => [f.id, f]));

export const relationsOf = (figId) =>
  relations.edges
    .filter((e) => e[0] === figId || e[2] === figId)
    .map((e) => {
      const [a, type, b] = e;
      const other = a === figId ? b : a;
      const dir = a === figId ? 1 : -1; // 1 = 出边
      return { type, other, dir };
    })
    .filter((r) => figuresById[r.other] || emperorById(r.other));

export const SOURCE_LEVELS = {
  1: "① 正史官修（《明史》《明实录》《大明会典》等）",
  2: "② 当时人著述（《国榷》《万历野获编》《明史纪事本末》等）",
  3: "③ 现代研究（孟森、黄仁宇、樊树志、顾诚等）",
  4: "④ 传闻/野史/演义（仅入误区与当代接受框）",
};
