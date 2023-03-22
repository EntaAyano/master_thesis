import numpy as np

# 各入力の該当するメンバーシップ関数を返す
## 入力1,2,4
def get_number_input(value):
    return_num = []
    if (value<=-0.4):
        return_num.append(1)
    if (-0.5<value) and (value<=-0.1):
        return_num.append(2)
    if (-0.2<value) and (value<=0.2):
        return_num.append(3)
    if (0.1<value) and (value<=0.5):
        return_num.append(4)
    if (0.4<value):
        return_num.append(5)
    return return_num

## 入力3
def get_number_input3(value):
    return_num = []
    if (value<=-0.15):
        return_num.append(1)
    if (-0.2<value) and (value<=-0.0):
        return_num.append(2)
    if (-0.05<value) and (value<=0.05):
        return_num.append(3)
    if (0.0<value) and (value<=0.2):
        return_num.append(4)
    if (0.15<value):
        return_num.append(5)
    return return_num


# メンバーシップ関数のインデックスからルールの番号を返す
def rule_search(arr):

    rule_num = []

    for index in arr:
        if(index==1133):
            rule_num.append(1)
        elif(index==1134):
            rule_num.append(2)
        elif(index==1142):
            rule_num.append(3)
        elif(index==1143):
            rule_num.append(4)
        elif(index==1144):
            rule_num.append(5)
        elif(index==1145):
            rule_num.append(6)
        elif(index==1152):
            rule_num.append(7)
        elif(index==1153):
            rule_num.append(8)
        elif(index==1154):
            rule_num.append(9)
        elif(index==1155):
            rule_num.append(10)
        elif(index==1223):
            rule_num.append(11)
        elif(index==1232):
            rule_num.append(12)
        elif(index==1233):
            rule_num.append(13)
        elif(index==1234):
            rule_num.append(14)
        elif(index==1242):
            rule_num.append(15)
        elif(index==1243):
            rule_num.append(16)
        elif(index==1244):
            rule_num.append(17)
        elif(index==1252):
            rule_num.append(18)
        elif(index==1253):
            rule_num.append(19)
        elif(index==1254):
            rule_num.append(20)
        elif(index==1322):
            rule_num.append(21)
        elif(index==1323):
            rule_num.append(22)
        elif(index==1332):
            rule_num.append(23)
        elif(index==1333):
            rule_num.append(24)
        elif(index==1341):
            rule_num.append(25)
        elif(index==1342):
            rule_num.append(26)
        elif(index==1343):
            rule_num.append(27)
        elif(index==1351):
            rule_num.append(28)
        elif(index==1352):
            rule_num.append(29)
        elif(index==1353):
            rule_num.append(30)
        elif(index==1422):
            rule_num.append(31)
        elif(index==1431):
            rule_num.append(32)
        elif(index==1432):
            rule_num.append(33)
        elif(index==1433):
            rule_num.append(34)
        elif(index==1441):
            rule_num.append(35)
        elif(index==1442):
            rule_num.append(36)
        elif(index==1443):
            rule_num.append(37)
        elif(index==1451):
            rule_num.append(38)
        elif(index==1452):
            rule_num.append(39)
        elif(index==1541):
            rule_num.append(40)
        elif(index==1542):
            rule_num.append(41)
        elif(index==2123):
            rule_num.append(42)
        elif(index==2124):
            rule_num.append(43)
        elif(index==2125):
            rule_num.append(44)
        elif(index==2133):
            rule_num.append(45)
        elif(index==2134):
            rule_num.append(46)
        elif(index==2135):
            rule_num.append(47)
        elif(index==2142):
            rule_num.append(48)
        elif(index==2143):
            rule_num.append(49)
        elif(index==2144):
            rule_num.append(50)
        elif(index==2145):
            rule_num.append(51)
        elif(index==2152):
            rule_num.append(52)
        elif(index==2153):
            rule_num.append(53)
        elif(index==2154):
            rule_num.append(54)
        elif(index==2155):
            rule_num.append(55)
        elif(index==2222):
            rule_num.append(56)
        elif(index==2223):
            rule_num.append(57)
        elif(index==2224):
            rule_num.append(58)
        elif(index==2225):
            rule_num.append(59)
        elif(index==2232):
            rule_num.append(60)
        elif(index==2233):
            rule_num.append(61)
        elif(index==2234):
            rule_num.append(62)
        elif(index==2235):
            rule_num.append(63)
        elif(index==2242):
            rule_num.append(64)
        elif(index==2243):
            rule_num.append(65)
        elif(index==2244):
            rule_num.append(66)
        elif(index==2245):
            rule_num.append(67)
        elif(index==2252):
            rule_num.append(68)
        elif(index==2253):
            rule_num.append(69)
        elif(index==2254):
            rule_num.append(70)
        elif(index==2322):
            rule_num.append(71)
        elif(index==2323):
            rule_num.append(72)
        elif(index==2324):
            rule_num.append(73)
        elif(index==2332):
            rule_num.append(74)
        elif(index==2333):
            rule_num.append(75)
        elif(index==2334):
            rule_num.append(76)
        elif(index==2335):
            rule_num.append(77)
        elif(index==2341):
            rule_num.append(78)
        elif(index==2342):
            rule_num.append(79)
        elif(index==2343):
            rule_num.append(80)
        elif(index==2344):
            rule_num.append(81)
        elif(index==2345):
            rule_num.append(82)
        elif(index==2351):
            rule_num.append(83)
        elif(index==2352):
            rule_num.append(84)
        elif(index==2353):
            rule_num.append(85)
        elif(index==2421):
            rule_num.append(86)
        elif(index==2422):
            rule_num.append(87)
        elif(index==2423):
            rule_num.append(88)
        elif(index==2424):
            rule_num.append(89)
        elif(index==2431):
            rule_num.append(90)
        elif(index==2432):
            rule_num.append(91)
        elif(index==2433):
            rule_num.append(92)
        elif(index==2434):
            rule_num.append(93)
        elif(index==2435):
            rule_num.append(94)
        elif(index==2441):
            rule_num.append(95)
        elif(index==2442):
            rule_num.append(96)
        elif(index==2443):
            rule_num.append(97)
        elif(index==2444):
            rule_num.append(98)
        elif(index==2445):
            rule_num.append(99)
        elif(index==2451):
            rule_num.append(100)
        elif(index==2452):
            rule_num.append(101)
        elif(index==2521):
            rule_num.append(102)
        elif(index==2522):
            rule_num.append(103)
        elif(index==2531):
            rule_num.append(104)
        elif(index==2532):
            rule_num.append(105)
        elif(index==2541):
            rule_num.append(106)
        elif(index==2542):
            rule_num.append(107)
        elif(index==3115):
            rule_num.append(108)
        elif(index==3123):
            rule_num.append(109)
        elif(index==3124):
            rule_num.append(110)
        elif(index==3125):
            rule_num.append(111)
        elif(index==3133):
            rule_num.append(112)
        elif(index==3134):
            rule_num.append(113)
        elif(index==3135):
            rule_num.append(114)
        elif(index==3143):
            rule_num.append(115)
        elif(index==3144):
            rule_num.append(116)
        elif(index==3145):
            rule_num.append(117)
        elif(index==3153):
            rule_num.append(118)
        elif(index==3154):
            rule_num.append(119)
        elif(index==3155):
            rule_num.append(120)
        elif(index==3214):
            rule_num.append(121)
        elif(index==3215):
            rule_num.append(122)
        elif(index==3221):
            rule_num.append(123)
        elif(index==3222):
            rule_num.append(124)
        elif(index==3223):
            rule_num.append(125)
        elif(index==3224):
            rule_num.append(126)
        elif(index==3225):
            rule_num.append(127)
        elif(index==3232):
            rule_num.append(128)
        elif(index==3233):
            rule_num.append(129)
        elif(index==3234):
            rule_num.append(130)
        elif(index==3235):
            rule_num.append(131)
        elif(index==3242):
            rule_num.append(132)
        elif(index==3243):
            rule_num.append(133)
        elif(index==3244):
            rule_num.append(134)
        elif(index==3245):
            rule_num.append(135)
        elif(index==3252):
            rule_num.append(136)
        elif(index==3253):
            rule_num.append(137)
        elif(index==3254):
            rule_num.append(138)
        elif(index==3255):
            rule_num.append(139)
        elif(index==3313):
            rule_num.append(140)
        elif(index==3314):
            rule_num.append(141)
        elif(index==3322):
            rule_num.append(142)
        elif(index==3323):
            rule_num.append(143)
        elif(index==3324):
            rule_num.append(144)
        elif(index==3325):
            rule_num.append(145)
        elif(index==3331):
            rule_num.append(146)
        elif(index==3332):
            rule_num.append(147)
        elif(index==3333):
            rule_num.append(148)
        elif(index==3334):
            rule_num.append(149)
        elif(index==3335):
            rule_num.append(150)
        elif(index==3341):
            rule_num.append(151)
        elif(index==3342):
            rule_num.append(152)
        elif(index==3343):
            rule_num.append(153)
        elif(index==3344):
            rule_num.append(154)
        elif(index==3345):
            rule_num.append(155)
        elif(index==3351):
            rule_num.append(156)
        elif(index==3352):
            rule_num.append(157)
        elif(index==3353):
            rule_num.append(158)
        elif(index==3354):
            rule_num.append(159)
        elif(index==3412):
            rule_num.append(160)
        elif(index==3413):
            rule_num.append(161)
        elif(index==3421):
            rule_num.append(162)
        elif(index==3422):
            rule_num.append(163)
        elif(index==3423):
            rule_num.append(164)
        elif(index==3424):
            rule_num.append(165)
        elif(index==3425):
            rule_num.append(166)
        elif(index==3431):
            rule_num.append(167)
        elif(index==3432):
            rule_num.append(168)
        elif(index==3433):
            rule_num.append(169)
        elif(index==3434):
            rule_num.append(170)
        elif(index==3435):
            rule_num.append(171)
        elif(index==3441):
            rule_num.append(172)
        elif(index==3442):
            rule_num.append(173)
        elif(index==3443):
            rule_num.append(174)
        elif(index==3444):
            rule_num.append(175)
        elif(index==3445):
            rule_num.append(176)
        elif(index==3451):
            rule_num.append(177)
        elif(index==3452):
            rule_num.append(178)
        elif(index==3453):
            rule_num.append(179)
        elif(index==3511):
            rule_num.append(180)
        elif(index==3512):
            rule_num.append(181)
        elif(index==3513):
            rule_num.append(182)
        elif(index==3521):
            rule_num.append(183)
        elif(index==3522):
            rule_num.append(184)
        elif(index==3523):
            rule_num.append(185)
        elif(index==3524):
            rule_num.append(186)
        elif(index==3531):
            rule_num.append(187)
        elif(index==3532):
            rule_num.append(188)
        elif(index==3533):
            rule_num.append(189)
        elif(index==3534):
            rule_num.append(190)
        elif(index==3541):
            rule_num.append(191)
        elif(index==3542):
            rule_num.append(192)
        elif(index==3543):
            rule_num.append(193)
        elif(index==3544):
            rule_num.append(194)
        elif(index==4114):
            rule_num.append(195)
        elif(index==4115):
            rule_num.append(196)
        elif(index==4124):
            rule_num.append(197)
        elif(index==4125):
            rule_num.append(198)
        elif(index==4134):
            rule_num.append(199)
        elif(index==4135):
            rule_num.append(200)
        elif(index==4144):
            rule_num.append(201)
        elif(index==4145):
            rule_num.append(202)
        elif(index==4154):
            rule_num.append(203)
        elif(index==4155):
            rule_num.append(204)
        elif(index==4214):
            rule_num.append(205)
        elif(index==4215):
            rule_num.append(206)
        elif(index==4223):
            rule_num.append(207)
        elif(index==4224):
            rule_num.append(208)
        elif(index==4225):
            rule_num.append(209)
        elif(index==4233):
            rule_num.append(210)
        elif(index==4234):
            rule_num.append(211)
        elif(index==4235):
            rule_num.append(212)
        elif(index==4243):
            rule_num.append(213)
        elif(index==4244):
            rule_num.append(214)
        elif(index==4245):
            rule_num.append(215)
        elif(index==4253):
            rule_num.append(216)
        elif(index==4254):
            rule_num.append(217)
        elif(index==4255):
            rule_num.append(218)
        elif(index==4312):
            rule_num.append(219)
        elif(index==4313):
            rule_num.append(220)
        elif(index==4314):
            rule_num.append(221)
        elif(index==4315):
            rule_num.append(222)
        elif(index==4322):
            rule_num.append(223)
        elif(index==4323):
            rule_num.append(224)
        elif(index==4324):
            rule_num.append(225)
        elif(index==4325):
            rule_num.append(226)
        elif(index==4332):
            rule_num.append(227)
        elif(index==4333):
            rule_num.append(228)
        elif(index==4334):
            rule_num.append(229)
        elif(index==4342):
            rule_num.append(230)
        elif(index==4343):
            rule_num.append(231)
        elif(index==4344):
            rule_num.append(232)
        elif(index==4352):
            rule_num.append(233)
        elif(index==4353):
            rule_num.append(234)
        elif(index==4354):
            rule_num.append(235)
        elif(index==4412):
            rule_num.append(236)
        elif(index==4413):
            rule_num.append(237)
        elif(index==4414):
            rule_num.append(238)
        elif(index==4421):
            rule_num.append(239)
        elif(index==4422):
            rule_num.append(240)
        elif(index==4423):
            rule_num.append(241)
        elif(index==4424):
            rule_num.append(242)
        elif(index==4431):
            rule_num.append(243)
        elif(index==4432):
            rule_num.append(244)
        elif(index==4433):
            rule_num.append(245)
        elif(index==4434):
            rule_num.append(246)
        elif(index==4441):
            rule_num.append(247)
        elif(index==4442):
            rule_num.append(248)
        elif(index==4443):
            rule_num.append(249)
        elif(index==4444):
            rule_num.append(250)
        elif(index==4451):
            rule_num.append(251)
        elif(index==4452):
            rule_num.append(252)
        elif(index==4453):
            rule_num.append(253)
        elif(index==4511):
            rule_num.append(254)
        elif(index==4512):
            rule_num.append(255)
        elif(index==4513):
            rule_num.append(256)
        elif(index==4521):
            rule_num.append(257)
        elif(index==4522):
            rule_num.append(258)
        elif(index==4523):
            rule_num.append(259)
        elif(index==4531):
            rule_num.append(260)
        elif(index==4532):
            rule_num.append(261)
        elif(index==4533):
            rule_num.append(262)
        elif(index==4541):
            rule_num.append(263)
        elif(index==4542):
            rule_num.append(264)
        elif(index==4543):
            rule_num.append(265)
        elif(index==4544):
            rule_num.append(266)
        elif(index==5115):
            rule_num.append(267)
        elif(index==5125):
            rule_num.append(268)
        elif(index==5135):
            rule_num.append(269)
        elif(index==5214):
            rule_num.append(270)
        elif(index==5215):
            rule_num.append(271)
        elif(index==5224):
            rule_num.append(272)
        elif(index==5225):
            rule_num.append(273)
        elif(index==5313):
            rule_num.append(274)
        elif(index==5314):
            rule_num.append(275)
        elif(index==5315):
            rule_num.append(276)
        elif(index==5323):
            rule_num.append(277)
        elif(index==5324):
            rule_num.append(278)
        elif(index==5325):
            rule_num.append(279)
        elif(index==5412):
            rule_num.append(280)
        elif(index==5413):
            rule_num.append(281)
        elif(index==5414):
            rule_num.append(282)
        elif(index==5422):
            rule_num.append(283)
        elif(index==5423):
            rule_num.append(284)
        elif(index==5424):
            rule_num.append(285)
        elif(index==5511):
            rule_num.append(286)
        elif(index==5512):
            rule_num.append(287)
        elif(index==5513):
            rule_num.append(288)
        elif(index==5521):
            rule_num.append(289)
        elif(index==5522):
            rule_num.append(290)
        elif(index==5523):
            rule_num.append(291)

    return rule_num



# 記述したいデータのインポート
dataset = np.loadtxt(
    fname = "data/cartpole/experiment_from_output_keep-only-13_6.csv",
    dtype = "float",
    delimiter = ",",
)


rule_num = 291 +1# 記述したいファジィ制御器のルール数

# 各ルールが適用された回数を入れる配列
rule = np.zeros(rule_num) # 立たせる挙動
rule_center = np.zeros(rule_num) # 中間の挙動
rule_keep = np.zeros(rule_num) # キープの挙動


counter = 0

# 各ルールが適用された回数を調べる
for ele in dataset:

    # 該当するルールを集める
    apply_rule_index = [] # そのデータが該当するメンバーシップ関数のインデックス

    x_1 = get_number_input(ele[0])
    x_2 = get_number_input(ele[1])
    x_3 = get_number_input3(ele[2])
    x_4 = get_number_input(ele[3])

    for x1 in x_1:
        for x2 in x_2:
            for x3 in x_3:
                for x4 in x_4:
                    tmp = 1000*x1 + 100*x2 + 10*x3 + x4
                    apply_rule_index.append(tmp)


    # ルールが該当した回数をカウントする
    apply_rule = rule_search(apply_rule_index)

    # 適用された回数を入れる配列を更新する
    if(counter<50):
        for num in apply_rule:
            rule[num] = rule[num] + 1
    elif(50<=counter<=125):
        for num in apply_rule:
            rule_center[num] = rule_center[num] + 1
    else:
        for num in apply_rule:
            rule_keep[num] = rule_keep[num] + 1

    counter += 1

rule = rule.tolist()
rule_center = rule_center.tolist()
rule_keep = rule_keep.tolist()


# 各フェーズの中で該当した回数の多いルールTOP3を出力する

print("＊立たせる挙動")
top1 = rule.index(max(rule))
print(top1)
rule[top1] = 0
top2 = rule.index(max(rule))
print(top2)
rule[top2] = 0
top3 = rule.index(max(rule))
print(top3)

print("＊中間の挙動")
top1 = rule_center.index(max(rule_center))
print(top1)
rule_center[top1] = 0
top2 = rule_center.index(max(rule_center))
print(top2)
rule_center[top2] = 0
top3 = rule_center.index(max(rule_center))
print(top3)

print("＊キープの挙動")
top1 = rule_keep.index(max(rule_keep))
print(top1)
rule_keep[top1] = 0
top2 = rule_keep.index(max(rule_keep))
print(top2)
rule_keep[top2] = 0
top3 = rule_keep.index(max(rule_keep))
print(top3)




