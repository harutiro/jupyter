import csv

def calculate_sampling_frequency(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # スキップ: ヘッダ行
        next(reader)
        # 1行目の時間を取得
        prev_time = float(next(reader)[0])
        # サンプル間隔のリストを初期化
        time_diffs = []

        for row in reader:
            time = float(row[0])
            time_diff = time - prev_time
            time_diffs.append(time_diff)
            prev_time = time

        # サンプリング周波数の計算
        average_time_diff = sum(time_diffs) / len(time_diffs)
        sampling_frequency = 1.0 / average_time_diff

        return sampling_frequency

csv_file = './study/fft/acc.csv'
sampling_frequency = calculate_sampling_frequency(csv_file)
print(f"サンプリング周波数: {sampling_frequency} Hz")