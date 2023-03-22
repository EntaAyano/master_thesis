# 分類モデル
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.resnet50 import ResNet50
from keras.models import Sequential, Model
from keras.layers import Input, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.python.keras.models import load_model
import pandas as pd
from keras.preprocessing import image
from keras import backend as K

# action_analyze
import argparse, csv, cv2, os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import gc
from memory_profiler import profile

#実験1つめ
expt_num = "inout_data/" + "experiment6"

#[1]saliency mapがあるep.の番号をとってきて saliency_ep に入れる
print("============ now [1] ============")
pass_sal_ep = expt_num + "/saliency/make_saliency_ep._data-.csv"
csv_sal_ep = open(pass_sal_ep,"r")
f_sal_ep = csv.reader(csv_sal_ep)

saliency_ep = []
for i in f_sal_ep:
    saliency_ep.append(int(i[0]))

csv_sal_ep.close()

#[2]reward_data.csvから各ep.のframe数をとってきて ep_frame に入れ>る
print("============ now [2] ============")
pass_reward = expt_num + "/reward_data.csv"
csv_reward = open(pass_reward,"r")
f_reward = csv.reader(csv_reward)

ep_frame = []
for i in f_reward:
    if(int(i[0]) in saliency_ep):
        ep_frame.append(int(i[1]))
csv_reward.close()

#[3]制御規則を保存するための変数を作る -> 0で初期化
###rule[エージェントの場所(0-2)][saliencyの場所(0-8)][saliency内容の分類クラス(0-11)][action(0-5)(実際のactionの番号-1)]
print("============ now [3] ============")
agent_space_num = 3
saliency_space_num = 6
action_num = 6

rule = [[] for i in range(action_num)]

#[4]分類モデルの呼び出し
print("============ now [4] ============")
# 分類モデルに必要な変数とか
classes = ["A-B","A-S","Agent","Invader_singular","S-I_p","A-B-S","A-S-I_p","B-S","Invader_plural","SafeArea","B-I_p"]
img_width, img_height = 50, 50
class_num = len(classes)

# 分類モデル
model = load_model("model_FineTuning-4.h5")

#[4]1frameずつsaliency/inputの画像をとってきて、制御規則を生成する
print("============ now [5] ============")

ep_log = 0
ep_last = saliency_ep[-1]
counter = 1
counter_name = 1

# 画像の大きさなどの値を持ってきたかのフラグ
flag_get_num = 0

pass_rulefile = expt_num + "/rule7_model4_1input_1rule.csv"
file_rule = open(pass_rulefile, 'w')
writer_rule = csv.writer(file_rule)

rule_counter = 0

for ep, frame in zip(saliency_ep, ep_frame):
    # 進捗を出力
    if(ep_log != ep):
        print("** now ep ",counter,"/",len(saliency_ep))
        counter += 1

        # outputのファイルを開く
        pass_output = expt_num + "/output/output_data-" + str(ep) + ".csv"
        csv_output = open(pass_output,"r")
        f_output = csv.reader(csv_output)

        outputdata = []
        for j in f_output:
            frame_num = int(j[1])
            if(frame_num != 1):
                outputdata.append(int(j[2]))

        csv_output.close()

        ep_log = ep

    # saliency / input 画像の読み込み
    for i in range(frame-2):

        # ログの出力
        if(i%50==0):
            print("*** now frame " + str(i) + " / " + str(frame-2))


        pass_saliency = expt_num + "/saliency/saliency-" + str(ep) + "/saliency_map-" + str(i+2) + ".jpg"
        saliency = cv2.imread(pass_saliency)
        
        pass_inputdata = expt_num + "/input/input_data-" + str(ep) + "/input-" + str(i+2) + ".jpg"
        inputdata = cv2.imread(pass_inputdata)

        # 画像の高さ(height)と幅(width)の取り出し
        if(flag_get_num == 0):
            height = inputdata.shape[0]
            width = inputdata.shape[1]

            # 上の切り取り：25
            # 下の切り取り：15
            ## 1/3 の値
            height_1_3 = (height - 40) / 3 + 25
            width_1_3 = width / 3

            ## 2/3の値
            height_2_3 = ( (height - 40) / 3 ) * 2 + 25
            width_2_3 = ( width / 3 ) * 2

            # フラグの更新
            flag_get_num = 1


        ##[5.1]そのframeでとったactionをとってくる
        action = outputdata[i]

        ##[5.2]エージェントの場所の獲得
        # 下から25行目だけを取り出し
        input_data_agent = inputdata[-25, :]

        # 左のピクセルから順番にみて、BGRすべてが50より大きいピクセルを探す
        for j in range(width):
            if(input_data_agent[j][0]>50 and input_data_agent[j][1]>50 and input_data_agent[j][2]>50):
                agent_pixel = j+1
                break

        # ピクセルの値をみて、エージェントが 左/中央/右 のうちどこのブロックにいるのかを調べる(左:0, 中央:1, 右:2)
        if(agent_pixel <= width_1_3):
            agent_block = 0
        elif(width_1_3 < agent_pixel <= width_2_3):
            agent_block = 1
        else:
            agent_block = 2
        
        ##[5.3]saliency箇所の切り出し
        # グレー化(?)
        saliency_gray = cv2.cvtColor(saliency, cv2.COLOR_BGR2GRAY)
        retval, saliency_bw = cv2.threshold(saliency_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 輪郭の抽出
        contours, hierarchy = cv2.findContours(saliency_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        rule_frame = []

        ##[5.4]saliency場所の獲得
        # 輪郭をひとつずつみる
        for j in range(len(contours)):
            # x,y:外接矩形の左上、w:幅、h:高さ
            x, y, w, h = cv2.boundingRect(contours[j])

            # 外接矩形の中心(x,y)
            saliency_center_x = x + (w/2)
            saliency_center_y = y + (h/2)

            # 中心の値をみて、saliencyがどこのブロックにいるのかを調べる(0-8)
            if(saliency_center_x <= width_1_3):
                if(saliency_center_y <= height_1_3):
                    saliency_block = 0
                elif(height_1_3 < saliency_center_y <= height_2_3):
                    saliency_block = 3
                else:
                    saliency_block = 6
            elif(width_1_3 < saliency_center_x <= width_2_3):
                if(saliency_center_y <= height_1_3):
                    saliency_block = 1
                elif(height_1_3 < saliency_center_y <= height_2_3):
                    saliency_block = 4
                else:
                    saliency_block = 7
            else:
                if(saliency_center_y <= height_1_3):
                    saliency_block = 2
                elif(height_1_3 < saliency_center_y <= height_2_3):
                    saliency_block = 5
                else:
                    saliency_block = 8

            ##[5.5]saliency内容の分類
            # 入力画像における外接矩形の切り出し
            inputdata_cut = inputdata[y : y+h , x : x+w]

            # 分類したい画像を分類できる形式に直す -> z
            inputdata_cut_resize = cv2.resize(inputdata_cut, dsize=(img_width, img_height))
            z = image.img_to_array(inputdata_cut_resize)
            z = np.expand_dims(z, axis=0)
            z = z / 255

            del inputdata_cut_resize
            del inputdata_cut
            gc.collect()

            # 分類の予測
            result_numpy = model.predict_on_batch(z)
            saliency_item = np.argmax(result_numpy[0])

            # この frame における Saliency 内容に追加
            rule_frame.append([agent_block, saliency_block, saliency_item])

        # すべての Saliency の内容がとり終わったあと
        ## rule_frame をならべかえ
        rule_frame_sort = sorted(rule_frame)

        ## 重複したルールがまだないとき
        if(rule_frame_sort not in rule[action]):
            ## ruleに追加
            rule[action].append(rule_frame_sort)
            ## ルールのファイルに書き込み
            for k,l in enumerate(rule_frame_sort):
                 writer_rule.writerow([rule_counter,k,action,l[0],l[1],l[2]])
            rule_counter += 1


# 実験2つめ
expt_num = "inout_data/" + "experiment4"

#[1]saliency mapがあるep.の番号をとってきて saliency_ep に入れる
print("============ now [1] ============")
pass_sal_ep = expt_num + "/saliency/make_saliency_ep._data-.csv"
csv_sal_ep = open(pass_sal_ep,"r")
f_sal_ep = csv.reader(csv_sal_ep)

saliency_ep = []
for i in f_sal_ep:
    saliency_ep.append(int(i[0]))

csv_sal_ep.close()

#[2]reward_data.csvから各ep.のframe数をとってきて ep_frame に入れ>る
print("============ now [2] ============")
pass_reward = expt_num + "/reward_data.csv"
csv_reward = open(pass_reward,"r")
f_reward = csv.reader(csv_reward)

ep_frame = []
for i in f_reward:
    if(int(i[0]) in saliency_ep):
        ep_frame.append(int(i[1]))
csv_reward.close()

ep_log = 0
ep_last = saliency_ep[-1]
counter = 1
counter_name = 1

for ep, frame in zip(saliency_ep, ep_frame):
    # 進捗を出力
    if(ep_log != ep):
        print("** now ep ",counter,"/",len(saliency_ep))
        counter += 1

        # outputのファイルを開く
        pass_output = expt_num + "/output/output_data-" + str(ep) + ".csv"
        csv_output = open(pass_output,"r")
        f_output = csv.reader(csv_output)

        outputdata = []
        for j in f_output:
            frame_num = int(j[1])
            if(frame_num != 1):
                outputdata.append(int(j[2]))

        csv_output.close()

        ep_log = ep

    # saliency / input 画像の読み込み
    for i in range(frame-2):

        # ログの出力
        if(i%50==0):
            print("*** now frame " + str(i) + " / " + str(frame-2))


        pass_saliency = expt_num + "/saliency/saliency-" + str(ep) + "/saliency_map-" + str(i+2) + ".jpg"
        saliency = cv2.imread(pass_saliency)

        pass_inputdata = expt_num + "/input/input_data-" + str(ep) + "/input-" + str(i+2) + ".jpg"
        inputdata = cv2.imread(pass_inputdata)

        ##[5.1]そのframeでとったactionをとってくる
        action = outputdata[i]

        ##[5.2]エージェントの場所の獲得
        # 下から25行目だけを取り出し
        input_data_agent = inputdata[-25, :]

        # 左のピクセルから順番にみて、BGRすべてが50より大きいピクセルを探す
        for j in range(width):
            if(input_data_agent[j][0]>50 and input_data_agent[j][1]>50 and input_data_agent[j][2]>50):
                agent_pixel = j+1
                break

        # ピクセルの値をみて、エージェントが 左/中央/右 のうちどこのブロックにいるのかを調べる(左:0, 中央:1, 右:2)
        if(agent_pixel <= width_1_3):
            agent_block = 0
        elif(width_1_3 < agent_pixel <= width_2_3):
            agent_block = 1
        else:
            agent_block = 2


        # グレー化(?)
        saliency_gray = cv2.cvtColor(saliency, cv2.COLOR_BGR2GRAY)
        retval, saliency_bw = cv2.threshold(saliency_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 輪郭の抽出
        contours, hierarchy = cv2.findContours(saliency_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        rule_frame = []

        ##[5.4]saliency場所の獲得
        # 輪郭をひとつずつみる
        for j in range(len(contours)):
            # x,y:外接矩形の左上、w:幅、h:高さ
            x, y, w, h = cv2.boundingRect(contours[j])

            # 外接矩形の中心(x,y)
            saliency_center_x = x + (w/2)
            saliency_center_y = y + (h/2)

            # 中心の値をみて、saliencyがどこのブロックにいるのかを調べる(0-8)
            if(saliency_center_x <= width_1_3):
                if(saliency_center_y <= height_1_3):
                    saliency_block = 0
                elif(height_1_3 < saliency_center_y <= height_2_3):
                    saliency_block = 3
                else:
                    saliency_block = 6
            elif(width_1_3 < saliency_center_x <= width_2_3):
                if(saliency_center_y <= height_1_3):
                    saliency_block = 1
                elif(height_1_3 < saliency_center_y <= height_2_3):
                    saliency_block = 4
                else:
                    saliency_block = 7
            else:
                if(saliency_center_y <= height_1_3):
                    saliency_block = 2
                elif(height_1_3 < saliency_center_y <= height_2_3):
                    saliency_block = 5
                else:
                    saliency_block = 8

            ##[5.5]saliency内容の分類
            # 入力画像における外接矩形の切り出し
            inputdata_cut = inputdata[y : y+h , x : x+w]

            # 分類したい画像を分類できる形式に直す -> z
            inputdata_cut_resize = cv2.resize(inputdata_cut, dsize=(img_width, img_height))
            z = image.img_to_array(inputdata_cut_resize)
            z = np.expand_dims(z, axis=0)
            z = z / 255

            del inputdata_cut_resize
            del inputdata_cut
            gc.collect()

            # 分類の予測
            result_numpy = model.predict_on_batch(z)
            saliency_item = np.argmax(result_numpy[0])

            # この frame における Saliency 内容に追加
            rule_frame.append([agent_block,saliency_block, saliency_item])

        # すべての Saliency の内容がとり終わったあと
        ## rule_frame をならべかえ
        rule_frame_sort = sorted(rule_frame)

        ## 重複したルールがまだないとき
        if(rule_frame_sort not in rule[action]):
            ## ruleに追加
            rule[action].append(rule_frame_sort)
            ## ルールのファイルに書き込み
            for k,l in enumerate(rule_frame_sort):
                 writer_rule.writerow([rule_counter,k,action,l[0],l[1],l[2]])
            rule_counter += 1

