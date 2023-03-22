import numpy as np
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
from matplotlib import pyplot as plt
from skfuzzy.cluster import cmeans

# 入力の所属するメンバーシップ関数の値をリストにして返す
## 入力1,2,4

def get_number_input(value):
    return_num = []
    if (value<=-0.4):
        return_num.append(0)
    if (-0.5<value) and (value<=-0.1):
        return_num.append(1)
    if (-0.2<value) and (value<=0.2):
        return_num.append(2)
    if (0.1<value) and (value<=0.5):
        return_num.append(3)
    if (0.4<value):
        return_num.append(4)
    return return_num

## 入力3
def get_number_input3(value):
    return_num = []
    if (value<=-0.15):
        return_num.append(0)
    if (-0.2<value) and (value<=-0.0):
        return_num.append(1)
    if (-0.05<value) and (value<=0.05):
        return_num.append(2)
    if (0.0<value) and (value<=0.2):
        return_num.append(3)
    if (0.15<value):
        return_num.append(4)
    return return_num

# 入力の所属するメンバーシップ関数の名前を返す
def get_name_input(value):
    if (value==0):
        return "0"
    elif (value==1):
        return "1"
    elif (value==2):
        return "2"
    elif (value==3):
        return "3"
    elif (value==4):
        return "4"

# 出力の所属するメンバーシップ関数の名前を返す
def get_name_output(value):
    if (value==0):
        return "0"
    elif (value==1):
        return "1"
    elif (value==2):
        return "2"

# メンバーシップ関数の個数
c = 5

# 各メンバーシップ関数の中心値
"""
center_input = [-0.6,0.0,0.6]
center_input3 = [-0.2,0.0,0.2]
"""
center_input = [-0.5,-0.3,0.0,0.3,0.5]
center_input3 = [-0.2,-0.1,0.0,0.1,0.2]


# データの読み込み
data_set = np.loadtxt(
    fname="experiment-keep-before50.csv", #読み込むファイルのパスと名前
    dtype="float", #floatで読み込む
    delimiter=",", #csvなのでカンマで区切る
)

input_list =[ [[[0 for i in range(c)] for j in range(c)]for j in range(c)]for j in range(c)]

input_weight_list =[ [[[0 for i in range(c)] for j in range(c)]for j in range(c)]for j in range(c)]

for data in data_set:
    # それぞれの入力が所属するメンバーシップ関数のリストを作成
    data1_men = get_number_input(data[0])
    data2_men = get_number_input(data[1])
    data3_men = get_number_input3(data[2])
    data4_men = get_number_input(data[3])
    
    # すべての組み合わせにおいて、その重みとaction*重みの値を保存
    for i in data1_men:
        weight_tmp1 = abs(data[0] - center_input[i])
        weight1 = Decimal(str(weight_tmp1)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        for j in data2_men:
            weight_tmp2 = abs(data[1] - center_input[i])
            weight2 = Decimal(str(weight_tmp2)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            for k in data3_men:
                weight_tmp3 = abs(data[2] - center_input3[i])
                weight3 = Decimal(str(weight_tmp3)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                for l in data4_men:
                    weight_tmp4 = abs(data[3] - center_input[i])
                    weight4 = Decimal(str(weight_tmp4)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    
                    # 重みの和
                    weight_sum = weight1 + weight2 + weight3 + weight4

                    # 重み*action
                    action = float(weight_sum) * data[4]

                    # それぞれのデータのリストに加算
                    tmp_action = input_list[i][j][k][l]
                    input_list[i][j][k][l] = tmp_action + action

                    tmp_weight = input_weight_list[i][j][k][l]
                    input_weight_list[i][j][k][l] = tmp_weight + weight_sum


# それぞれの組み合わせにおけるactionの出力
counter = 1

for i in range(c):
    for j in range(c):
        for k in range(c):
            for l in range(c):
                if(input_list[i][j][k][l] != 0):
                    #num = float(input_list[i][j][k][l]) * 1.0 / float(input_weight_list[i][j][k][l])
                    #action_num = Decimal(str(num)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
                    #print("    rule%d = ctrl.Rule(cart_position[\"%d\"] & cart_speed[\"%d\"] & pole_angule[\"%d\"] & pole_angular_velocity[\"%d\"], action[\"%s\"])" % (counter,i,j,k,l,get_name_output(action_num)))
                    #print("input1:%d, input2:%d, input3:%d, input4:%d -> %s" % (i,j,k,l,get_name_output(action_num)))
                    
                    index = 1000*(i+1) + 100*(j+1) + 10*(k+1) + l+1

                    print("        elif(index==%d):" % (index))
                    print("            rule_num.append(%d)" % (counter))
                    counter += 1



