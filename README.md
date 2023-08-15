# Binary-Classification-of-MachineFailure 
**主要運用kaggle提供的機器對應的各項參數，進行一些對於機器失效分析的處理及預測**

## **資料講解**
> 這次的題目屬於二元分類問題，最終目的是預測機器運作中異常的機率，針對Kaggle提供的資料集，首先解釋一下資料中各參數所代表的大致意義。而其中的Machine failure便是作為最終判定機器是否異常的指標。
- **Type**: 由字母 L、M 或 H 組成，代表產品的不同品質，分別為低、中、高品質。
- **Air temperature [K]**: 空氣溫度。
- **Process temperature [K]**: 機器運昨時的溫度。
- **Rotational speed [rpm]**: 機器旋轉速率。
- **Torque [Nm]**: 機器旋轉力矩。
- **Tool wear [min]**: 機器磨損時間。
- **Tool wear failure (TWF)**: 機器磨損失效或需更換的狀態。
- **Heat dissipation failure (HDF)**: 機器熱散失導致異常。
- **Power failure (PWF)**: 機器運轉的功率過低或過高導致異常的狀態。
- **Overstrain failure (OSF)**: 機器運轉過程過度應力變化而導致異常。
- **Random failures (RNF)**: 隨機下導致機器異常。
- **Machine failure**: 判定機器故障、失效的狀態。

## **資料分析與處理**
針對數據分析，大致分為以下幾個部分
- **Train, Test data stastics and visualization**
- **Correlation of features and histogram plot to decide the importance of features**
- **Dimensionally reduction with PCA by Machine failure** 
- **Training with different algorithm (Logistic regression, random forest)**
- **ROC curve to estimation and Caliabration**
  
### 1. **Train, Test data stastics and visualization**
> 在我們對資料沒有任何domain knowledge 的情況下，直接對所有的特徵進行密度分析、相關性下手或許是不錯的選擇。由於我們最關心的是最後的Machine failure的結果，從tain, test 數據上來看，初步可觀察到資料可發現在type欄位的部分H,M,L僅影響Air temp./ Process tem. /Rotational speed/ Torque/ Tool wear等五個特徵下的數量差異，分布上幾乎一致，而從這五個特徵目前還看不出和Machine failure顯著的關係，而"品質"在各特徵中分布是相當一致的

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/32885aab-81a4-4a48-85ed-0d9ce5f8c72f)

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/abd1881e-9d12-46f4-a6d8-47d54e39a3a1)

### 2. **Correlation of features and histogram plot to decide the importance of features**
> 若進一步Air temp./ Process tem. /Rotational speed/ Torque/ Tool wear等五個特徵和Machine failure 關係，從相關性(Correlation)的作圖中，值得注意的是在Toque和Rotation speed 欄位似乎對於解釋Machine failure有一定的重要性。而其餘特徵對於Machine failure的分布暫時看不出顯著的趨勢

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/9548d76d-f625-4b3f-9128-ea4f65ad5d78)

>另外，對於TWF/HDF/PWF/OSF/RNF對Machine failure的影響來看，從以下直方圖來看，當Machine failure 為"0"時，除了RNF外其他特徵也剛好為"0"，說明了在TWF/HDF/PWF/OSF出現fail時，機器才有可能出現異常，而RNF例外則推測是因為隨機性所導致結果不穩定。

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/84d373a8-6f83-4617-ab49-af4fbbad510f)

>對於品質是否影響Machine failure，從下圖統計的結果來看，確實有發現隨著品質越低，機器異常的可能性越高。

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/b5a0d1a3-7110-45d0-a168-1cfd9d21e704)


>進一步使用混淆矩陣(Confusion matrix)來觀察所有特徵間的依賴關係，可發現確實在TWF/HDF/PWF/OSF位其中最具影響機器異常的特徵，另外在Process temp/Air temp.以及Toque/Rotation speed 也具有很高的相關性。

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/83050ca9-b041-42f6-a3b7-1ee3fae67166)

### 3. **Dimensionally reduction with PCA by Machine failure**
>接著對所有特徵進行主成分分析(PCA)[2]，簡單來說我們想利用降維的方式在盡可能不失資料本身特性下，找到能夠切分出這些特徵的平面所構成的向量空間，而這向量空間便是對原先特徵向量化後求解特徵值和特徵向量的過程，最終能得到這所有所有特徵向量組合構成的超維空間，若以每個特徵向量平方為機率(Probability)，因此進一步計算每一種"組合"在整體機率分佈下所占的比例，可觀察在最大前兩個pca0和pca1的維度下資料的切分狀況，確實發現還無法很好的切分Machine failure的"0"和"1"分布，因此後續會進一步利用不同演算法來找到最佳切分的結果

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/f30b7929-093b-423f-bb76-42ce6a51966f)

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/1358be46-6675-46eb-b6ab-ec9b62077560)


### 4. **Training with different algorithm**
>對於使用ROC判斷正確率(Accuracy)
>由於kaggle未提供的測試(Valid)資料，故直接針對train的資料進行(0.75/0.25)比例切分出測試資料，並採用以下三種演算法訓練:<br>
> 1.針對MLP進行超參數方式優化，使用交叉驗證(cross validation)的方式進行網格搜索<br>
> 2.使用Logistic Regression方式進行預測<br>
> 3.使用隨機森林方式進行預測<br>
> 最終發現到Logist regression 所得到的分數最高

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/f1176b74-97bb-4d1b-874e-ac0442861194)

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/237c390d-dd95-4aeb-b7c4-ad728708450b)

> 從對應上圖的機率分布直方圖來看，由於Logistic regression更真實反映了數據"機率"分布的表現，相較之下，使用MLP多層感知層以及隨機森林的免算法進行ROC計算後發現，發現預測的機率都會極端分布在0和1，此代表可能出現

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/9c097715-699b-4d24-8a38-553ab72c2f59)


### 5. **ROC curve to estimation and Caliabration** 
> 在經過ROC曲線計算後，發現準確度(Accuracy)高達97%，從校正曲線(Calibraiton curve)來衡量[3]，當我們透過不同模型繪製出來的曲線越靠近中間的黑色虛線，便代表結果越準確。

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/c0fd791d-390f-44f2-b457-f4fb958c17f7)


**結果與討論**
> 在假設沒有任何Domain knowladge下，我們考慮所有特徵，進行PCA分析後，藉由Logistic regression 演算法進行訓練，可發現準確度有97%，但推測由於TWF/FDF/PWF/OSF等四個特徵對於整體的影響程度太大，從最一開始的confusion matrix就能夠得知，因此對於分析上會使得其他特徵無法有效反映在預測結果上。此外，若考慮其他可用的特徵訓練，或許能更加提升模型預測能力，像是Rotation speed 和 Toque的乘積亦能作為新的特徵欄位，增加模型準確度，另外也可採用前向特徵篩選(Feature slelction)的方式，依序將不同特徵丟置模型中訓練，只要過程中低於閥值參數，就被視為不重要的特徵而進一步替除掉，而閥值通常可透過每次結果的均值作為標準。

## **參考資料**
1. [分類器評估方法 — ROC曲線、AUC、Accuracy、PR曲線](https://medium.com/marketingdatascience/%E5%88%86%E9%A1%9E%E5%99%A8%E8%A9%95%E4%BC%B0%E6%96%B9%E6%B3%95-roc%E6%9B%B2%E7%B7%9A-auc-accuracy-pr%E6%9B%B2%E7%B7%9A-d3a39977022c)
2. [機器/統計學習:主成分分析(Principal Component Analysis, PCA)](https://chih-sheng-huang821.medium.com/%E6%A9%9F%E5%99%A8-%E7%B5%B1%E8%A8%88%E5%AD%B8%E7%BF%92-%E4%B8%BB%E6%88%90%E5%88%86%E5%88%86%E6%9E%90-principle-component-analysis-pca-58229cd26e71)
3. [模型信心的本質！：Probability Calibration](https://axk51013.medium.com/%E6%A8%A1%E5%9E%8B%E4%BF%A1%E5%BF%83%E7%9A%84%E6%9C%AC%E8%B3%AA-probability-calibration-cbc680a44efa)


