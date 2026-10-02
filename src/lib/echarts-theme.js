// ECharts 主题（D4 规范）· 双模式：chartTheme() 按当前 data-theme 返回，themechange 时组件重渲染
export const chartTheme = () => {
  const dark = typeof document !== "undefined" && document.documentElement.dataset.theme === "dark";
  if (dark) {
    return {
      dark: true,
      color: ["#C8564F", "#6C93C4", "#7FB894", "#D4B578", "#C2A878", "#D08A64", "#9B8BB5", "#86A992", "#C9B085", "#A3927F"],
      ink: "#E8E2D0", sub: "#B5AC98",
      split: "rgba(181,172,152,0.14)", axis: "#8A7F6B",
      tooltip: {
        backgroundColor: "rgba(38,35,32,0.97)", borderColor: "rgba(181,172,152,0.35)", borderWidth: 1,
        textStyle: { color: "#E8E2D0", fontSize: 13 },
        extraCssText: "box-shadow:0 4px 16px rgba(0,0,0,.5);border-radius:8px;",
      },
      legend: { textStyle: { color: "#B5AC98", fontSize: 12 }, itemWidth: 14, itemHeight: 9, icon: "roundRect" },
      title: { textStyle: { color: "#E8E2D0", fontSize: 16, fontWeight: 600 }, subtextStyle: { color: "#B5AC98", fontSize: 12 } },
      backgroundColor: "transparent",
      textStyle: { fontFamily: '"Noto Sans SC", "PingFang SC", sans-serif', color: "#E8E2D0" },
    };
  }
  return {
    dark: false,
    color: ["#A02C2C", "#2E5A88", "#3E7C59", "#C6A664", "#8A6D3B", "#9E5B3C", "#5A4A6E", "#4E6E5D", "#B08D57", "#6E5C4E"],
    ink: "#2B2620", sub: "#5C5346",
    split: "rgba(138,109,59,0.15)", axis: "#8A6D3B",
    tooltip: {
      backgroundColor: "rgba(247,243,232,0.97)", borderColor: "rgba(138,109,59,0.4)", borderWidth: 1,
      textStyle: { color: "#2B2620", fontSize: 13 },
      extraCssText: "box-shadow:0 4px 16px rgba(43,38,32,.15);border-radius:8px;",
    },
    legend: { textStyle: { color: "#5C5346", fontSize: 12 }, itemWidth: 14, itemHeight: 9, icon: "roundRect" },
    title: { textStyle: { color: "#2B2620", fontSize: 16, fontWeight: 600 }, subtextStyle: { color: "#5C5346", fontSize: 12 } },
    backgroundColor: "transparent",
    textStyle: { fontFamily: '"Noto Sans SC", "PingFang SC", sans-serif', color: "#2B2620" },
  };
};

// 图表重渲染挂载：监听 themechange 与系统切换，重建实例
export const onThemeChange = (rerender) => {
  window.addEventListener("themechange", rerender);
  const mq = matchMedia("(prefers-color-scheme: dark)");
  mq.addEventListener?.("change", rerender);
};

export const ERAS_BAND = [
  ["洪武", 1368, 1398, "#A02C2C", "hongwu"], ["建文", 1399, 1402, "#8A6D3B", "jianwen"],
  ["永乐", 1403, 1424, "#8A6D3B", "yongle"], ["洪熙", 1425, 1425, "#C6A664", "hongxi"],
  ["宣德", 1426, 1435, "#C6A664", "xuande"], ["正统", 1436, 1449, "#9E5B3C", "yingzong"],
  ["景泰", 1450, 1457, "#9E5B3C", "jingtai"], ["天顺", 1457, 1464, "#9E5B3C", "yingzong"],
  ["成化", 1465, 1487, "#3E7C59", "chenghua"], ["弘治", 1488, 1505, "#3E7C59", "hongzhi"],
  ["正德", 1506, 1521, "#5A4A6E", "zhengde"], ["嘉靖", 1522, 1566, "#5A4A6E", "jiajing"],
  ["隆庆", 1567, 1572, "#2E5A88", "longqing"], ["万历", 1573, 1620, "#2E5A88", "wanli"],
  ["泰昌", 1620, 1620, "#2B2620", "taichang"], ["天启", 1621, 1627, "#2B2620", "tianqi"],
  ["崇祯", 1628, 1644, "#2B2620", "chongzhen"],
];
