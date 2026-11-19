---
type: concept
title: AUC 與 C-index：怎麼替預測模型打分數
---
# AUC 與 C-index：怎麼替預測模型打分數

## 白話解釋
- **AUC**：隨便抓一個「有效的人」和一個「沒效的人」，模型給前者較高分的機率。一半一半等於丟銅板，滿分是完美，分數越接近滿分越好。
- **C-index**：AUC 的存活版本。隨便抓兩個人，模型能不能正確排出誰活得比較久。
- **信賴區間（CI）**：分數的不確定範圍，區間越窄越可信。
- **P 值**：差異是不是可能只是運氣。習慣上要夠小，才說「有顯著差異」。

## 在這篇論文怎麼用
- 只用臨床資料的模型，在測試集預測 24 個月存活的 AUC 0.74（95% CI 0.67–0.81）[prelaj2026, p.2]。
- 疾病控制的 AUC 在外部驗證只剩 0.55，接近丟銅板 [prelaj2026, p.2]。
- Cox 模型的 C-index 0.65，LIPI 分數 0.55 [prelaj2026, p.6]。

## 相關頁面
[[validation]]、[[biomarkers]]、[[sensitivity-specificity]]、[[external-validation-drop]]
