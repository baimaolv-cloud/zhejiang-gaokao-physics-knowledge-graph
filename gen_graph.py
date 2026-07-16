#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成浙江新高考物理知识图谱 (SVG + 交互 HTML)"""
import os, html

OUT = "/Users/mac/WorkBuddy/2026-07-16-08-20-32"
W = 680
H = 1320

modules = [
    {"name":"力学","en":"Mechanics","color":"#2563eb","weight":"约 40%  ·  压舱石","side":"L","points":[
        "运动的描述","匀变速直线运动","相互作用与力","牛顿运动定律",
        "曲线运动（平抛·圆周）","万有引力与航天","机械能守恒定律","动量守恒定律"]},
    {"name":"电磁学","en":"Electromagnetism","color":"#db2777","weight":"约 35%  ·  压舱石","side":"L","points":[
        "静电场","恒定电流","磁场","电磁感应","交变电流","电磁波"]},
    {"name":"热学","en":"Thermal","color":"#ea580c","weight":"约 10%","side":"L","points":[
        "分子动理论","气体实验定律（玻意耳/查理/盖·吕萨克）","热力学定律"]},
    {"name":"光学","en":"Optics","color":"#16a34a","weight":"约 7%","side":"R","points":[
        "几何光学（折射·全反射·透镜）","物理光学（干涉·衍射·偏振）"]},
    {"name":"原子物理与近代物理","en":"Atomic & Modern","color":"#7c3aed","weight":"约 8%","side":"R","points":[
        "原子结构（玻尔模型）","原子核（衰变·裂变·聚变）","波粒二象性","相对论简介"]},
    {"name":"实验探究","en":"Experiments","color":"#0891b2","weight":"贯穿全卷 · 约 15 分","side":"R","points":[
        "力学实验（纸带·验证定律）","电学实验（伏安法·电表改装）","热学·光学实验","探究性 / 设计性实验"]},
]

rows = [200, 560, 920]
panel_w = 312
left_x, right_x = 16, 352
root_x, root_y, root_h = 340, 64, 48

left_mod  = [m for m in modules if m["side"]=="L"]
right_mod = [m for m in modules if m["side"]=="R"]
for i,m in enumerate(left_mod):  m["row"], m["x"] = rows[i], left_x
for i,m in enumerate(right_mod): m["row"], m["x"] = rows[i], right_x
for m in modules:
    m["h"] = max(150, 64 + len(m["points"])*34 + 14)

def esc(s): return html.escape(str(s), quote=True)

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="\'PingFang SC\',\'Microsoft YaHei\',sans-serif">')
svg.append('''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f8fafc"/><stop offset="1" stop-color="#eef2f7"/>
  </linearGradient>
  <linearGradient id="rootg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#334155"/>
  </linearGradient>
  <filter id="sh" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.18"/>
  </filter>
</defs>''')
svg.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# 标题
svg.append(f'<text x="{root_x}" y="34" text-anchor="middle" font-size="22" font-weight="800" fill="#0f172a">浙江新高考 · 物理知识图谱</text>')
svg.append(f'<text x="{root_x}" y="52" text-anchor="middle" font-size="12" fill="#64748b">命卷人视角 · 浙教版必修 + 选择性必修 · 分值权重参考近年真题</text>')

# 根节点
rx, ry = root_x-110, root_y
svg.append(f'<g filter="url(#sh)"><rect x="{rx}" y="{ry}" width="220" height="{root_h}" rx="14" fill="url(#rootg)"/>'
           f'<text x="{root_x}" y="{ry+31}" text-anchor="middle" font-size="17" font-weight="800" fill="#fff">高中物理 知识体系</text></g>')
root_bot = ry + root_h

# 连接线 + 面板
for m in modules:
    cx = m["x"] + panel_w/2
    top = m["row"]
    # 连接曲线：根 -> 面板顶部中心
    my = (root_bot + top) / 2
    svg.append(f'<path d="M {root_x} {root_bot} C {root_x} {my}, {cx} {my}, {cx} {top}" '
               f'fill="none" stroke="{m["color"]}" stroke-width="2.2" stroke-opacity="0.55" stroke-linecap="round"/>')
    # 面板
    px, py, pw, ph = m["x"], m["row"], panel_w, m["h"]
    svg.append(f'<g class="module" filter="url(#sh)">')
    svg.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="#ffffff" stroke="{m["color"]}" stroke-width="1.5"/>')
    # 标题栏
    svg.append(f'<rect x="{px}" y="{py}" width="{pw}" height="42" rx="14" fill="{m["color"]}"/>')
    svg.append(f'<rect x="{px}" y="{py+21}" width="{pw}" height="21" fill="{m["color"]}"/>')
    svg.append(f'<text x="{px+16}" y="{py+27}" font-size="16" font-weight="800" fill="#fff">{esc(m["name"])}</text>')
    svg.append(f'<text x="{px+pw-12}" y="{py+27}" text-anchor="end" font-size="11" fill="#fff" fill-opacity="0.92">{esc(m["en"])}</text>')
    # 权重徽标
    svg.append(f'<rect x="{px+10}" y="{py+52}" width="{pw-20}" height="22" rx="11" fill="{m["color"]}" fill-opacity="0.12"/>')
    svg.append(f'<text x="{px+pw/2}" y="{py+68}" text-anchor="middle" font-size="12" font-weight="700" fill="{m["color"]}">{esc(m["weight"])}</text>')
    # 知识点
    yy = py + 96
    for p in m["points"]:
        svg.append(f'<circle cx="{px+20}" cy="{yy-4}" r="3.4" fill="{m["color"]}"/>')
        svg.append(f'<text x="{px+32}" y="{yy}" font-size="13" fill="#1e293b">{esc(p)}</text>')
        yy += 34
    svg.append('</g>')

# 页脚命卷说明
fy = H - 36
svg.append(f'<line x1="20" y1="{fy-18}" x2="{W-20}" y2="{fy-18}" stroke="#cbd5e1" stroke-width="1"/>')
svg.append(f'<text x="350" y="{fy}" text-anchor="middle" font-size="12" fill="#475569">物理为浙江"7选3"选考科目之一 · 试卷覆盖必修+选择性必修全部内容 · 实验题必考（力/电实验为核心区分度来源）</text>')
svg.append('</svg>')

svg_str = "\n".join(svg)
with open(os.path.join(OUT,"physics_knowledge_graph.svg"),"w",encoding="utf-8") as f:
    f.write(svg_str)

# 交互 HTML：复用同一 SVG，外裹平移/缩放 + 悬浮高亮
html_doc = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>浙江新高考物理知识图谱</title>
<style>
  html,body{{margin:0;height:100%;background:#0f172a;font-family:'PingFang SC','Microsoft YaHei',sans-serif;overflow:hidden}}
  #wrap{{width:100vw;height:100vh;display:flex;align-items:center;justify-content:center}}
  svg{{width:100%;height:100%;cursor:grab;touch-action:none}}
  svg:active{{cursor:grabbing}}
  .module{{transition:opacity .2s, transform .2s;transform-box:fill-box;transform-origin:center}}
  .module:hover{{opacity:1!important}}
  .module{{opacity:.97}}
  #hint{{position:fixed;left:16px;bottom:14px;color:#94a3b8;font-size:12px;background:rgba(15,23,42,.6);padding:6px 10px;border-radius:8px}}
</style></head><body>
<div id="wrap">{svg_str}</div>
<div id="hint">滚轮缩放 · 拖拽平移 · 悬停模块查看权重</div>
<script>
  const svg=document.querySelector('svg');
  const vp=svg; let scale=1,tx=0,ty=0,panning=false,sx=0,sy=0;
  function apply(){{svg.style.transform=`translate(${{tx}}px,${{ty}}px) scale(${{scale}})`;svg.style.transformOrigin='0 0';}}
  svg.addEventListener('wheel',e=>{{e.preventDefault();const f=e.deltaY<0?1.12:1/1.12;scale=Math.min(4,Math.max(.4,scale*f));apply();}},{{passive:false}});
  svg.addEventListener('mousedown',e=>{{panning=true;sx=e.clientX-tx;sy=e.clientY-ty;}});
  addEventListener('mousemove',e=>{{if(!panning)return;tx=e.clientX-sx;ty=e.clientY-sy;apply();}});
  addEventListener('mouseup',()=>panning=false);
  // 触摸
  svg.addEventListener('touchstart',e=>{{if(e.touches.length===1){{panning=true;sx=e.touches[0].clientX-tx;sy=e.touches[0].clientY-ty;}}}},{{passive:true}});
  svg.addEventListener('touchmove',e=>{{if(panning&&e.touches.length===1){{tx=e.touches[0].clientX-sx;ty=e.touches[0].clientY-sy;apply();}}}},{{passive:true}});
  svg.addEventListener('touchend',()=>panning=false);
</script></body></html>'''
with open(os.path.join(OUT,"physics_knowledge_graph.html"),"w",encoding="utf-8") as f:
    f.write(html_doc)

print("OK", os.path.getsize(os.path.join(OUT,"physics_knowledge_graph.svg")), "bytes svg")
print("OK", os.path.getsize(os.path.join(OUT,"physics_knowledge_graph.html")), "bytes html")
