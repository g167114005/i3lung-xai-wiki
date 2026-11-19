#!/usr/bin/env python3
"""把 wiki/ 轉成可瀏覽的靜態網頁（wiki-site/）並產生首頁 index.html，供 GitHub Pages 使用。
只做格式轉換，不改內容。用法：python tools/build_site.py（需要 pip install markdown）"""
import os, re, glob, html, markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/g167114005/i3lung-xai-wiki"
DOI = "https://doi.org/10.1038/s41591-026-04488-2"
CSS = """:root{--bg:#F6F3EC;--ink:#1A2331;--mut:#5A6475;--rule:#D8D2C5;--acc:#8E2A2A;--warn:#B3432A;--card:#FFFDF8}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.8 "Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif}
header{border-bottom:1px solid var(--rule);background:var(--card)}header div,main{max-width:860px;margin:0 auto;padding:14px 24px}
header a{margin-right:18px;font-weight:600}main{padding-top:28px;padding-bottom:80px}a{color:var(--acc)}
h1{font-size:30px;line-height:1.3;margin:.2em 0 .6em}h2{font-size:21px;margin:1.8em 0 .5em;padding-bottom:4px;border-bottom:2px solid var(--rule)}h3{font-size:18px;margin:1.4em 0 .3em}
table{border-collapse:collapse;width:100%;font-size:15px;margin:1em 0;display:block;overflow-x:auto}th,td{border:1px solid var(--rule);padding:6px 10px;text-align:left;vertical-align:top}th{background:var(--card)}
img{max-width:100%;height:auto;display:block;margin:16px 0 4px;border:1px solid var(--rule);border-radius:6px;background:#fff}
.meta{font-size:14px;color:var(--mut);background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:10px 16px;margin-bottom:8px}.meta b{color:var(--ink)}
.cite{font:12.5px ui-monospace,Consolas,monospace;color:var(--mut);background:var(--card);border:1px solid var(--rule);border-radius:4px;padding:0 5px;white-space:nowrap}
blockquote{margin:1em 0;padding:8px 16px;border-left:4px solid var(--warn);background:var(--card)}code{background:var(--card);border:1px solid var(--rule);border-radius:4px;padding:0 4px;font-size:.9em}
figure{margin:20px 0}figcaption{font-size:14px;color:var(--mut)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:24px 0}.cards a{display:block;background:var(--card);border:1px solid var(--rule);border-top:5px solid var(--acc);border-radius:8px;padding:18px 20px;text-decoration:none;color:var(--ink)}
.cards b{display:block;font-size:20px;color:var(--acc);margin-bottom:4px}.cards span{font-size:15px;color:var(--mut)}
@media (max-width:600px){body{font-size:16px}h1{font-size:25px}header div,main{padding-left:16px;padding-right:16px}}"""


def page(title, body, up=""):
    nav = (f'<header><div><a href="{up}index.html">首頁</a><a href="{up}wiki-site/story.html">三分鐘看懂</a>'
           f'<a href="{up}wiki-site/index.html">Wiki 目錄</a><a href="{REPO}">GitHub</a></div></header>')
    return (f'<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>'
            f'<style>{CSS}</style></head><body>{nav}<main>{body}</main></body></html>')


def main():
    out = os.path.join(ROOT, "wiki-site"); os.makedirs(out, exist_ok=True)
    files = {os.path.splitext(os.path.basename(p))[0]: p
             for p in glob.glob(os.path.join(ROOT, "wiki", "**", "*.md"), recursive=True)}
    titles = {}
    for name, p in files.items():
        text = open(p, encoding="utf-8").read()
        m = re.search(r"^title:\s*(.+)$", text, re.M)
        titles[name] = m.group(1).strip() if m else name
    for name, p in files.items():
        text = open(p, encoding="utf-8").read(); meta = ""
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if m:
            kv = [l.split(":", 1) for l in m.group(1).splitlines() if ":" in l]
            shown = [(k.strip(), v.strip()) for k, v in kv if k.strip() not in ("title", "type")]
            if shown:
                meta = '<div class="meta">' + "　".join(f"<b>{html.escape(k)}</b> {html.escape(v)}" for k, v in shown) + "</div>"
            text = text[m.end():]
        text = re.sub(r"\[\[([^\]]+)\]\]",
                      lambda x: f"[{titles.get(x.group(1), x.group(1)).split('：')[0]}]({x.group(1)}.html)" if x.group(1) in files else x.group(1),
                      text)
        text = re.sub(r"\[([a-z0-9]+), (p\.\d+)\]", r'<span class="cite">\1 \2</span>', text)
        body = markdown.markdown(text, extensions=["tables", "sane_lists"])
        body = re.sub(r'<p><img alt="([^"]*)" src="([^"]*)" ?/?></p>',
                      r'<figure><img alt="\1" src="\2"><figcaption>\1</figcaption></figure>', body)
        h1 = re.search(r"<h1>(.*?)</h1>", body, re.S)
        open(os.path.join(out, name + ".html"), "w", encoding="utf-8").write(
            page(re.sub("<.*?>", "", h1.group(1)) if h1 else name, meta + body, "../"))
    n = len(files) - 2
    home = f"""<h1>AI 能幫醫師判斷誰適合免疫治療嗎？</h1>
<p>一篇 Nature Medicine 論文的白話 Wiki｜北醫 G167114005 醫學院人工智慧醫療碩士在職專班 碩二 鄭為遠</p>
<p>論文：Prelaj A, et al. <i>Clinical usability of an explainable AI decision support tool and evaluation of multimodal models in NSCLC.</i>
Nature Medicine 2026;32:3235–3247（2025 JIF 52.5；CC BY 4.0）。<a href="{DOI}">原文連結</a></p>
<p>這個網站寫給<b>沒有醫學背景的人</b>：先用三分鐘看懂整個故事，再依需要點進名詞與議題。每個數字都標到原文 PDF 的頁碼，可以回查。</p>
<div class="cards">
<a href="wiki-site/story.html"><b>三分鐘看懂</b><span>這篇研究在做什麼、發現了什麼、為什麼重要，不用術語。</span></a>
<a href="wiki-site/prelaj2026.html"><b>論文頁</b><span>研究設計、模型與結果、XAI 怎麼做，以及報告者的評讀。</span></a>
<a href="wiki-site/index.html"><b>Wiki 目錄</b><span>{n} 頁：導讀、論文頁、12 個觀念頁、4 個議題頁。</span></a>
<a href="wiki-site/automation-bias.html"><b>最反直覺的發現</b><span>自動化偏誤：專家反而更容易被錯誤的 AI 建議帶著走。</span></a>
<a href="{REPO}/blob/main/AGENTS.md"><b>AGENTS.md</b><span>建 wiki 的規則：給誰看、出處到頁碼、數字可回查、評讀與原文分開寫。</span></a>
<a href="{REPO}/blob/main/tools/lint.py"><b>自動檢查</b><span>lint.py 逐行檢查：含數字的句子都要有出處，數字要能在該頁 PDF 找到。</span></a>
</div>
<p style="color:var(--mut);font-size:15px">圖片取自原文（CC BY 4.0）。期刊影響因子不在原文中，請以 Clarivate JCR 核對。建置紀錄見 <a href="wiki-site/log.html">log</a>。</p>"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page("I3LUNG 白話 Wiki", home))
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    print("wiki-site:", len(files), "頁；index.html")


if __name__ == "__main__":
    main()
