# -*- coding: utf-8 -*-

import cv2
import numpy as np
import mylib

# GPIOを設定する。
# 入力に設定するGPIO番号を外部からの入力の順に記述する。
# ピン数は4個である。
def pin_init():
    # 入力関係の値の設定
    ACT = 0					# 能動状態の値 (INACTの逆)
    INACT = 1				# 非能動状態の値 (ACTの逆)
    CONT_REQ = 4			# ロボットコントローラからの連続運転指示ビットの番号　GPIOの何番を使用するか指定する。
    D_IN = [4, 5, 6, 7]		# GPIO4をD_IN0、GPIO5をD_IN1、GPIO6をD_IN2、GPIO7をD_IN3にする。

    # 要素0:CB05からの画像処理要求　ACTIVEなら、画像処理を継続して結果をGPIOに出力する。INACTIVEになったら、画像処理を停止してGPIOの値を固定する。
    return D_IN, ACT, INACT, CONT_REQ	# D_IN、ACT、INACT、CONT_REQを返す。


# GPIOを設定する。
# 入力に設定するGPIO番号を外部からの入力の順に記述する。
# ピン数は4個である。
def pout_init():
    # 出力関係の値の設定
    D_OUT = [17, 18, 19, 20]	# GPIO17をD_OUT0、GPIO18をD_OUT1、GPIO19をD_OUT2、GPIO20をD_OUT3にする。

    return D_OUT	# D_OUTを返す。


# 画像処理用関数
# ここでいろいろな処理をして、ワークの有無、ワークの向き、パレットの有無を返す。
# 引数src_imgはカメラから読み込んだ画像
# 戻り値は画像処理した結果
def image_process( src_img ):
#	src_img = cv2.imread( "presence_forward.png" )
#	src_img = cv2.imread( "presence_reverse.png" )
#	src_img = cv2.imread( "RFIDpalette.png" )
#	src_img = cv2.imread( "no_work.png" )

#   src_img = cv2.imread( "sei1.png" )
#   src_img = cv2.imread( "sei2.png" )
#   src_img = cv2.imread( "gyaku1.png" )
#   src_img = cv2.imread( "gyaku2.png" )
#   src_img = cv2.imread( "sei2_swnon.png" )
#   src_img = cv2.imread( "pos12_sei_rl.png" )

    # 有無、順逆でそれぞれ1にするか0にするかをハードウェア、CB05とのインターフェースによって設定する。
    Finish = 1      #終了
    Halfway = 0     #途中
    Presence = 1	# 有
    Absence = 0		# 無
    Forward = 1		# 順方向
    Reverse = 0		# 逆方向
    DoNotCare = -1	# 未使用
	
#   Capture_size_r = 480
#   Capture_size_c = 640

    Capture_size_r, Capture_size_c, Capture_size_color = src_img.shape   # 入力画像の高さ、幅、（色）を取得
    pixel_mag = 1.0;
    pixel_mag = Capture_size_r/480*1.0;		# 画素数680:480を1.0としたときの入力画像の倍率を求める
#   print( pixel_mag )
    # 座標の初期値は画素数640:480を基準として設定

    # 色相範囲(角度)　0～255の範囲でしか表せないため1/2で表す
    blue_low = 100	# パレットの青の色相範囲の下限(角度)　200度
    blue_high = 140	# パレットの青の上限　280度
    green_low = 70	# 基板の緑
    green_high = 85
    red_low = 10	# 赤LEDの色相の下限　赤の範囲は20度から0度経由の340度の範囲
    red_high = 170


    # 画像処理
    hsv_img = cv2.cvtColor( src_img, cv2.COLOR_BGR2HSV )	# HSVに変換する。
    split_img = cv2.split( hsv_img )						# SHVの各チャンネルに分離する。

    #撮影位置    0:基板    1:パレット
    if mylib.read_gpio(5) == 0:

        result = [DoNotCare, DoNotCare, DoNotCare, DoNotCare]	#  結果の初期値は、全て「未使用」とする。

        # 基板有無判定　緑の面積が広かったら基板があるとみなす。
        hue_img = cv2.inRange( split_img[0], green_low, green_high )	# しきい値内の色相を抽出	
        sat_img = cv2.inRange( split_img[1], 128, 255 )					# しきい値以上の彩度を抽出
        green_img = cv2.bitwise_and( hue_img, sat_img )					# 色相と彩度のandを取る
        pixel_sum = cv2.reduce( green_img, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F )/255	# 各行の和を求める。
        pixel_sum = cv2.reduce( pixel_sum, 0, cv2.REDUCE_SUM, dtype=cv2.CV_64F )		# 各列の和を求める。

        if pixel_sum > (90000*pixel_mag**2):	# 緑の面積がある程度以上だったら、
            result[1] = Presence
        else:
            result[1] = Absence

    else:
         # パレット有無判定
        hue_img = cv2.inRange( split_img[0], blue_low, blue_high )
        sat_img = cv2.inRange( split_img[1], 180, 255 )
        blue_img = cv2.bitwise_and( hue_img, sat_img )
        pixel_sum = cv2.reduce( blue_img, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F )/255	# 各行の和を求める。
        pixel_sum = cv2.reduce( pixel_sum, 0, cv2.REDUCE_SUM, dtype=cv2.CV_64F )	# 各列の和を求める。

        if pixel_sum > (180000.0*pixel_mag**2):	# 青の面積がある程度以上だったら、
            result[3] = Presence	# パレット有り
        else:
            result[3] = Absence		# パレット無し


    # ここまで

#   result[0] = finish      # 画像処理終了信号  Halfway:画像処理途中　　Finish:画像処理終了
#   result[1] = Presence    # 仮の結果          Absence:ワークがない    Presence:ワークがある
#   result[2] = Forward     # 仮の結果          Reverse:ワークが逆向き  Forward: ワークが順向き
#   result[3] = Presence    # 仮の結果          Absence:パレットがない  Presence:パレットがある

#   print( "Result", result )

    return result