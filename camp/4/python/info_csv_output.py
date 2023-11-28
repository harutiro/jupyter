import os

from Graphs import MakeGraph ,GraphAxis , GraphViewOptions


def info_csv_output():
    # ../data/以下のフォルダ名を全て取得
    folder_names = os.listdir('../data')

    # フォルダ名を一つずつ取り出す
    for folder_name in folder_names:
        print(folder_name)

        # .DS_Storeを除外
        if folder_name == '.DS_Store' or folder_name == "output":
            continue

        # グラフを作成
        make_graph = MakeGraph(folder_name)

        acc_df = make_graph.acc_df
        info_df = make_graph.calc(acc_df, 50)

        # 正解データを足す
        # folder_nameがテント生活を含まれていた場合は0
        # folder_nameが焼きそばを含まれていた場合は1
        # folder_nameが肉を焼くを含まれていた場合は1
        # folder_nameが火おこしを含まれていた場合は2

        if 'テント生活' in folder_name:
            info_df['answer'] = 0
        elif '焼きそば' in folder_name:
            info_df['answer'] = 1
        elif '肉を焼く' in folder_name:
            info_df['answer'] = 1
        elif '火おこし' in folder_name:
            info_df['answer'] = 2
        else:
            info_df['answer'] = -1

        make_graph.output_csv(info_df, file_name= folder_name + 'acc_info.csv')

if __name__ == '__main__':
    info_csv_output()