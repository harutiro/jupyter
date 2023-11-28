import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# フォントサイズとフォントの設定
plt.rcParams["font.size"] = 14
plt.rcParams['font.family'] = "IPAexGothic"

# CSVデータを読み込む
data1 = "./data/21/east_bpm.csv"
data2 = "./data/21/west_bpm.csv"
data3 = "./data/21/south_bpm.csv"
data4 = "./data/21/north_bpm.csv"

# CSVデータをDataFrameに変換する
df = pd.read_csv(os.path.join(data4))

# 心拍数データを抽出
heart_rate = df['bpm'].values.reshape(-1, 1)

# 標準化
scaler = StandardScaler()
heart_rate_scaled = scaler.fit_transform(heart_rate)

# diff
df['diff'] = df['bpm'].diff()
df['diff'] = df['diff'].fillna(0)

# KMeansで4つのクラスに分類
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(heart_rate_scaled)

# 分類結果を取得
df['cluster'] = kmeans.labels_

# 高いBPMのクラスタと低いBPMのクラスタを特定
high_bpm_cluster = df[df['bpm'] == df['bpm'].max()]['cluster'].values[0]
low_bpm_cluster = df[df['bpm'] == df['bpm'].min()]['cluster'].values[0]

# 驚愕と安堵のデータを取得
df_surprise = df[(df['diff'] > 2) & (df['cluster'] == high_bpm_cluster)]
df_relief = df[(df['diff'] < -2) & (df['cluster'] == low_bpm_cluster)]

# 条件に合致した場合、その後の10個のデータも同じ状態に変更
for index in df_surprise.index:
    df.loc[index:index+5, 'state'] = 'surprise'
for index in df_relief.index:
    df.loc[index:index+5, 'state'] = 'relief'


# グラフ描画
plt.figure(figsize=(10, 6))

# クラスタごとにデータをプロット
for cluster in df['cluster'].unique():
    plt.scatter(df[df['cluster'] == cluster]['time'], df[df['cluster'] == cluster]['bpm'], label=f'Cluster {cluster}')

# # 驚愕と安堵のデータをプロット
plt.scatter(df[df['state'] == 'surprise']['time'], df[df['state'] == 'surprise']['bpm'], label='Surprise', color='red')
plt.scatter(df[df['state'] == 'relief']['time'], df[df['state'] == 'relief']['bpm'], label='Relief', color='blue')

plt.xlabel('Time')
plt.ylabel('Heart Rate (bpm)')
plt.title('Heart Rate Clustering with Modified Clusters')
plt.legend()
plt.show()
