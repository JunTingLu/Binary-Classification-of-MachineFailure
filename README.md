# Binary-Classification-of-MachineFailure 
 
## **資料講解**
這次的題目屬於分類問題，主要透過不同指標，像是機器的各項參數來評估分析機器可能故障的機率。
首先解釋一下資料中各參數所代表的意義
- **Type**: 由字母 L、M 或 H 組成，代表產品的不同品質變體，分別為低、中、高品質。
- **Air temperature [K]**: 使用隨機遊走過程生成，然後將其標準化為標準差為 2 K，圍繞著 300 K 的範圍。
- **Process temperature [K]**: 使用隨機遊走過程生成，然後將其標準化為標準差為 1 K，並加上 10 K，以得到最終的處理溫度。處理溫度是在空氣溫度的基礎上進行計算的。
- **Rotational speed [rpm]**: 由功率 2860 瓦特計算得出，並添加了一個服從正態分布的噪音。
- **Torque [Nm]**: 扭矩值服從正態分布，平均值為 40 Nm，標準差為 10 Nm，且不會有負值。
- **Tool wear [min]**: 不同品質變體 H/M/L 會分別給使用的工具增加 5/3/2 分鐘的工具磨損時間。
- **Tool wear failure (TWF)**: 工具在使用過程中將在隨機選定的工具使用時間點（介於 200 到 240 分鐘之間）失效或需更換。
- **Heat dissipation failure (HDF)**: 如果空氣溫度與處理溫度之間的差異小於 8.6 K，且旋轉速度低於 1380 rpm，則熱散失導致了一個處理失敗。
- **Power failure (PWF)**: 扭矩和旋轉速度（以 rad/s 為單位）的乘積等於處理所需的功率。如果此功率低於 3500 瓦特或高於 9000 瓦特，則處理失敗。
- **Overstrain failure (OSF)**: 如果工具磨損和扭矩的乘積超過 L 品質變體為 11,000 minNm（M 為 12,000，H 為 13,000），則由於過度應變而導致處理失敗。
- **Random failures (RNF)**: 每個處理過程有 0.1% 的機會在不考慮其過程參數的情況下失敗。
- **Machine failure**: 此數據點中機器是否因任何故障模式而失效。


## **資料分析與處理**

針對數據分析，大致分為以下幾個部分
- Train, Test data stastics and visualization
- Correlation of features and histogram plot to decide the importance of features
- Dimensionality reduction with PCA by Machine failure 
- Training with different algorithm (Logistic regression, random forest)
- ROC curve to estimation
- Collabration 
- Feature engineering
- Optimizing the result 

**1.Train, Test data stastics and visualization**
>在我們對資料沒有任何domain knowledge 的情況下，直接對所有的特徵進行密度分析、相關性下手或許是不錯的選擇。由於委們最關心的是>最後的machine failure的結果，從tain, test 數據上來看，初步可觀察到資料可發現在type欄位的部分H,M,L對於machine failure並無>明顯影響，因為分布上幾乎一致，只是數量級上的差別。


在這五個特徵下的處理不會有閥值設定的問題。而除此之外的其他特徵

最後machine failure即是我們最終需要評估的重要指標也只有0和1兩種可能，因此最後把資料丟進模型訓練的過程將會是一個二元分類器

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/887e9b97-0e13-497d-a77d-59268900dd99)

若將先前Air temperature,Process temperature,Rotational speed,Torque,Tool wear進行統計量計算，



**2. Correlation of features and histogram plot to decide the importance of features**
>嘗試先在未做任何資料處理的情況下從correlation來篩選出較為重要的特徵，

**Dimensionality reduction with PCA by Machine failure**
>進一步對資料進行主成分分系(PCA)降維處理，簡單來說我們想利用降維的方式在盡可能不失資料本身特性下，找到資料對應的特徵向量，並投影到此新的坐標系下，


4.**Training with different algorithm**
由於kaggle未提供的測試(valid)資料，故直接針對train的資料進行(0.75/0.25)比例切分出測試資料，




**Feature engineering**
若加入特徵前處理，從先前的資料視覺化來看，發現事實上id和資料本身並無太大的關係，但若考慮新的特徵組合，例如



## **延伸討論**




## **參考資料**
1. [分類器評估方法 — ROC曲線、AUC、Accuracy、PR曲線](https://medium.com/marketingdatascience/%E5%88%86%E9%A1%9E%E5%99%A8%E8%A9%95%E4%BC%B0%E6%96%B9%E6%B3%95-roc%E6%9B%B2%E7%B7%9A-auc-accuracy-pr%E6%9B%B2%E7%B7%9A-d3a39977022c)
2. [機器/統計學習:主成分分析(Principal Component Analysis, PCA)](https://chih-sheng-huang821.medium.com/%E6%A9%9F%E5%99%A8-%E7%B5%B1%E8%A8%88%E5%AD%B8%E7%BF%92-%E4%B8%BB%E6%88%90%E5%88%86%E5%88%86%E6%9E%90-principle-component-analysis-pca-58229cd26e71)

