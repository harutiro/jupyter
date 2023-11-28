import os

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from enum import Enum
from typing import List


class GraphViewOptions(Enum):
    low_filter = 'low_filter'
    diff = 'diff'
    none = 'none'


class GraphAxis(Enum):
    x = 'x'
    y = 'y'
    z = 'z'
    rssi = 'rssi'
    bpm = 'bpm'
    acc = 'acc'


class MakeGraph:
    """
    コンストラクタ
    @param folder_name フォルダ名
    """

    def __init__(self, folder_name):
        self.folder_name = '../data/' + folder_name
        self.path = folder_name
        self.file_names = os.listdir(self.folder_name)

        # 全てのファイルのデータフレームを作成
        self.acc_df = pd.DataFrame()
        self.angular_df = pd.DataFrame()
        self.ble_char_df = pd.DataFrame()
        self.ble_tent_df = pd.DataFrame()
        self.heart_rate_df = pd.DataFrame()

        # フォントサイズとフォントの設定
        plt.rcParams["font.size"] = 14
        plt.rcParams['font.family'] = "IPAexGothic"

        for file_name in self.file_names:
            # .DS_Storeを除外
            if file_name == '.DS_Store':
                continue

            df_tmp = pd.read_csv(os.path.join(self.folder_name, file_name))
            file_type = file_name.replace('.csv', '')

            print(file_name)
            # 時間を0から始める
            df_tmp['time'] = (df_tmp['time'] - df_tmp['time'][0]) / 1000

            match file_type:
                case 'acc':
                    self.acc_df = df_tmp
                case 'Angular':
                    self.angular_df = df_tmp
                case 'BLE_isu':
                    self.ble_char_df = df_tmp
                case 'BLE_tent':
                    self.ble_tent_df = df_tmp
                case 'HartRate':
                    self.heart_rate_df = df_tmp

    """
    normを計算する
    @param list データフレーム
    @return normのデータフレーム
    """

    def norm(self, norm_list: pd.DataFrame) -> pd.DataFrame:
        tmp_list = pd.DataFrame()
        tmp_list['time'] = norm_list['time']
        tmp_list['norm'] = np.sqrt(norm_list['x'] ** 2 + norm_list['y'] ** 2 + norm_list['z'] ** 2)
        return tmp_list

    """
    ローパスフィルタ
    @param list データフレーム
    @param window_size ウィンドウサイズ
    @return フィルタ後のデータフレーム
    """

    def low_filter(self, low_filter_list: pd.DataFrame, window_size: int) -> pd.DataFrame:

        for column in low_filter_list:
            if column == 'time':
                continue
            low_filter_list[column] = low_filter_list[column].rolling(window_size).mean()

        return low_filter_list

    """
    微分を行う
    @param list データフレーム
    @return 微分後のデータフレーム
    """

    def diff(self, diff_list: pd.DataFrame) -> pd.DataFrame:
        for column in diff_list:
            if column == 'time':
                continue
            diff_list[column] = diff_list[column].diff()

        return diff_list

    """
    RSSIのグラフを作成する
    @param list データフレーム
    @param axis 軸
    @param filter_num フィルタ数
    @param label_nameの名前
    """
    def ble_plot(self, plt_lists: [pd.DataFrame], axis: GraphAxis, filter_num: int,label_name: [str]) -> None:
        fig = plt.figure(figsize=(15, 25))
        fig.subplots_adjust(hspace=0.5)
        ax = fig.add_subplot(5, 1, 1)

        for index, list_val in enumerate(plt_lists):
            ax.plot(list_val['time'], list_val['rssi'], label=label_name[index])
        ax.legend()

        # タイトル
        ax.set_title(self.path + '_' + axis.value + '_' + "window=" + str(filter_num))
        ax.set_xlabel('time [s]')
        ax.set_ylabel('RSSI [dBm]')
        ax.grid()

        plt.show()

    """
    グラフを作成する
    @param list データフレーム
    @param option オプション
    @param axis 軸
    @param filter_num フィルタ数
    """
    def plot(self, plt_lists: List[pd.DataFrame], option: List[GraphViewOptions], axis: GraphAxis,
             filter_num: int) -> None:
        fig = plt.figure(figsize=(15, 25))
        fig.subplots_adjust(hspace=0.5)

        for index, list_val in enumerate(plt_lists):
            self.__ax(index=index, fig=fig, ax_list=list_val, option=option, axis=axis, filter_num=filter_num)

        plt.show()

    """
    matplotlibのaxを作成する
    @param list データフレーム
    @param option オプション
    @param axis 軸
    @param filter_num フィルタ数
    """

    def __ax(self, index: int, fig: plt.Figure, ax_list: pd.DataFrame, option: List[GraphViewOptions], axis: GraphAxis,
             filter_num: int) -> None:
        ax = fig.add_subplot(5, 1, index + 1)

        match axis:
            case GraphAxis.acc:
                for column in ax_list:
                    if column == 'time':
                        continue
                    ax.plot(ax_list['time'], ax_list[column], label=column)
            case _:  # GraphAxis.x, GraphAxis.y, GraphAxis.z, GraphAxis.rssi, GraphAxis.bpm
                try:
                    ax.plot(ax_list['time'], ax_list[axis.value], label=axis.value)
                except:
                    print('その軸は存在しません')
                    pass
        ax.legend()

        # タイトル
        ax.set_title(self.path + '_' + axis.value + '_' + "window=" + str(filter_num))
        ax.set_xlabel('time [s]')

        # 単位の指定
        if axis == GraphAxis.x or axis == GraphAxis.y or axis == GraphAxis.z or axis == GraphAxis.acc:
            ax.set_ylabel('acceleration [m/s^2]')
        elif axis == GraphAxis.bpm:
            ax.set_ylabel('BPM [bpm]')
        elif axis == GraphAxis.rssi:
            ax.set_ylabel('RSSI [dBm]')

        ax.grid()

    """
    時間でデータフレームを分割する
    @param list データフレーム
    @param start_time 開始時間
    @param end_time 終了時間
    @return 分割後のデータフレーム
    """

    def split_time(self, split_time_list: pd.DataFrame, start_time: int,
                   end_time: int) -> pd.DataFrame:
        split_time_list = split_time_list[
            (split_time_list['time'] >= start_time) & (split_time_list['time'] <= end_time)]
        return split_time_list

    """
    csvを出力する
    @param list データフレーム
    @param file_name ファイル名
    """
    def output_csv(self, output_list: pd.DataFrame, file_name: str) -> None:
        # indexも出力する
        output_list.to_csv('../data/output/' + file_name + '.csv', index=True)

    """
    周波数成分を計算する
    @param list データフレーム
    @param filter_num フィルタ数
    @return 周波数成分のデータフレーム
    """
    def __fft(self, fft_list: pd.DataFrame, filter_num: int) -> pd.DataFrame:
        tmp_list = pd.DataFrame()

        # window_sizeで指定した範囲で計算して、終わったら、次の範囲に移動する
        for i in range(0, len(fft_list), filter_num):
            for column in fft_list:
                if column == 'time':
                    continue
                # FFTを計算

                N = len(fft_list[column][i:i + filter_num])  # サンプル数
                dt = 1 / self.calculate_sampling_frequency(fft_list[column][i:i + filter_num])  # サンプリング間隔

                y_fft = np.fft.fft(fft_list[column][i:i + filter_num])  # 離散フーリエ変換
                freq = np.fft.fftfreq(N, d=dt)  # 周波数を割り当てる（※後述）
                Amp = abs(y_fft / (N / 2))  # 音の大きさ（振幅の大きさ）

                # 最大の周波数成分のインデックスを取得
                index = np.argmax(Amp[1:int(N / 2)])

                # 最大の周波数成分を取得
                tmp_list.loc[i, column + '_fft'] = freq[index]

                # 最大の周波数成分の振幅を取得
                tmp_list.loc[i, column + '_fft_amp'] = Amp[index]

                # 最大の周波数成分の位相を取得
                tmp_list.loc[i, column + '_fft_phase'] = np.angle(y_fft[index])

                # 最大の周波数成分の周波数を取得
                tmp_list.loc[i, column + '_fft_freq'] = freq[index] * self.calculate_sampling_frequency(fft_list[column][i:i + filter_num])


        return tmp_list

    """
    平均・分散・最大値・最小値・中央値・四分位数・標準偏差を計算する
    範囲はwindow_sizeで指定する
    @param list データフレーム
    @param filter_num フィルタ数
    @return 平均・分散・最大値・最小値・中央値・四分位数・標準偏差のデータフレーム
    """
    def calc(self, calc_list: pd.DataFrame, filter_num: int) -> pd.DataFrame:
        tmp_list = pd.DataFrame()

        # window_sizeで指定した範囲で計算して、終わったら、次の範囲に移動する
        for i in range(0, len(calc_list), filter_num):
            for column in calc_list:
                if column == 'time':
                    continue
                # 平均、標準偏差、最小値、第1四分位数、中央値（第2四分位数）、第3四分位数、最大値などを計算する
                tmp_list.loc[i, column + '_mean'] = calc_list[column][i:i + filter_num].mean()
                tmp_list.loc[i, column + '_std'] = calc_list[column][i:i + filter_num].std()
                tmp_list.loc[i, column + '_min'] = calc_list[column][i:i + filter_num].min()
                tmp_list.loc[i, column + '_25%'] = calc_list[column][i:i + filter_num].quantile(0.25)
                tmp_list.loc[i, column + '_50%'] = calc_list[column][i:i + filter_num].quantile(0.5)
                tmp_list.loc[i, column + '_75%'] = calc_list[column][i:i + filter_num].quantile(0.75)
                tmp_list.loc[i, column + '_max'] = calc_list[column][i:i + filter_num].max()

        return tmp_list

    """
    サンプリング周波数を計算する
    """
    def calculate_sampling_frequency(self,data: pd.DataFrame) -> float:
        time_stamps = [data_point for data_point in data]
        time_interval = time_stamps[-1] - time_stamps[0]
        sampling_frequency = 1 / (time_interval / len(data))
        return sampling_frequency
