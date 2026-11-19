# 建置紀錄

## 2026-11-19
- ingest `prelaj2026`：Prelaj A, et al. Clinical usability of an explainable AI decision support tool and evaluation of multimodal models in NSCLC. Nature Medicine. 2026;32:3235–3247. doi:10.1038/s41591-026-04488-2（CC BY 4.0）。
- 建立導讀 1 頁、論文頁 1 頁、觀念頁 12 頁、議題頁 4 頁。
- 圖片取自原文（CC BY 4.0），放在 `assets/`，每張都標明出處。
- `python tools/lint.py` 全過後才產生網頁。

## 已知限制
- 只有一份來源；觀念頁的「白話解釋」是一般背景知識，沒有引用其他文獻，因此依規則不放具體數字。
- 「報告者的評讀／看法」是報告者的觀點，不是原文作者的結論。
- 期刊影響因子（2025 JIF 52.5）不在原文 PDF 中，取自公開資料，正式引用前請以 Clarivate JCR 核對。
- 原文 PDF 不放進版控（`raw/` 已列入 `.gitignore`），可由 doi 連結免費下載。
