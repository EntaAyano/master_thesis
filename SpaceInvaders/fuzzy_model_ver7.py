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

# gym
import gym

# メモリの解放
import gc

# 動画保存
import imageio

import random

#[0] 実験の番号などのセット
## 実験の番号
expt_num = "inout_data/experiment6"

## 分類モデル/制御規則のファイル についている通し番号
model_num = 4


# [1]gymの環境を作る
print("============ now [1] ============")
env = gym.make('SpaceInvaders-v0')


# [2]分類モデルの呼び出し
print("============ now [2] ============")
#classes = ["A-B","A-S","Agent","Backgraund","Invader_singular","S-I_p","A-B-S","A-S-I_p","B-S","Invader_plural","Number","SafeArea","B-I_p"]
classes = ["A-B","A-S","Agent","Invader_singular","S-I_p","A-B-S","A-S-I_p","B-S","Invader_plural","SafeArea","B-I_p"]
img_width, img_height = 50, 50

# 分類モデル
model_name = "model_FineTuning-" + str(model_num) + ".h5"
model = load_model(model_name)


# [3]制御規則の読み込み
print("============ now [3] ============")
class_num = len(classes)
action_num = 6

# 制御規則を入れる配列
## NOOPのルールは飛ばすため action_num から 1 引いてる
rule = [[] for i in range(action_num-1)]


# [4]制御規則のファイル読み込み
pass_rulefile = expt_num + "/rule7_model4_1input_1rule_summary.csv"
csv_rule = open(pass_rulefile,"r")
f_rule = csv.reader(csv_rule)

# 現在のルールの番号
rule_num_now = -1

# 一旦入れておくところ
rule_element_tmp = []

# NOOPのルールは飛ばす
# i = [ルールの番号][ルール内の要素の番号][action(0-5)][エージェントとsaliencyの位置(0-5)][分類ラベルの番号(0-12)]
for i in f_rule:
    # 新しいルールのとき：
    if(int(i[0]) != rule_num_now):
        ## rule_element_tmpが空じゃないとき(=最初以外)はrule_element_tmpをrule[action-1]に追加
        if(len(rule_element_tmp) != 0):
            rule[action_num_now-1].append(rule_element_tmp)

        ## 新しいルールの情報を更新
        ### actionの番号
        action_num_now = int(i[2])

        ### 現在のルールの番号
        rule_num_now = int(i[0])

        ### rule_element_tmpを初期化
        rule_element_tmp = []

        ### actionがNOOPじゃないとき，rule_element_tmpに追加
        if(rule_num_now != 0):
            rule_element_tmp.append([int(i[3]),int(i[4])])
    # 前と同じルールのとき：
    else:
        ### actionがNOOPじゃないとき，rule_element_tmpに追加
        if(rule_num_now != 0):
            rule_element_tmp.append([int(i[3]),int(i[4])])

# [5]各種変数の準備
## 入力画像を1枚インポート
print("============ now [5] ============")
pass_inputdata = expt_num + "/input/input_data-" + str(1) + "/input-" + str(3) + ".jpg"
inputdata = cv2.imread(pass_inputdata)

height = inputdata.shape[0]
width = inputdata.shape[1]

# 上の切り取り：25
# 下の切り取り：15
## 1/3 の値
height_1_3 = int((height - 40) / 3 + 25)
width_1_3 = int(width / 3)

## 2/3の値
height_2_3 = int(( (height - 40) / 3 ) * 2 + 25)
width_2_3 = int(( width / 3 ) * 2)

# [6]1ep.のループ
print("============ now [6] ============")

# 累積reward
reward_sum = 0

# 平均reward
reward_mean = 0

# 累積frame
frame_sum = 0

# scoreのmin/max
reward_min = 0
reward_max = 0

# frameのmin/max
frame_min = 0
frame_max = 0

# ep数
ep_num = 100

# saliency map があるディレクトリの指定
saliency_mean_dir = "inout_data/experiment6/saliency/saliency-60/saliency_map-"
#saliency_mean_dir = "inout_data/experiment4/saliency/saliency-30/saliency_map-"
for ep in range(ep_num):
    #print("============= ep. " + str(ep) + " =============")
    observation = env.reset()
    reward_sum = 0

    input_observation = []

    for frame in range(10000):

        env.render()

        input_observation.append(observation)

        action_ = [0 for g in range(action_num-1)]

        ########## [5.1] エージェントの場所 ###########
        # 下から25行目だけを取り出し
        input_data_agent = observation[-25, :]

        # 左のピクセルから順番にみて、BGRすべてが50より大きいピクセルを探す
        for j in range(width):
            if(input_data_agent[j][0]>50 and input_data_agent[j][1]>50 and input_data_agent[j][2]>50):
                agent_pixel = j+1
                break

        # Saliencyの中心が，
        # これより小さいときは「左」のみ
        agent_pixel_left = agent_pixel - 15
        # これより大きい値 ~ agent_pixel_up_right までは「上」のみ
        agent_pixel_up_left = agent_pixel - 15
        # agent_pixel_up_left ~ これより小さい値までは「上」のみ
        agent_pixel_up_right = agent_pixel + 15
        # これより大きいときは「右」のみ
        agent_pixel_right = agent_pixel + 15

        ##[5.2] saliency mapの読み込み
        saliency_mean_img_pass = saliency_mean_dir + str(frame+2) + ".jpg"
        saliency_mean_img = cv2.imread(saliency_mean_img_pass)

        if(frame>1550):
        #if(frame>800):
            frame_ = random.randint(0,1550)
            saliency_mean_img_pass = saliency_mean_dir + str(frame_) + ".jpg"
            saliency_mean_img = cv2.imread(saliency_mean_img_pass)
        else:
            saliency_mean_img_pass = saliency_mean_dir + str(frame+2) + ".jpg"
        saliency_mean_img = cv2.imread(saliency_mean_img_pass)
        
        ##[5.3]saliency箇所の切り出し
        # グレー化(?)
        saliency_gray = cv2.cvtColor(saliency_mean_img, cv2.COLOR_BGR2GRAY)
        retval, saliency_bw = cv2.threshold(saliency_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 輪郭の抽出
        contours, hierarchy = cv2.findContours(saliency_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        rule_frame = []

        # 輪郭をひとつずつみる
        #print(len(contours))
        for j in range(len(contours)):
            # x,y:外接矩形の左上、w:幅、h:高さ
            x, y, w, h = cv2.boundingRect(contours[j])

            # 外接矩形の中心(x,y)
            saliency_center_x = x + (w/2)
            saliency_center_y = y + (h/2)

            # 「高い」に属する
            if(saliency_center_y<110):
                # 「左上」に属する
                if(saliency_center_x<agent_pixel_left):
                    agent_saliency_block = 0
                # 「右上」に属する
                #elif(agent_pixel_right<saliency_center_x):
                #    agent_saliency_block = 2
                # 「真上」に属する
                #else:
                #    agent_saliency_block = 1
                elif(agent_pixel_left<saliency_center_x<agent_pixel_right):
                    agent_saliency_block = 4
                else:
                    agent_saliency_block = 5
            # 「低い」に属する
            else:
                # 「左上」に属する
                if(saliency_center_x<agent_pixel_left):
                    agent_saliency_block = 3
                # 「右上」に属する
                #elif(agent_pixel_right<saliency_center_x):
                #    agent_saliency_block = 5
                # 「真上」に属する
                #else:
                #    agent_saliency_block = 4
                elif(agent_pixel_left<saliency_center_x<agent_pixel_right):
                    agent_saliency_block = 4
                else:
                    agent_saliency_block = 5

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
            rule_frame.append([agent_saliency_block, saliency_item])


        # すべての Saliency の内容がとり終わったあと
        ## rule_frame をならべかえ
        rule_frame_sort = sorted(rule_frame)

        # 適用できるルールを探す
        ## actionを順番にみる：
        for i in range(len(rule)):
            for j in rule[i]:
                if(rule_frame_sort == j):
                    # 該当したsaliency boxの個数も加味
                    action_[i] += len(j)

        # ルールが適応された回数が最も多いactionを取り出し
        action = action_.index(max(action_)) + 1

        # actionを伝える
        observation, reward, done, info = env.step(action)

        reward_sum += reward

        if done:
            reward_mean += reward_sum
            frame_sum += frame
            print("Ep." + str(ep) + " is end " + str(frame+1) + " frames, and reward is " + str(reward_sum))

            if(reward_min == 0):
                reward_min = reward_sum
                reward_max = reward_sum
                frame_min = frame
                frame_max = frame

            if(reward_sum < reward_min):
                reward_min = reward_sum
            elif(reward_max < reward_sum):
                reward_max = reward_sum

            if(frame < frame_min):
                frame_min = frame
            elif(frame_max < frame):
                frame_max = frame

            # input_observation を動画保存
            movie_name = "movie_fuzzy/SpaceInveders_model" + str(model_num)+ "-fuzzy_ver8_ep"+ str(ep) + "_useSaliency1ep_1input21Rule_summary.gif"
            imageio.mimsave(movie_name, input_observation, 'GIF', **{'duration': 1.0/60.0})
            reward_sum = 0

            break

reward_mean = reward_mean / ep_num
print("reward mean : " + str(reward_mean))
print("reward min : " + str(reward_min))
print("reward max : " + str(reward_max))

frame_mean = frame_sum / ep_num
print("frame mean : " + str(frame_mean))
print("frame min : " + str(frame_min))
print("frame max : " + str(frame_max))
