# D3 · 核心组件规格（C1–C12）

> 组件库为 Web Components（Astro islands 或原生），命名 `mh-*`（明史）。全部样式走 D1 token。

## C1 三层阅读块 `mh-reading`
- **结构**：`<div class="tldr">`（TL;DR 一句话，柘黄左边线）→ 正文段落 → `<details class="deep">` 深读考据
- **状态**：TL;DR 常显；深读默认折叠，`<summary>` 显示「深读与考据（n 条）」；打开后 `--shadow-1` 浮起
- **规则**：正文内术语/人名/出处由构建期标注（md 扩展语法：`[[票拟]]`、`{{人物:于谦}}`、`[[[1|《明史·于谦传》]]]`），渲染为 C2/C8/C3
- **可访问性**：details 原生键盘可达；TL;DR 有 `aria-label="一句话结论"`

## C2 术语弹窗 `mh-term`
- **触发**：正文术语渲染为虚线下划线词；click/tap 打开；**不跳页**
- **弹层**：260px 卡片，内容 = glossary.json 的 def + related 跳转链 + 「查看术语表 →」
- **状态**：桌面 hover 预览（300ms 延迟）+ click 固定；移动端仅 tap，底部抽屉式
- **可访问性**：`role="button" aria-haspopup="dialog"`；Esc/点击外部关闭

## C3 史料等级标 `mh-source-badge`
- **形态**：行内 10px 方标（①②③④ 或数字），色取 `--c-source-1..4`
- **悬停**：tooltip 显示「① 正史官修：《明史》《明实录》《大明会典》」等释义
- **四级定义**：① 正史/官修 ② 当时人著述 ③ 现代研究 ④ 传闻野史（必须醒目）

## C4 参考文献列表 `mh-references`
- 页尾组件；按等级分四组着色列表，条目格式 `作者《书名·篇卷》（出版信息）`
- 数据源：页面 frontmatter 的 refs 数组；与正文 C3 标一一对应

## C5 误区辨析框 `mh-myth`
- **形态**：警示框——左 3px `--c-source-4` 竖线 + ⚠ 图标 + 「常见误传」标题 + 正文（含史实更正与出处）
- **用途**：events.json 的 misconceptions[]、创作者专区误区清单
- **规则**：内容必须给出更正来源；纯猎奇禁入

## C6 考据框 `mh-disputed`
- **形态**：左 3px `--c-disputed` 竖线 + 🔍 + 「考据」标题；正文为诸说并列（每说一行，尾挂 C3）
- **用途**：emperors/consorts/events 的 disputed 字段渲染（建文下落、成祖生母等）

## C7 时间锚 `mh-era-strip`
- **形态**：h28 横条，16 段按 D1 十六朝色着色；段内显示年号（12px，段宽不足显示庙号首字）
- **两种模式**：筛选模式（列表页：点击=按朝过滤 URL query）、定位模式（详情页：当前朝高亮 + 底线 2px 朱砂，点击跳该朝模块视图）
- **移动**：横滑 + 当前段自动滚入

## C8 人物悬浮卡 `mh-figure-pop`
- 正文人名 hover/长按出 320×180 卡：姓名/生卒/类别/一句话；点击进 `/figures/[id]`
- 数据：figures.json 轻量索引（构建期注入）

## C9 关联四联卡 `mh-relation-grid`
- 详情页底部固定四列：**同期皇帝 / 相关事件 / 相关人物 / 相关图表**（各 3–6 卡）
- 数据来自各 JSON 的交叉字段（emperors.stage / events.figures / relations）
- 移动端 2×2

## C10 图注卡 `mh-figure`（配图）
- 图片 + 图注（题名 · 作者/藏地 · 许可徽标）；数据源 assets/images/manifest.json
- CC 图自动生成署名链接；PD 图显示藏地；自绘图显示「本站绘制」
- 帝王画像缺项时显示线描占位 + 「无存世官方像」说明

## C11 印章 `mh-seal`
- CSS 方印：`--c-vermilion` 底 + 纸色字，尺寸 24/32/38 三档；可变文字（明/模块名首字）

## C12 筛选器 `mh-filter-bar`
- 胶囊组（多选），选中态柘黄填充；与 C7 时间锚联动写 URL query；计数徽标显示各桶数量
- 移动端折叠为「筛选（n） ▾」

## 交互一致性约定
- 弹层 z-index 一律 `--z-modal`；打开弹层时 body 滚动锁定
- 触控热区 ≥44px；focus-visible 用 2px 朱砂外圈
- 所有异步组件有骨架态；错误态显示「数据暂缺 + 来源链接」而非空白
