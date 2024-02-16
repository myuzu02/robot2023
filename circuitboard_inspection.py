# -*- coding: utf-8 -*-

import cv2
import numpy as np

def main():

#   src_img = cv2.imread( "2023_sei1.png" )
#   src_img = cv2.imread( "2023_noboard.png" )
#   src_img = cv2.imread( "2023_ng3.png" )
#   src_img = cv2.imread( "2023_paretto.png" )
    src_img = cv2.imread( "2023_noparetto.png" )

#   src_img = cv2.imread( "presence_forward.png" )
#   src_img = cv2.imread( "presence_reverse.png" )
#   src_img = cv2.imread( "RFIDpalette.png" )
#   src_img = cv2.imread( "no_work.png" )

#   src_img = cv2.imread( "sei1.png" )
#   src_img = cv2.imread( "sei2.png" )
#   src_img = cv2.imread( "gyaku1.png" )
#   src_img = cv2.imread( "gyaku2.png" )
#   src_img = cv2.imread( "sei2_swnon.png" )
#   src_img = cv2.imread( "pos12_sei_rl.png" )

    Capture_size_r, Capture_size_c, Capture_size_color = src_img.shape   # 入力画像の高さ、幅、（色）を取得

    pixel_mag = 1.0
    pixel_mag = Capture_size_r/480*1.0;	   # 画素数680:480を1.0としたときの入力画像の倍率を求める
    print( pixel_mag )
#   座標の初期値は画素数640:480を基準として設定

    green_low = 70	# 基板の緑
    green_high = 85    
    # 色相範囲(角度)　0～255の範囲でしか表せないため1/2で表す
    blue_low = 100	# パレットの青の色相範囲の下限(角度)　200度
    blue_high = 140	# パレットの青の上限　280度

    # 画像処理
    hsv_img = cv2.cvtColor( src_img, cv2.COLOR_BGR2HSV )	# HSVに変換する。
    split_img = cv2.split( hsv_img )	

    # 基板有無判定　緑の面積が広かったら基板があるとみなす。
    hue_img = cv2.inRange( split_img[0], green_low, green_high )	# しきい値内の色相を抽出	
    sat_img = cv2.inRange( split_img[1], 128, 255 )					# しきい値以上の彩度を抽出
    green_img = cv2.bitwise_and( hue_img, sat_img )					# 色相と彩度のandを取る
    pixel_sum = cv2.reduce( green_img, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F )/255	# 各行の和を求める。
    pixel_sum = cv2.reduce( pixel_sum, 0, cv2.REDUCE_SUM, dtype=cv2.CV_64F )		# 各列の和を求める。
#   print( "Green pixels number:", pixel_sum[0][0] )
#   cv2.imshow( "hue image", hue_img )
#   cv2.imshow( "saturation image", sat_img )
    cv2.imshow( "green image", green_img )

    cv2.imshow( "source image", src_img )

    if pixel_sum > (90000*pixel_mag**2):	# 緑の面積がある程度以上だったら、
        print( "基板有り" )
    else:
        print( "基板無し" )			

    # パレット有無判定
    hue_img = cv2.inRange( split_img[0], blue_low, blue_high )
    sat_img = cv2.inRange( split_img[1], 180, 255 )
    blue_img = cv2.bitwise_and( hue_img, sat_img )
    pixel_sum = cv2.reduce( blue_img, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F )/255	# 各行の和を求める。
    pixel_sum = cv2.reduce( pixel_sum, 0, cv2.REDUCE_SUM, dtype=cv2.CV_64F )	# 各列の和を求める。

    if pixel_sum > (10000.0*pixel_mag**2):	# 青の面積がある程度以上だったら、
        print( "パレット有り" )
    else:
        print( "パレット無し" )

#   gray_img = cv2.cvtColor( src_img, cv2.COLOR_BGR2GRAY )		# グレースケールに変換する。
#   zeros = gray_img * 0										# オール0の画像を生成する。
#   split_img = cv2.split( src_img )							# カラー画像をBGRの3枚に分離する。
#   blue_img = cv2.merge( ( split_img[0], zeros, zeros ) )		# 青画像を作成する。
#   green_img = cv2.merge( ( zeros, split_img[1], zeros ) )		# 緑画像を作成する。
#   red_img = cv2.merge( ( zeros, zeros, split_img[2] ) )		# 赤画像を作成する。
#   inverted_img = 255 - gray_img								# 白黒反転する。

# 画像の表示は、デバッグの時だけ行う。
#   cv2.imshow( "source image", src_img )					# 表示する。
#   cv2.imshow( "gray scale image", gray_img )				# 表示する。 
#   cv2.imshow( "blue channel image", blue_img )			# 表示する。 
#   cv2.imshow( "green channel image", green_img )			# 表示する。 
#   cv2.imshow( "red channel image", red_img )				# 表示する。 
#   cv2.imshow( "gray scale inverted image", inverted_img )	# 表示する。 
#   print( "Result", result )

    cv2.waitKey( 0 )	# 表示のアクションを起こす。
    cv2.destroyAllWindows()

# ここまで

#   result[0] = finish   	# 画像処理終了信号　continue:継続中　　finish:終了
#   result[1] = Presence	# 仮の結果　Absence:ワークがない　　Presence:ワークがある
#   result[2] = Forward 	# 仮の結果　Reverse:ワークが逆向き　Forward: ワークが順向き
#   result[3] = Presence	# 仮の結果　Absence:パレットがない　　Presence:パレットがある
#   print( "Result", result )

if __name__=="__main__":
    main()