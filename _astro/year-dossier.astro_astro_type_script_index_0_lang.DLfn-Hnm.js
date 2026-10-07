import{e as d}from"./emperors.pffwcHaj.js";import{e as h}from"./events.JbIQYdwi.js";import{s as $}from"./first-secretaries.C5smZxn7.js";import{f}from"./figures.D8mivB5C.js";const x=d.emperors,p=h.events,y=$.secretaries,v=f.figures,u=[["洪武",1368,1398],["建文",1399,1402],["永乐",1403,1424],["洪熙",1425,1425],["宣德",1426,1435],["正统",1436,1449],["景泰",1450,1457],["天顺",1457,1464],["成化",1465,1487],["弘治",1488,1505],["正德",1506,1521],["嘉靖",1522,1566],["隆庆",1567,1572],["万历",1573,1620],["泰昌",1620,1620],["天启",1621,1627],["崇祯",1628,1644]],E="甲乙丙丁戊己庚辛壬癸",z="子丑寅卯辰巳午未申酉戌亥",b=e=>E[((e-4)%10+10)%10]+z[((e-4)%12+12)%12];function k(e){const r=u.find(n=>e>=n[1]&&e<=n[2]),a=r?`${r[0]}${e-r[1]+1}年`:"南明纪年（简编）",t=x.find(n=>e>=n.reignStart&&e<=n.reignEnd),s=t?e-t.reignStart+1:0,l=y.filter(n=>n.terms.some(i=>i.start<=e&&(i.end??i.start)>=e)),m=p.filter(n=>n.year===e),c=p.filter(n=>Math.abs(n.year-e)===1),g=v.filter(n=>n.birth&&n.birth<=e&&(n.death??9999)>=e).sort((n,i)=>(n.death??1700)-(i.death??1700));return{y:e,eraText:a,ganzhi:b(e),emp:t,empReignNo:s,secs:l,sameYear:m,nearby:c,alive:g}}function j(e){const r=document.getElementById("dossier"),a=(t,s)=>t.length?`<ul style="font-size:14px;line-height:1.9">${t.map(s).join("")}</ul>`:'<p style="font-size:13px;color:var(--c-ink-2)">（本年无记录）</p>';r.innerHTML=`
      <div class="card" style="padding:18px 22px">
        <h2 style="margin:0;font-size:26px">${e.y} 年 <span style="font-size:18px;color:var(--c-ink-2)">· ${e.eraText} · ${e.ganzhi}年</span></h2>
        ${e.emp?`<p style="font-size:15px;margin:10px 0 0">在位：<a href="/emperors/${e.emp.id}"><strong>${e.emp.templeName} · ${e.emp.name}</strong></a>（${e.emp.era}${e.emp.eras?"／"+e.emp.eras.map(t=>t.era).join("、"):""}，在位第 ${e.empReignNo} 年）—— ${e.emp.brief}</p>`:'<p style="font-size:14px;color:var(--c-ink-2)">此年在明朝全国性政权之外（南明时期，见皇帝页南明简编）。</p>'}
      </div>

      <div class="card" style="padding:16px 22px;margin-top:14px">
        <h3 style="margin:0 0 6px;font-size:16px">当任首辅 / 阁臣居首</h3>
        ${a(e.secs,t=>`<li><a href="/power/secretaries"><strong>${t.name}</strong></a>（${t.terms.map(s=>s.start+"–"+(s.end??s.start)).join("；")}）—— ${t.note??""}</li>`)}
      </div>

      <div class="card" style="padding:16px 22px;margin-top:14px">
        <h3 style="margin:0 0 6px;font-size:16px">大事（当年 ${e.sameYear.length} 条 · 前后一年 ${e.nearby.length} 条）</h3>
        ${a(e.sameYear,t=>`<li><a href="/events/${t.id}"><strong>${t.title}</strong></a>——${t.result.slice(0,60)}…</li>`)}
        ${e.nearby.length?`<p style="font-size:13px;color:var(--c-ink-2);margin:8px 0 2px">前后一年：</p><ul style="font-size:13px;line-height:1.8">${e.nearby.map(t=>`<li>${t.year} · <a href="/events/${t.id}">${t.title}</a></li>`).join("")}</ul>`:""}
      </div>

      <div class="card" style="padding:16px 22px;margin-top:14px">
        <h3 style="margin:0 0 6px;font-size:16px">在世人物（生卒可考者 ${e.alive.length} 人）</h3>
        ${e.alive.length?`<p style="font-size:13px;margin:0">${e.alive.map(t=>`<a href="/figures/${t.id}" title="${t.birth}–${t.death} · ${t.career??""}">${t.name}</a>`).join(" · ")}</p>`:'<p style="font-size:13px;color:var(--c-ink-2)">（无生卒可考的人物在世——数据库生卒覆盖率有限，写作请勿据此断言「某年无人」）</p>'}
      </div>

      <p style="font-size:12px;color:var(--c-ink-2);margin-top:10px">数据源：emperors.json / first-secretaries.json / events.json / figures.json（仓库内可见出处）。首辅年份精确到年、月份待校对轮；人物生卒缺载者未列入。</p>
    `,r.style.display="block"}function o(){const e=Math.round(+document.getElementById("dYear").value);e>=1368&&e<=1644?j(k(e)):(document.getElementById("dossier").innerHTML='<p class="mh-myth" style="display:block">请输入 1368–1644 之间的年份（南明 1644–1662 暂按简编处理，请用皇帝页）。</p>',document.getElementById("dossier").style.display="block")}document.getElementById("dGo").addEventListener("click",o);document.getElementById("dYear").addEventListener("keydown",e=>{e.key==="Enter"&&o()});o();
