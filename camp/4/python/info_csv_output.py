import os

from Graphs import MakeGraph ,GraphAxis , GraphViewOptions


def info_csv_output():
    # ../data/以下のフォルダ名を全て取得
    folder_names = os.listdir('../data')

    # フォルダ名を一つずつ取り出す
    for folder_name in folder_names:
        print(folder_name)

        # .DS_Storeを除外
        if folder_name == '.DS_Store':
            continue

        # グラフを作成
        make_graph = MakeGraph(folder_name)

        acc_df = make_graph.acc_df
        info_df = make_graph.calc(acc_df, 50)

        make_graph.output_csv(info_df, file_name= folder_name + 'acc_info.csv')

if __name__ == '__main__':
    info_csv_output()