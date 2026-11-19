---
type: concept
title: 機器學習、深度學習與 logistic regression
---
# 機器學習、深度學習與 logistic regression

## 白話解釋
- **機器學習（ML）**：給電腦很多「題目＋答案」，讓它自己找出規則。像 logistic regression（邏輯斯迴歸）其實是統計學的老方法：把每個因素乘上一個權重、加起來，換算成機率。random forest 則是讓很多棵「是非題決策樹」投票。
- **深度學習（DL）**：用很多層神經網路，自己從原始資料（例如影像）學出特徵。很強，但需要大量資料，也比較難解釋。
- **LASSO**：一種「自動挑變數」的方法，把不重要的因素權重壓成零，避免模型記住雜訊。
- **Cox 模型**：統計上專門處理「多久之後發生事件」（例如存活時間）的模型。

## 在這篇論文怎麼用
- 機器學習路線（MLEF）：特徵串接後用 LASSO 篩選，再用 logistic regression 或 random forest [prelaj2026, p.16]。
- 深度學習路線（DLIF）：每種資料各有一個編碼器，再合併判斷，可以處理缺資料的病人 [prelaj2026, p.8]。
- 兩者只用臨床資料時表現差不多：預測 24 個月存活，機器學習 0.74、深度學習 0.73 [prelaj2026, p.6]。
- 最後拿去給醫師試用的，是只用臨床資料的 logistic regression 與 Cox 模型，不是深度學習 [prelaj2026, p.6]。

## 相關頁面
[[multimodal-fusion]]、[[foundation-model]]、[[auc-cindex]]、[[prelaj2026]]
