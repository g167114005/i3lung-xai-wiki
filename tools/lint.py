#!/usr/bin/env python3
"""Wiki lint：出處完整、數字可回查、連結與索引、格式一致。
（改寫自第 10 週作業 xai-stroke-llm-wiki 的 tools/lint.py；本專案只有一份來源，不使用 review。）
用法：python tools/lint.py [--quiet]    （在專案根目錄執行）
需要：pdftotext（poppler）或 pypdf。結束碼 0 = 全過；1 = 有錯。
"""
import csv, os, re, subprocess, sys, shutil, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")
RAW = os.path.join(ROOT, "raw")
CACHE = os.path.join(ROOT, ".cache", "pages")

REQUIRED = {
    "paper": (["type", "title", "key", "year", "journal", "source_file"],
              ["一句話", "研究設計", "模型與結果", "XAI 怎麼做", "報告者的評讀", "相關頁面"]),
    "guide": (["type", "title"], ["一句話", "相關頁面"]),
    "concept": (["type", "title"], ["白話解釋", "在這篇論文怎麼用", "相關頁面"]),
    "issue": (["type", "title"], ["問題是什麼", "證據", "報告者的看法", "相關頁面"]),
}
CITE = re.compile(r"\[([a-z0-9]+),\s*p\.(\d+)\]")
LINK = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]")
NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")


def norm(s):
    for a in "‐‑‒–—−­":
        s = s.replace(a, "-")
    s = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", s)   # 千分位逗號：2,396 → 2396
    return re.sub(r"\s+", " ", s)


def load_sources():
    with open(os.path.join(ROOT, "sources.csv"), encoding="utf-8") as f:
        return {r["key"]: r["file"] for r in csv.DictReader(f)}


def pdf_pages(key, fn):
    d = os.path.join(CACHE, key)
    if not os.path.isdir(d) or not os.listdir(d):
        os.makedirs(d, exist_ok=True)
        path = os.path.join(RAW, fn)
        if shutil.which("pdftotext") and shutil.which("pdfinfo"):
            info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
            n = int(re.search(r"Pages:\s+(\d+)", info).group(1))
            for i in range(1, n + 1):
                t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), path, "-"],
                                   capture_output=True, text=True).stdout
                open(os.path.join(d, f"p{i:03d}.txt"), "w", encoding="utf-8").write(t)
        else:
            from pypdf import PdfReader
            for i, pg in enumerate(PdfReader(path).pages, 1):
                open(os.path.join(d, f"p{i:03d}.txt"), "w", encoding="utf-8").write(pg.extract_text() or "")
    return {int(os.path.basename(p)[1:4]): norm(open(p, encoding="utf-8").read())
            for p in sorted(glob.glob(os.path.join(d, "p*.txt")))}


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1); fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def numbers(line):
    s = CITE.sub(" ", line)
    s = LINK.sub(" ", s)
    s = re.sub(r"`[^`]*`", " ", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)        # 圖片語法不檢查
    out = []
    for m in NUM.finditer(s):
        n = m.group(0).rstrip(",").replace(",", "")
        if "." not in n and len(n) < 2:
            continue                      # 個位數不檢查
        if re.fullmatch(r"(19|20)\d\d", n):
            continue                      # 年份不檢查
        out.append(n)
    return out


def found(n, text):
    return re.search(r"(?<![\d.])" + re.escape(n) + r"(?!\d)", text) is not None


def main():
    quiet = "--quiet" in sys.argv
    src = load_sources()
    errs = []
    pages = {os.path.splitext(os.path.basename(p))[0]: p
             for p in glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True)}
    cache_pdf = {}
    inlinks = {k: set() for k in pages}
    stats = dict(pages=len(pages), cites=0, numbers=0)

    for name, path in sorted(pages.items()):
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        fm, body = frontmatter(open(path, encoding="utf-8").read())
        special = name in ("index", "log")
        if not special:
            typ = fm.get("type")
            if typ not in REQUIRED:
                errs.append(f"[格式] {rel}: frontmatter 缺少或不認得 type")
            else:
                f_req, s_req = REQUIRED[typ]
                for f in f_req:
                    if not fm.get(f):
                        errs.append(f"[格式] {rel}: frontmatter 缺 {f}")
                heads = [h.strip() for h in re.findall(r"^## (.+)$", body, re.M)]
                for s in s_req:
                    if s not in heads:
                        errs.append(f"[格式] {rel}: 缺小節「{s}」")
                if typ == "paper" and fm.get("key") != name:
                    errs.append(f"[格式] {rel}: key 與檔名不同")
        for m in LINK.finditer(body):
            t = m.group(1).strip()
            if t not in pages:
                errs.append(f"[連結] {rel}: 斷鏈 [[{t}]]")
            elif t != name:
                inlinks[t].add(name)
        if special:
            continue
        for i, line in enumerate(body.splitlines(), 1):
            s = line.strip()
            if not s or s.startswith("#") or re.fullmatch(r"[|\-: ]+", s):
                continue
            cites = list(CITE.finditer(s))
            nums = numbers(s)
            stats["cites"] += len(cites)
            texts = []
            for c in cites:
                key, pg = c.group(1), int(c.group(2))
                if key not in src:
                    errs.append(f"[出處] {rel}:{i}: 來源代號不存在 {key}"); continue
                if key not in cache_pdf:
                    cache_pdf[key] = pdf_pages(key, src[key])
                if pg not in cache_pdf[key]:
                    errs.append(f"[出處] {rel}:{i}: {key} 沒有第 {pg} 頁"); continue
                texts.append(cache_pdf[key][pg])
            if nums and not cites:
                errs.append(f"[出處] {rel}:{i}: 含數字但沒有出處 → {s[:60]}")
                continue
            for n in nums:
                stats["numbers"] += 1
                if not any(found(n, t) for t in texts):
                    errs.append(f"[數字] {rel}:{i}: 在所標出處找不到「{n}」 → {s[:60]}")

    idx = open(pages["index"], encoding="utf-8").read() if "index" in pages else ""
    idx_links = {m.group(1).strip() for m in LINK.finditer(idx)}
    for name in pages:
        if name in ("index", "log"):
            continue
        if name not in idx_links:
            errs.append(f"[索引] index.md 沒列 [[{name}]]")
        if not (inlinks[name] - {"index", "log"}):
            errs.append(f"[連結] 孤兒頁：除了 index 以外沒有頁面連到 [[{name}]]")

    if not quiet:
        for e in errs:
            print(e)
    print(f"檢查 {stats['pages']} 頁、{stats['cites']} 個出處、{stats['numbers']} 個數字；錯誤 {len(errs)} 個。"
          + (" ✅ 全過" if not errs else " ❌"))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
