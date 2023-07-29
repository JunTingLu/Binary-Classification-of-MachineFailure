# Binary-Classification-of-MachineFailure
### **資料講解**
這次的題目屬於分類問題，主要透過分析機器可能故障的機率。
首先解釋一下資料型別所代表的意義
- **Type**: consisting of a letter L, M, or H for low, medium and high as product quality variants.
- **Air temperature [K]**: generated using a random walk process later normalized to a standard deviation of 2 K around 300 K.
- **Process temperature [K]**: generated using a random walk process normalized to a standard deviation of 1 K, added to the air temperature plus 10 K.
- **Rotational speed [rpm]**: calculated from a power of 2860 W, overlaid with a normally distributed noise.
- **Torque [Nm]**: torque values are normally distributed around 40 Nm with a Ïƒ = 10 Nm and no negative values.
- **Tool wear [min]**: The quality variants H/M/L add 5/3/2 minutes of tool wear to the used tool in the process.
- **Machine failure**: whether the machine has failed in this particular datapoint for any of the following failure modes are true.
- **Tool wear failure (TWF)**: the tool will be replaced of fail at a randomly selected tool wear time between 200 ~ 240 mins.
- **Heat dissipation failure (HDF)**: heat dissipation causes a process failure, if the difference between air and process temperature is below 8.6 K and the rotational speed is below 1380 rpm.
- **Power failure (PWF)**: the product of torque and rotational speed (in rad/s) equals the power required for the process. If this power is below 3500 W or above 9000 W, the process fails.
- **Overstrain failure (OSF)**: if the product of tool wear and torque exceeds 11,000 minNm for the L product variant (12,000 M, 13,000 H), the process fails due to overstrain.
- **Random failures (RNF)**: each process has a chance of 0,1 % to fail regardless of its process parameters.

從以下表格來看，

![image](https://github.com/JunTingLu/Binary-Classification-of-MachineFailure/assets/135250298/887e9b97-0e13-497d-a77d-59268900dd99)


### **資料分析與處理**
在我們對資料沒有任何domain knowledge 的情況下，直接對所有的特徵進行密度分析、相關性分析，
從資料分布發現到



對於訓練結果採用ROC(Receiver Operator Characteristic Curve)進行評分，


### **訓練結果**
