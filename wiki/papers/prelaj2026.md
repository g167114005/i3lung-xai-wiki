---
type: paper
title: AI 能不能幫醫師判斷誰適合免疫治療？I3LUNG 研究
key: prelaj2026
year: 2026
journal: Nature Medicine（2025 JIF 52.5）
source_file: Prelaj2026_NatMed_I3LUNG.pdf
---
# Prelaj et al.（2026）I3LUNG：可解釋 AI 輔助肺癌免疫治療決策

## 一句話
六個國家的醫院把兩千多位肺癌病人的資料交給 AI 學習，看 AI 能不能在打免疫治療「之前」就猜出誰會有效，再測試醫師拿到 AI 的建議和解釋後，判斷有沒有變準。

## 研究設計
- 對象：2,396 位晚期非小細胞肺癌（[[lung-cancer-immunotherapy]]）病人，都接受免疫治療或免疫合併化療 [prelaj2026, p.1]。
- 來自六個中心：義大利、希臘、德國、西班牙、美國、以色列 [prelaj2026, p.2]。
- 治療期間是 2012 年 9 月到 2023 年 10 月，屬於回溯性研究，也就是回頭整理過去的病歷 [prelaj2026, p.2]。
- 主分析用 2,075 人：1,550 人訓練、274 人測試；美國芝加哥大學的 251 人另外當外部驗證 [prelaj2026, p.2]。怎麼切資料見 [[validation]]。
- 四種資料（[[multimodal-fusion]]）：臨床與抽血資料 2,396 人、基因 1,723 人、CT 1,705 人、病理切片 936 人 [prelaj2026, p.2]。
- 四種資料都齊全的只有 339 人 [prelaj2026, p.2]。
- 要預測的結果：整體存活、6 個月與 24 個月存活，以及疾病控制率 [prelaj2026, p.2]。

## 模型與結果
- 兩條路線：機器學習早期融合（MLEF）與深度學習中期融合（DLIF）[prelaj2026, p.2]。名詞見 [[ml-vs-dl]]。
- 只用臨床抽血資料的模型，在測試集預測 24 個月存活的 AUC 是 0.74；到外部驗證降為 0.60 [prelaj2026, p.2]。AUC 見 [[auc-cindex]]。
- 單一指標 PD-L1 的 AUC 只有 0.53，AI 模型是 0.74 [prelaj2026, p.6]。PD-L1 見 [[biomarkers]]。
- 用 AI 分出的低風險組中位存活 25.1 個月，高風險組 4.7 個月 [prelaj2026, p.6]。見 [[kaplan-meier]]。
- 加入 CT 與病理的多模態模型，在交叉驗證把疾病控制 AUC 從 0.63 提到 0.77 [prelaj2026, p.2]；但在獨立測試集沒有一致重現 [prelaj2026, p.5]。見 [[multimodal-not-replicated]]。

## XAI 怎麼做
- 用 [[shap]] 說明每個病人的預測是哪些因素推上去或拉下來的 [prelaj2026, p.6]。
- 最重要的負面因素：體能狀態較差（ECOG 大於 0）、骨轉移、肝轉移、腦轉移 [prelaj2026, p.6]。
- 臨床可用性研究：20 位醫師先自己判斷，再看 AI 與 SHAP 解釋後重新判斷 [prelaj2026, p.6]。
- 醫師預測疾病控制的敏感度從 0.72 升到 0.87 [prelaj2026, p.6]。敏感度見 [[sensitivity-specificity]]。

![原文 Figure 5：臨床可用性研究的設計與結果（CC BY 4.0）](../assets/fig5.png)

## 報告者的評讀
- 優點：規模大、跨國多中心，驗證切分嚴謹，而且少見地真的去測「醫師用了以後有沒有變好」。
- 限制：可用性研究沒有對照組，見 [[usability-no-control]]；專家反而更常跟著錯誤建議走，見 [[automation-bias]]。
- 外部驗證表現下降，見 [[external-validation-drop]]。
- 模型學到的可能只是「誰本來預後比較好」，見 [[predictive-vs-prognostic]]。

## 相關頁面
- 導讀：[[story]]
- 觀念：[[lung-cancer-immunotherapy]]、[[biomarkers]]、[[ml-vs-dl]]、[[multimodal-fusion]]、[[foundation-model]]、[[auc-cindex]]、[[validation]]、[[kaplan-meier]]、[[shap]]、[[fairness]]、[[sensitivity-specificity]]、[[predictive-vs-prognostic]]
- 議題：[[multimodal-not-replicated]]、[[external-validation-drop]]、[[usability-no-control]]、[[automation-bias]]
