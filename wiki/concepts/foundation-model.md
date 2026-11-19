---
type: concept
title: Foundation model（基礎模型）
---
# Foundation model（基礎模型）

## 白話解釋
- 先用海量資料把一個大模型「訓練成通才」，之後再拿去做各種專門任務。ChatGPT 就是語言上的 foundation model。
- 在醫療影像，foundation model 可以把一張 CT 或一整張病理切片，轉成一串數字（向量），代表影像的重點特徵。之後的小模型只要用這串數字來判斷就好。
- 好處是不必從零開始訓練；缺點是這串數字人類看不懂，維度又很高，病人少的時候容易過度擬合。

## 在這篇論文怎麼用
- CT：用一個癌症影像 foundation model，從病灶周圍擷取 4,096 維特徵 [prelaj2026, p.3]。
- 病理切片：用 Prov-GigaPath 把整張切片轉成一個向量 [prelaj2026, p.15]。
- 為了確認結果不是剛好某個模型造成的，作者又用另一個病理 foundation model TITAN 重做，結論相同 [prelaj2026, p.15]。

## 相關頁面
[[multimodal-fusion]]、[[ml-vs-dl]]、[[multimodal-not-replicated]]
