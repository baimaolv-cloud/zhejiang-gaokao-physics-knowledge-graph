# -*- coding: utf-8 -*-
import os, re, html, shutil, zipfile

BASE = "/Users/mac/WorkBuddy/2026-07-16-08-20-32"
SRC = {
    "graph": os.path.join(BASE, "physics_knowledge_graph.html"),
    "detailed": os.path.join(BASE, "physics_detailed_graph.html"),
    "demos": os.path.join(BASE, "physics_demos.html"),
    "practice_md": os.path.join(BASE, "physics_practice.md"),
}
OFFLINE = os.path.join(BASE, "物理知识图谱_离线版")
STANDALONE = os.path.join(BASE, "物理知识图谱_单机版")

VER = "v1.1"
TITLE = "浙江新高考物理 · 考点知识图谱系统"

# ---------- 轻量 Markdown -> HTML ----------
def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return text

def md_to_html(md):
    lines = md.split("\n")
    out = []
    in_ul = in_ol = False
    def close():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>"); in_ul = False
        if in_ol:
            out.append("</ol>"); in_ol = False
    for s in lines:
        s = s.rstrip()
        if not s.strip():
            close(); continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            close()
            lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, inline(m.group(2)), lv))
            continue
        if s.startswith(">"):
            close()
            out.append("<blockquote>%s</blockquote>" % inline(s[1:].strip()))
            continue
        if re.match(r"^-{3,}$", s.strip()):
            close(); out.append("<hr/>"); continue
        m = re.match(r"^(\d+)\.\s+(.*)", s)
        if m:
            if not in_ol:
                close(); out.append("<ol>"); in_ol = True
            out.append("<li>%s</li>" % inline(m.group(2))); continue
        if re.match(r"^[-*]\s+", s):
            if not in_ul:
                close(); out.append("<ul>"); in_ul = True
            out.append("<li>%s</li>" % inline(s[2:].strip())); continue
        close()
        out.append("<p>%s</p>" % inline(s))
    close()
    return "\n".join(out)

PRACTICE_CSS = """body{font-family:'PingFang SC','Microsoft YaHei',sans-serif;max-width:920px;margin:0 auto;padding:28px 22px;color:#1e293b;background:#fff;line-height:1.85;font-size:15px}
h1{font-size:24px;border-bottom:3px solid #2563eb;padding-bottom:10px;color:#1e40af;margin-bottom:6px}
h2{font-size:19px;color:#1d4ed8;margin-top:34px;border-left:5px solid #2563eb;padding-left:12px;background:#f8fafc;padding:8px 12px}
h3{font-size:16px;color:#0f766e;margin-top:22px}
blockquote{background:#f1f5f9;border-left:4px solid #94a3b8;margin:10px 0;padding:8px 16px;color:#475569;border-radius:0 6px 6px 0}
ul,ol{padding-left:24px} li{margin:5px 0}
b{color:#b91c1c} hr{border:none;border-top:1px solid #e2e8f0;margin:20px 0}
.tip{color:#0369a1}"""

def practice_html():
    md = open(SRC["practice_md"], encoding="utf-8").read()
    body = md_to_html(md)
    return ("<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>真题练习册 · " + TITLE + "</title><style>" + PRACTICE_CSS +
            "</style></head><body>" + body +
            "<hr><p style=\"color:#64748b;font-size:13px\">命卷人视角 · 离线单机版 " + VER +
            " · 本页由 Markdown 自动转换，无需联网即可阅读</p></body></html>")

# ---------- 离线使用说明页 ----------
OFFLINE_README = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>离线版使用说明 · __TITLE__</title>
<style>body{font-family:'PingFang SC','Microsoft YaHei',sans-serif;max-width:720px;margin:0 auto;padding:32px 24px;color:#1e293b;line-height:1.9}
h1{color:#1e40af;border-bottom:3px solid #2563eb;padding-bottom:10px}
.card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;margin:14px 0}
.card b{color:#0f766e}.warn{background:#fff7ed;border-color:#fed7aa;color:#9a3412}
code{background:#1e293b;color:#e2e8f0;padding:2px 8px;border-radius:5px;font-size:13px}
</style></head><body>
<h1>__TITLE__ · 离线版使用说明</h1>
<p>本文件夹为<strong>完全离线、零依赖</strong>交付包。所有 HTML 均内联资源，<strong>断网状态双击即可使用</strong>，无需安装任何软件、无需联网、不请求任何外部网络地址。</p>
<div class="card"><b>📁 文件清单</b><br>
• <code>knowledge-graph.html</code> —— 知识图谱总览（6 大模块 → 27 考点，含分值权重）<br>
• <code>detailed-graph.html</code> —— 考点细化与真题体系（细分 + 真题 + 易错/易混/妙法 + 动态演示）<br>
• <code>demos.html</code> —— 课堂演示版（纯仿真，投屏用）<br>
• <code>practice.html</code> —— 真题练习册（离线可读）<br>
• <code>index.html</code> —— 离线版首页（入口导航）<br>
• <code>离线使用说明.html</code> —— 使用说明</div>
<div class="card warn"><b>⚠ 使用提示</b><br>
1. 直接用浏览器（Chrome / Edge / Safari）打开上述任一 <code>.html</code> 文件即可；<br>
2. 动态演示需浏览器支持 JavaScript（默认开启）；<br>
3. 拷贝整个文件夹到任意电脑 / U 盘均可运行，<strong>请勿单文件剪切</strong>（演示与练习册为独立文件）；<br>
4. 本版不依赖网络，适合无网考场、临时授课机、外出讲评。</div>
<p style="color:#64748b;font-size:13px">版本 __VER__ · 杭州白毛驴爱科科技 · 命卷人视角出品</p>
</body></html>"""

# ---------- 离线版：首页 index.html（扁平链接） ----------
OFFLINE_INDEX_HTML = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · 离线版首页</title>
<style>
body{font-family:'PingFang SC','Microsoft YaHei',sans-serif;margin:0;background:#0f172a;color:#e2e8f0}
header{background:linear-gradient(120deg,#1e3a8a,#0f766e);color:#fff;padding:30px 26px}
header h1{margin:0 0 6px;font-size:24px} header p{margin:0;opacity:.9}
main{max-width:900px;margin:0 auto;padding:24px 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin:16px 0}
.mod{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:18px;text-decoration:none;color:#e2e8f0;display:block;transition:.15s}
.mod:hover{transform:translateY(-3px);box-shadow:0 8px 22px rgba(0,0,0,.35);border-color:#38bdf8}
.mod h3{margin:0 0 6px;color:#38bdf8} .mod p{margin:0;font-size:13px;color:#94a3b8;line-height:1.7}
.sec{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:16px 20px;margin:16px 0}
.sec h2{margin-top:0;color:#2dd4bf;font-size:17px}
code{background:#0f172a;color:#e2e8f0;padding:2px 7px;border-radius:5px;font-size:12px}
footer{text-align:center;color:#64748b;font-size:12px;padding:18px}
</style></head><body>
<header><h1>__TITLE__ · 离线版</h1><p>命卷人视角 · 完全离线 / 零依赖 · 断网双击即用 · 版本 __VER__</p></header>
<main>
<div class="grid">
<a class="mod" href="knowledge-graph.html"><h3>① 知识图谱总览</h3><p>6 大模块 → 27 主考点两级结构，标注分值权重。</p></a>
<a class="mod" href="detailed-graph.html"><h3>② 考点细化与真题体系</h3><p>27 考点 · 123 细分 · 每点配真实浙江真题 + 易错/易混/妙法 + 动态演示。</p></a>
<a class="mod" href="demos.html"><h3>③ 课堂演示版</h3><p>纯仿真投屏页，按模块铺开 27 考点动态演示，含命题陷阱。</p></a>
<a class="mod" href="practice.html"><h3>④ 真题练习册</h3><p>离线可读练习册，可打印 / 组卷。</p></a>
</div>
<div class="sec"><h2>使用说明</h2>
<p>1. 本文件夹为<strong>完全离线交付包</strong>，断网双击任一 <code>.html</code> 即可；<br>
2. 动态演示依赖浏览器 JavaScript（默认开启）；<br>
3. 建议<strong>整文件夹拷贝</strong>到 U 盘 / 任意电脑，请勿单文件剪切。</p></div>
<p class="sec" style="margin:0"><a class="mod" href="离线使用说明.html" style="text-decoration:none"><h2 style="margin:0">📖 查看离线使用说明</h2></a></p>
</main>
<footer>杭州白毛驴爱科科技 · 命卷人视角出品 · 仅供教研与教学使用</footer>
</body></html>"""

# ---------- 单机版：产品首页 index.html ----------
INDEX_HTML = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ · 产品首页</title>
<style>
body{font-family:'PingFang SC','Microsoft YaHei',sans-serif;margin:0;background:#f1f5f9;color:#1e293b}
header{background:linear-gradient(120deg,#1e3a8a,#0f766e);color:#fff;padding:34px 28px}
header h1{margin:0 0 6px;font-size:26px} header p{margin:0;opacity:.9}
main{max-width:980px;margin:0 auto;padding:26px 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:18px 0}
.mod{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px;text-decoration:none;color:inherit;display:block;transition:.15s}
.mod:hover{transform:translateY(-3px);box-shadow:0 8px 22px rgba(0,0,0,.1);border-color:#2563eb}
.mod h3{margin:0 0 6px;color:#1d4ed8} .mod p{margin:0;font-size:13px;color:#64748b;line-height:1.7}
.sec{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px 22px;margin:18px 0}
.sec h2{margin-top:0;color:#0f766e;font-size:18px}
code{background:#1e293b;color:#e2e8f0;padding:2px 7px;border-radius:5px;font-size:12px}
footer{text-align:center;color:#64748b;font-size:12px;padding:20px}
</style></head><body>
<header><h1>__TITLE__</h1><p>命卷人视角 · 离线单机产品 · 版本 __VER__ · 完全离线 / 零依赖 / 可二次开发</p></header>
<main>
<div class="grid">
<a class="mod" href="modules/knowledge-graph.html"><h3>① 知识图谱总览</h3><p>6 大模块 → 27 主考点两级结构，标注分值权重，全局把握命题重心。</p></a>
<a class="mod" href="modules/detailed-graph.html"><h3>② 考点细化与真题体系</h3><p>27 考点 · 123 细分 · 每点配真题（27 道真实浙江选考真题）+ 易错/易混/妙法 + 动态演示。</p></a>
<a class="mod" href="modules/demos.html"><h3>③ 课堂演示版</h3><p>纯仿真投屏页，按模块铺开 27 考点动态演示，含命题陷阱浮层。</p></a>
<a class="mod" href="docs/practice.html"><h3>④ 真题练习册</h3><p>同体系可打印 / 组卷文字版，离线可读。</p></a>
</div>
<div class="sec"><h2>使用说明</h2>
<p>1. 双击 <code>index.html</code> 进入本首页，点击上方卡片打开对应模块；<br>
2. 所有模块均为<strong>自包含 HTML</strong>，断网可用，无需服务器；<br>
3. 动态演示依赖浏览器 JavaScript（默认开启）；<br>
4. 二次开发：<code>modules/</code> 放三大交互页，<code>docs/</code> 放练习册与文档，源数据在 <code>gen_detailed.py</code> 中维护。</p></div>
<div class="sec"><h2>版本与更新</h2>
<p>当前版本 <code>__VER__</code>。详细变更见 <code>docs/CHANGELOG.md</code>。<br>
核心能力：知识图谱 → 考点细化 → 易错易混妙法 → 动态演示 → 真题练习，五层递进。</p></div>
</main>
<footer>杭州白毛驴爱科科技 · 命卷人视角出品 · 本产品仅供教研与教学使用</footer>
</body></html>"""

README_MD = """# __TITLE__ · 单机文件夹版

> 命卷人视角出品 · 版本 __VER__ · 完全离线 / 零依赖

## 产品定位
面向浙江新高考物理命卷与教学的<strong>考点知识图谱系统</strong>。五层能力递进：
**知识图谱 → 考点细化 → 易错/易混/妙法 → 动态演示 → 真题练习**。

## 目录结构
```
物理知识图谱_单机版/
├── index.html            # 产品首页（入口导航）
├── README.md             # 本文件
├── modules/              # 三大交互模块（自包含 HTML）
│   ├── knowledge-graph.html   # 知识图谱总览
│   ├── detailed-graph.html    # 考点细化与真题体系
│   └── demos.html             # 课堂演示版
└── docs/                 # 文档与资料
    ├── practice.html         # 真题练习册（离线可读）
    ├── practice.md            # 真题练习册（Markdown 源）
    └── CHANGELOG.md           # 版本变更日志
```

## 使用方式
- 双击 `index.html` 打开产品首页，点击卡片进入各模块；
- 全部模块断网可用，无需联网、无需安装；
- 动态演示需浏览器启用 JavaScript。

## 适用场景
- 教研组长期归档与版本管理；
- 二次编辑（源数据在 `gen_detailed.py` 中维护，重跑即重建）；
- 团队离线分发与讲评投屏。

## 版权
杭州白毛驴爱科科技 · 命卷人视角。仅供教研与教学使用，禁止未经授权的商业转售。
"""

CHANGELOG_MD = """# 变更日志 · __TITLE__

## __VER__ （本次交付）
- 初始交付，含两套打包形态：
  - **离线版**：扁平文件夹，断网即开即用，练习册转 HTML 离线可读；
  - **单机文件夹版**：结构化目录（index 首页 + modules + docs + README + CHANGELOG），便于归档与二次开发。
- 五层能力：知识图谱总览 / 考点细化（27 考点·123 细分）/ 易错易混妙法 / 动态演示（25 种仿真，真实量纲 + 命题陷阱浮层）/ 真题练习（27 道真实浙江选考真题）。
"""

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def zip_folder(folder, zip_path):
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder):
            for fn in sorted(files):
                fp = os.path.join(root, fn)
                z.write(fp, os.path.relpath(fp, folder))

def build():
    # ===== 离线版 =====
    os.makedirs(OFFLINE, exist_ok=True)
    shutil.copy(SRC["graph"], os.path.join(OFFLINE, "knowledge-graph.html"))
    shutil.copy(SRC["detailed"], os.path.join(OFFLINE, "detailed-graph.html"))
    shutil.copy(SRC["demos"], os.path.join(OFFLINE, "demos.html"))
    write_file(os.path.join(OFFLINE, "practice.html"), practice_html())
    write_file(os.path.join(OFFLINE, "index.html"),
               OFFLINE_INDEX_HTML.replace("__TITLE__", TITLE).replace("__VER__", VER))
    write_file(os.path.join(OFFLINE, "离线使用说明.html"),
               OFFLINE_README.replace("__TITLE__", TITLE).replace("__VER__", VER))

    # ===== 单机文件夹版 =====
    mod_dir = os.path.join(STANDALONE, "modules")
    doc_dir = os.path.join(STANDALONE, "docs")
    os.makedirs(mod_dir, exist_ok=True)
    os.makedirs(doc_dir, exist_ok=True)
    shutil.copy(SRC["graph"], os.path.join(mod_dir, "knowledge-graph.html"))
    shutil.copy(SRC["detailed"], os.path.join(mod_dir, "detailed-graph.html"))
    shutil.copy(SRC["demos"], os.path.join(mod_dir, "demos.html"))
    write_file(os.path.join(doc_dir, "practice.html"), practice_html())
    shutil.copy(SRC["practice_md"], os.path.join(doc_dir, "practice.md"))
    write_file(os.path.join(STANDALONE, "index.html"),
               INDEX_HTML.replace("__TITLE__", TITLE).replace("__VER__", VER))
    write_file(os.path.join(STANDALONE, "README.md"),
               README_MD.replace("__TITLE__", TITLE).replace("__VER__", VER))
    write_file(os.path.join(doc_dir, "CHANGELOG.md"),
               CHANGELOG_MD.replace("__TITLE__", TITLE).replace("__VER__", VER))

    print("离线版 ->", OFFLINE)
    print("单机版 ->", STANDALONE)
    zip_folder(OFFLINE, OFFLINE + ".zip")
    zip_folder(STANDALONE, STANDALONE + ".zip")
    print("离线版 zip ->", OFFLINE + ".zip")
    print("单机版 zip ->", STANDALONE + ".zip")
    for d in (OFFLINE, STANDALONE):
        for root, _, files in os.walk(d):
            for fn in sorted(files):
                p = os.path.join(root, fn)
                print("  %s  (%d bytes)" % (os.path.relpath(p, BASE), os.path.getsize(p)))

if __name__ == "__main__":
    build()
