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
            df_tmp = pd.read_csv(os.path.join(self.folder_name, file_name))
            file_type = file_name.replace('.csv', '')

            # 時間を0から始める
            df_tmp['time'] = (df_tmp['time'] - df_tmp['time'][0]) / 1000

            print(file_name)

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
