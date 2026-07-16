# -*- coding: utf-8 -*-
"""将物理知识图谱产品打包为单一自包含 HTML 文件（零外部依赖）。"""
import os, re, json, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, "physics_detailed_graph.html")
SVG  = os.path.join(ROOT, "physics_knowledge_graph.svg")
OUT_HTML = os.path.join(ROOT, "物理知识图谱_单文件版.html")
OUT_ZIP = os.path.join(ROOT, "物理知识图谱_单文件版.zip")
VER  = "v1.2"

h = open(SRC, encoding="utf-8").read()
svg_raw = open(SVG, encoding="utf-8").read()

# ---------- 1) 提取权威数据 DATA ----------
i = h.index("const DATA = "); j = h.index(";", i)
data_json = h[i + len("const DATA = "):j]

# ---------- 2) 提取 DEMO_TRAP (单层对象, 无嵌套{}) ----------
tm = re.search(r"const DEMO_TRAP = (\{[^{}]*\})", h, re.S)
trap_json = tm.group(1)

# ---------- 3) 提取 DEMOS 引擎块 + runDemo 函数 ----------
di = h.index("function dist("); ri = h.index("function runDemo")
demos_block = h[di:ri]
depth = 0; k = None
for off in range(ri, len(h)):
    if h[off] == "{":
        depth += 1
    elif h[off] == "}":
        depth -= 1
        if depth == 0:
            k = off; break
run_demo_fn = h[ri:k + 1]

# ---------- 4) 内联 SVG 总览 ----------
sm = re.search(r"(<svg[\s\S]*?</svg>)", svg_raw, re.S)
svg_inline = sm.group(1)

print("DATA 考点:", data_json.count('"name"') // 2, "| TRAP 键:", trap_json.count('"'))
print("DEMOS 块:", len(demos_block), "字节 | runDemo:", len(run_demo_fn), "字节")

# ---------- 5) 单文件 HTML 模板 ----------
TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>浙江新高考物理知识图谱 · 单文件版</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:'PingFang SC','Microsoft YaHei',sans-serif;background:#0b1220;color:#e2e8f0}
header{background:linear-gradient(120deg,#1e3a8a,#0ea5e9);color:#fff;padding:14px 20px;display:flex;align-items:baseline;gap:12px}
header h1{margin:0;font-size:18px}
header .v{font-size:12px;opacity:.85}
.tabs{display:flex;gap:8px;padding:10px 20px;background:#0f1a30;border-bottom:1px solid #1e293b;flex-wrap:wrap}
.tab{padding:8px 16px;border-radius:8px;cursor:pointer;background:#1e293b;color:#cbd5e1;font-size:14px;font-weight:600;user-select:none}
.tab:hover{background:#273449}
.tab.active{background:#0ea5e9;color:#fff}
section{display:none;padding:16px 20px}
section.show{display:block}
/* 总览 */
#overview{background:#fff;color:#1e293b;min-height:80vh}
#overview svg{max-width:680px;width:100%;height:auto;display:block;margin:0 auto}
.modlist{display:flex;flex-wrap:wrap;gap:10px;margin:14px auto 0;justify-content:center;max-width:720px}
.modpill{background:#e0f2fe;color:#0369a1;padding:6px 12px;border-radius:20px;font-size:13px;font-weight:600}
/* 考点细化 */
#detail.show{display:flex;gap:16px;align-items:flex-start}
#nav{width:240px;flex:none;max-height:80vh;overflow:auto;background:#0f1a30;border-radius:10px;padding:10px}
.mod-h{font-weight:700;color:#7dd3fc;margin:10px 0 4px;font-size:13px}
.pt{padding:5px 10px;margin:2px 0;cursor:pointer;border-radius:6px;font-size:13px;color:#cbd5e1}
.pt:hover{background:#1e293b}
.pt.sel{background:#0ea5e9;color:#fff}
#main{flex:1;max-height:80vh;overflow:auto;min-width:0}
.card{background:#0f1a30;border-radius:12px;padding:18px}
.card h2{margin:0 0 12px;color:#fff;font-size:18px}
.lab{font-weight:700;color:#38bdf8;margin:10px 0 4px;font-size:13px}
.sub{margin:4px 0;padding-left:18px;line-height:1.7}
.sec{margin:8px 0}
.exam{background:#0b1f17;border-left:4px solid #22c55e;padding:10px 14px;border-radius:0 8px 8px 0;margin:8px 0}
.exam.typ{border-left-color:#eab308;background:#1f1a08}
.tag{display:inline-block;background:#1e293b;color:#7dd3fc;font-size:11px;padding:2px 8px;border-radius:10px;margin:4px 0}
.q{margin:6px 0;line-height:1.7}
.a{color:#86efac;font-size:13px;line-height:1.7}
.n{color:#94a3b8;font-size:12px;line-height:1.6;margin-top:4px}
.pit{background:#2a0f12;border-left:4px solid #ef4444;padding:8px 12px;border-radius:0 8px 8px 0;margin:8px 0}
.con{background:#1e1030;border-left:4px solid #a855f7;padding:8px 12px;border-radius:0 8px 8px 0;margin:8px 0}
.tip{background:linear-gradient(120deg,#eff6ff,#dbeafe);border-left:4px solid #2563eb;padding:8px 12px;border-radius:0 8px 8px 0;margin:8px 0;color:#1e3a8a;font-weight:600;font-size:13px}
.pit ul,.con ul{margin:4px 0;padding-left:18px;line-height:1.7}
.trap{background:#3a2a08;color:#fde047;border-left:4px solid #f59e0b;padding:6px 12px;border-radius:0 8px 8px 0;margin-top:8px;font-size:12px;line-height:1.6}
/* 演示 */
.demo-mod{color:#7dd3fc;margin:16px 0 8px;border-bottom:1px dashed #1e293b;padding-bottom:4px}
.demo-card{background:#0f1a30;border-radius:10px;padding:10px;margin:8px 0;border:1px solid #1e293b}
.dc-title{cursor:pointer;font-weight:600;color:#e2e8f0;margin-bottom:6px}
.dc-title:hover{color:#38bdf8}
.read{color:#7dd3fc;font-size:12px;margin:4px 0;min-height:16px}
/* 练习册 */
.pm{color:#7dd3fc;border-bottom:1px solid #1e293b;padding-bottom:6px;margin-top:18px}
.pm span{color:#64748b;font-size:12px;font-weight:400}
.pc{background:#0b1426;border-radius:10px;padding:12px 16px;margin:10px 0}
.pc h3{margin:0 0 6px;color:#fff;font-size:15px}
.pex{background:#0b1f17;border-left:4px solid #22c55e;padding:8px 12px;border-radius:0 8px 8px 0;font-size:13px;line-height:1.7;margin:6px 0}
.pex.typ{border-left-color:#eab308;background:#1f1a08}
.pex i{color:#86efac;display:block;margin-top:3px;font-style:normal}
.pe{font-size:13px;line-height:1.7;margin:4px 0}
.pe b{color:#38bdf8}
footer{color:#64748b;font-size:12px;text-align:center;padding:14px}
</style>
</head>
<body>
<header>
  <h1>浙江新高考物理 · 知识图谱与真题体系</h1>
  <span class="v">单文件版 __VER__ · 零依赖 · 双击即用</span>
</header>
<div class="tabs">
  <div class="tab" data-tab="overview">① 知识图谱总览</div>
  <div class="tab" data-tab="detail">② 考点细化与真题</div>
  <div class="tab" data-tab="demos">③ 课堂动态演示</div>
  <div class="tab" data-tab="practice">④ 真题练习册</div>
</div>

<section id="overview">
  __SVG__
  <div class="modlist" id="modlist"></div>
</section>

<section id="detail">
  <div id="nav"></div>
  <div id="main"></div>
</section>

<section id="demos">
  <div id="demosWrap"></div>
</section>

<section id="practice">
  <div id="practiceWrap"></div>
</section>

<footer>物理为浙江“7选3”选考科目 · 27 主知识点 / 123 细分 / 27 道真实浙江选考真题 / 25 种动态演示（真实量纲 + 命题陷阱）· 单文件离线版</footer>

<script>
const DATA = __DATA__;
const DEMO_TRAP = __TRAP__;
__DEMOS__
__RUNDEMO__

const mods = DATA;
let demosBuilt = false;

// ---------- Tab 切换 ----------
function showTab(id){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('section').forEach(s=>s.classList.remove('show'));
  const t=document.querySelector('[data-tab="'+id+'"]'); if(t) t.classList.add('active');
  const s=document.getElementById(id); if(s) s.classList.add('show');
  if(id==='demos' && !demosBuilt){ buildDemos(); demosBuilt=true; }
}
document.querySelectorAll('.tab').forEach(t=>{
  t.onclick=()=>showTab(t.getAttribute('data-tab'));
});

// ---------- 总览模块权重 ----------
(function(){
  const ml=document.getElementById('modlist');
  mods.forEach(m=>{
    const p=document.createElement('span'); p.className='modpill';
    p.textContent=m.name+' · '+m.weight; ml.appendChild(p);
  });
})();

// ---------- 考点细化 ----------
function renderNav(){
  const nav=document.getElementById('nav'); nav.innerHTML='';
  mods.forEach(m=>{
    const h=document.createElement('div'); h.className='mod-h'; h.textContent=m.name+' ('+m.weight+')';
    nav.appendChild(h);
    m.points.forEach(p=>{
      const d=document.createElement('div'); d.className='pt'; d.textContent=p.name;
      d.onclick=()=>{ document.querySelectorAll('.pt').forEach(x=>x.classList.remove('sel')); d.classList.add('sel'); showPoint(m,p); };
      nav.appendChild(d);
    });
  });
}
function showPoint(m,p){
  const main=document.getElementById('main');
  const ex=p.exam; const isReal=!ex.src.startsWith('命卷视角');
  let html='<div class="card">';
  html+='<h2>'+m.name+' · '+p.name+'</h2>';
  html+='<div class="sec"><div class="lab">细分知识</div><ul class="sub">'+p.sub.map(s=>'<li>'+s+'</li>').join('')+'</ul></div>';
  html+='<div class="exam '+(isReal?'real':'typ')+'"><div class="lab">真题练习 '+(isReal?'🟢 真实':'🟡 仿真')+' · '+ex.src+'</div>';
  html+='<span class="tag">'+ex.tag+'</span>';
  html+='<div class="q">'+ex.q+'</div>';
  html+='<div class="a"><b>答案要点：</b>'+ex.a+'</div>';
  html+='<div class="n"><b>命卷提示：</b>'+ex.note+'</div></div>';
  html+='<div class="pit"><div class="lab">🔴 易错警示</div><ul>'+p.pit.map(s=>'<li>'+s+'</li>').join('')+'</ul></div>';
  html+='<div class="con"><div class="lab">🟣 易混辨析</div><ul>'+p.con.map(s=>'<li>'+s+'</li>').join('')+'</ul></div>';
  html+='<div class="tip"><div class="lab">🔵 妙法诀窍</div>'+p.tip+'</div>';
  html+='<div class="sec"><div class="lab">动态演示（拖动滑块观察参数关系）</div><div id="demoBox"></div></div>';
  html+='</div>';
  main.innerHTML=html;
  runDemo(p.demo, document.getElementById('demoBox'));
}

// ---------- 课堂演示（懒加载：点击才运行，避免动画互相取消）----------
function buildDemos(){
  const wrap=document.getElementById('demosWrap'); wrap.innerHTML='';
  let first=true;
  mods.forEach(m=>{
    const title=document.createElement('h3'); title.className='demo-mod'; title.textContent=m.name; wrap.appendChild(title);
    m.points.forEach(p=>{
      const card=document.createElement('div'); card.className='demo-card';
      const box=document.createElement('div'); box.className='dc-box';
      const t=document.createElement('div'); t.className='dc-title'; t.textContent='▶ '+p.name;
      card.appendChild(t); card.appendChild(box); wrap.appendChild(card);
      t.onclick=()=>{ runDemo(p.demo, box); };
      if(first){ first=false; setTimeout(()=>runDemo(p.demo, box), 120); }
    });
  });
}

// ---------- 真题练习册（文字版）----------
function buildPractice(){
  const wrap=document.getElementById('practiceWrap'); let html='';
  mods.forEach(m=>{
    html+='<h2 class="pm">'+m.name+' <span>('+m.weight+')</span></h2>';
    m.points.forEach(p=>{
      const ex=p.exam; const isReal=!ex.src.startsWith('命卷视角');
      html+='<div class="pc"><h3>'+p.name+'</h3>';
      html+='<p class="pe"><b>细分：</b>'+p.sub.join('；')+'</p>';
      html+='<div class="pex '+(isReal?'real':'typ')+'"><b>真题('+(isReal?'真实':'仿真')+') '+ex.src+'</b> ［'+ex.tag+'］<br>'+ex.q+'<br><i>答：'+ex.a+'</i><br><i>命卷提示：'+ex.note+'</i></div>';
      html+='<p class="pe"><b>易错：</b>'+p.pit.join('；')+'</p>';
      html+='<p class="pe"><b>易混：</b>'+p.con.join('；')+'</p>';
      html+='<p class="pe"><b>妙法：</b>'+p.tip+'</p></div>';
    });
  });
  wrap.innerHTML=html;
}

// ---------- 初始化 ----------
renderNav();
buildPractice();
showTab('detail');
const fm=mods[0];
showPoint(fm, fm.points[0]);
document.querySelectorAll('.pt')[0].classList.add('sel');
</script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__VER__", VER)
       .replace("__SVG__", svg_inline)
       .replace("__DATA__", data_json)
       .replace("__TRAP__", trap_json)
       .replace("__DEMOS__", demos_block)
       .replace("__RUNDEMO__", run_demo_fn))

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(out)
print("单文件已生成:", OUT_HTML, "大小:", os.path.getsize(OUT_HTML), "字节")

# ---------- 6) 打包 zip ----------
if os.path.exists(OUT_ZIP):
    os.remove(OUT_ZIP)
with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(OUT_HTML, os.path.basename(OUT_HTML))
print("zip 已生成:", OUT_ZIP)
