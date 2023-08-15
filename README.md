# Binary-Classification-of-MachineFailure 
 
## **資料講解**
>這次的題目屬於二元分類問題，最終目的是預測機器運作中異常的機率，針對Kaggle提供的資料集，首先解釋一下資料中各參數所代表的大致意義
- **Type**: 由字母 L、M 或 H 組成，代表產品的不同品質，分別為低、中、高品質。
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
- ROC curve to estimation and Caliabration 
- Optimizing the result 

**Train, Test data stastics and visualization**
- 欄位[H,M,L]和Machine failure關係
>在我們對資料沒有任何domain knowledge 的情況下，直接對所有的特徵進行密度分析、相關性下手或許是不錯的選擇。由於委們最關心的是>最後的machine failure的結果，從tain, test 數據上來看，初步可觀察到資料可發現在type欄位的部分H,M,L僅影響Air temp./ Process tem. 等五個特徵下的數量差異，分布上幾乎一致，而這五個特徵又和machine failure無顯著關係，因此可先初步排除"品質"對於預測結果的影響
![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/08eb3135-18a6-4b25-8217-e522c21978f0)


**Correlation of features and histogram plot to decide the importance of features**
>若進一步Air temp. / Process temp. 等五個特徵和Machine failure 關係，從相關性(Correlation)的作圖中，值得注意的是在Toque和Rotation speed 欄位似乎對於解釋Machine failure有一定的重要性。
>嘗試先在未做任何資料處理的情況下從correlation來篩選出較為重要的特徵。

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/9cb87f96-7454-4fb6-9ebf-91888dc3b019)

對於TWF/HDF/PWF/OSF/RNF對Machine failure的影響來看，當Machine failure 為"0"時，除了RNF外其他特徵也剛好為"0"，說明了在TWF/HDF/PWF/OSF出現fail時，機器才有可能出現異常，而RNF例外則推測是因為隨機性所導致結果不穩定。

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/a04741ce-d8d6-4735-9aaa-06b353211806)


對於品質是否影響Machine failure，從下圖統計的結果來看，確實有發現隨著品質越低，機器異常的可能性越高。

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/489f4950-4b48-4d45-87a9-b52eaf23ec71)


最後使用混淆矩陣(Confusion matrix)來觀察所有特徵間的依賴關係，可發現確實在TWF/HDF/PWF/OSF位其中最具影響機器異常的特徵，另外在Process temp/Air temp.以及Toque/Rotation speed 也具有很高的相關性。

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/2e12ad2d-2b34-4602-8dde-8a3d8dd4c110)


**Dimensionality reduction with PCA by Machine failure**
>接著對所有特徵進行主成分分析(PCA)[2]，簡單來說我們想利用降維的方式在盡可能不失資料本身特性下，找到每個特徵對應的特徵向量，並投影到此新的坐標系下，若以每個特徵對應的特徵向量平方為機率(Probability)，因此進一步計算每一個特徵在整體機率分佈下所占的比例

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/fb4b9316-28ef-4883-88fd-8a231ee8ae0f)


**Training with different algorithm**
>由於kaggle未提供的測試(Valid)資料，故直接針對train的資料進行(0.75/0.25)比例切分出測試資料，並透過多層感知層(MLP)訓練後，利用ROC曲線觀察在TF和TP兩類，其中TF指的是樣本無異常卻被檢測為異常；TP則為樣本無異常被檢測為無異常，這兩類的比例將影響準確度(Accuracy)的計算，如下
>
>![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/8ca6ae5a-061e-45a6-93d0-2a639c9178cb)

**ROC curve to estimation and Caliabration** 
>在經過ROC曲線計算後，發現準確度(Accuracy)高達97%，但若想進一步衡量此結果是否準確，可藉由繪製校正曲線(Calibraiton curve)來衡量[3]，當我們透過不同模型繪製出來的曲線越靠近中間的黑色虛線，便代表結果越準確

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/b67572b1-289a-4664-a589-d6100a077bf3)

**Optimizing the result** 
若進一步嘗試優化其結果，這裡採用了三種方式，如下:
1.針對MLP進行超參數方式優化，使用交叉驗證(cross validation)的方式進行網格搜索
2.使用Logistic Regression方式進行預測
3.使用隨機森林方式進行預測
藉由以上三種方式並透過Calibration curve衡量後，發現原來表現較好的Logistic regression模型的分數稍無降低了，

使用MLP多層感知層、Logistic regreesion 以及隨機森林的免算法進行ROC計算後發現，都有很好的準確度，從預測出來的機率直方圖來看，發現預測的機率都會極端分布在0和1，此代表可能出現

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/50e217d0-24cf-448b-a3f7-6b825fc11944)

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/b3b60be0-4149-410d-8b13-563d1b9dcb01)


**結果與討論**
> 在假設沒有任何Domain knowladge下，我們考慮所有特徵，進行PCA分析後，藉由Logistic regression 演算法進行訓練，可發現準確度有97%，但推測由於TWF/FDF/PWF/OSF等四個特徵對於整體的影響程度太大，從最一開始的confusion matrix就能夠得知，因此對於分析上會使得其他特徵無法有效反映在預測結果上。此外，若考慮其他可用的特徵訓練，或許能更加提升模型預測能力，像是Rotation speed 和 Toque的乘積亦能作為新的特徵欄位，增加模型準確度，另外也可採用前向特徵篩選(Feature slelction)的方式，依序將不同特徵丟置模型中訓練，只要過程中低於閥值參數，就被視為不重要的特徵而進一步替除掉，而閥值通常可透過每次結果的均值作為標準。

## **參考資料**
1. [分類器評估方法 — ROC曲線、AUC、Accuracy、PR曲線](https://medium.com/marketingdatascience/%E5%88%86%E9%A1%9E%E5%99%A8%E8%A9%95%E4%BC%B0%E6%96%B9%E6%B3%95-roc%E6%9B%B2%E7%B7%9A-auc-accuracy-pr%E6%9B%B2%E7%B7%9A-d3a39977022c)
2. [機器/統計學習:主成分分析(Principal Component Analysis, PCA)](https://chih-sheng-huang821.medium.com/%E6%A9%9F%E5%99%A8-%E7%B5%B1%E8%A8%88%E5%AD%B8%E7%BF%92-%E4%B8%BB%E6%88%90%E5%88%86%E5%88%86%E6%9E%90-principle-component-analysis-pca-58229cd26e71)
3. [模型信心的本質！：Probability Calibration](https://axk51013.medium.com/%E6%A8%A1%E5%9E%8B%E4%BF%A1%E5%BF%83%E7%9A%84%E6%9C%AC%E8%B3%AA-probability-calibration-cbc680a44efa)


