# %%
import numpy as np
import pandas as pd
import sklearn as skl
from matplotlib import pyplot as plt

# %%
from pathlib import Path

label_cols = [
    'id',
    'Product ID',
    'Type'
]

num_cols = [
    'Air temperature [K]',
    'Process temperature [K]',
    'Rotational speed [rpm]',
    'Torque [Nm]',
    'Tool wear [min]'
]

binary_cols = [
    'TWF',
    'HDF',
    'PWF',
    'OSF',
    'RNF'
]

target_col = 'Machine failure'

data_csv = Path('data/train.csv')
data_df = pd.read_csv(data_csv, index_col=label_cols).astype('float32')

# %%
display(data_df.size)
display(data_df.index)
display(data_df.columns)
display(data_df.dtypes)

data_df.info()

# %%
pd.options.display.float_format = '{:.3f}'.format
data_df.head()

# %%
data_df.describe()

# %%
data_df.head().style.background_gradient('Blues').format(precision=3)

# %%
data_df[num_cols].plot.kde(sharex=False, subplots=True, layout=(2, 3), figsize=(12, 6))
plt.show()

# %%
data_df[num_cols].hist(yrot=45, layout=(2, 3), figsize=(12, 6))
plt.show()

# %%
data_df[binary_cols].hist(bins=2, yrot=45, layout=(2, 3), figsize=(12, 6))
plt.show()

# %%
data_df.drop(columns=binary_cols).boxplot(by=target_col, sharey=False, layout=(2, 3), figsize=(12, 6))
plt.show()

# %%
pd.plotting.scatter_matrix(data_df[num_cols], 1, (12, 12), s=1, c=data_df[target_col], cmap='bwr')
plt.show()

# %%
data_df.plot.scatter(num_cols[0], num_cols[1], 1, target_col, cmap='bwr')
plt.show()

# %%
from sklearn.preprocessing import StandardScaler

x = data_df[num_cols+binary_cols].to_numpy()
y = data_df[target_col].to_numpy()

std_scalar = StandardScaler().fit(x)
x = std_scalar.transform(x)

pd.DataFrame(x).describe()

# %%
from sklearn.decomposition import PCA

pca = PCA(2).fit(x)
x_pca = pca.transform(x)

plt.scatter(*x_pca.T, 1, y, cmap='bwr')
plt.colorbar(label=target_col)
xlim = plt.xlim()
ylim = plt.ylim()
plt.show()

# %%
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y)

# %%
from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier((16, 16)).fit(x_train, y_train)

print('loss', mlp.loss_)

plt.plot(mlp.loss_curve_)
plt.show()

# %%
mlp.score(x_test, y_test)

# %%
y_preds = mlp.predict(x_test)
x_pca = pca.transform(x_test)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 4))

scatter0 = ax0.scatter(*x_pca.T, 1, y_test, cmap='bwr')
ax0.set_xlabel('PCA Component 1')
ax0.set_ylabel('PCA Component 2')
ax0.set_title('Actual')
fig.colorbar(scatter0, ax=ax0, label=target_col)

scatter1 = ax1.scatter(*x_pca.T, 1, y_preds, cmap='bwr')
ax1.set_xlabel('PCA Component 1')
ax1.set_ylabel('PCA Component 2')
ax1.set_title('Predicted')
fig.colorbar(scatter1, ax=ax1, label=target_col)

plt.show()

# %%
from sklearn.linear_model import LogisticRegression

logit = LogisticRegression().fit(x_train, y_train)
y_preds = logit.predict(x_test)
logit.score(x_test, y_test)

# %%
from sklearn.svm import LinearSVC

svc = LinearSVC(dual='auto').fit(x_train, y_train)
y_preds = svc.predict(x_test)
svc.score(x_test, y_test)

# %%
n = 1000
mesh = np.dstack(
    np.meshgrid(
        np.linspace(*xlim, n),
        np.linspace(*ylim, n),
        indexing='xy'
    )
).reshape(n * n, 2)

mesh = pca.inverse_transform(mesh)
mesh_preds = mlp.predict(mesh).reshape(n, n)

plt.imshow(mesh_preds, 'bwr', aspect='auto', interpolation='bilinear', extent=xlim+ylim, origin='lower')
plt.colorbar()
plt.show()


