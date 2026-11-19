# I3LUNG 白話 Wiki：AI 能幫醫師判斷誰適合免疫治療嗎？

北醫 G167114005 醫學院人工智慧醫療碩士在職專班 碩二 鄭為遠

把一篇 Nature Medicine 論文做成給**沒有醫學背景的人**看的中文 Wiki，做法沿用第 10 週作業（先定規則 → 生成 → 程式檢查 → 產生網頁）。

- 論文：Prelaj A, et al. Clinical usability of an explainable AI decision support tool and evaluation of multimodal models in NSCLC. *Nature Medicine* 2026;32:3235–3247. doi:[10.1038/s41591-026-04488-2](https://doi.org/10.1038/s41591-026-04488-2)（CC BY 4.0）
- 期刊影響因子：2025 JIF 52.5（取自公開資料，請以 Clarivate JCR 核對）

## 線上版本
- 首頁：https://g167114005.github.io/i3lung-xai-wiki/
- 三分鐘看懂：https://g167114005.github.io/i3lung-xai-wiki/wiki-site/story.html
- Wiki 目錄：https://g167114005.github.io/i3lung-xai-wiki/wiki-site/index.html

## 內容
| 類型 | 頁數 | 說明 |
|---|---|---|
| 導讀 | 1 | 三分鐘看懂這篇論文 |
| 論文頁 | 1 | 研究設計、結果、XAI、報告者評讀 |
| 觀念頁 | 12 | 免疫治療、PD-L1、AUC、外部驗證、SHAP、公平性… |
| 議題頁 | 4 | 多模態沒重現、外部驗證掉分、可用性研究無對照、自動化偏誤 |

規則見 `AGENTS.md`；建置紀錄與已知限制見 `wiki/log.md`。

## 怎麼檢查與重建
```
python tools/lint.py         # 出處、數字、連結、格式（需要 pdftotext 或 pypdf，以及 raw/ 內的原文 PDF）
python tools/build_site.py   # 產生 wiki-site/ 與 index.html（需要 pip install markdown）
```
`raw/` 不進版控；原文可由 doi 連結免費下載，存成 `raw/Prelaj2026_NatMed_I3LUNG.pdf`。
