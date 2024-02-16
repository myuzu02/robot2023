# -*- coding: utf-8 -*-

import cv2
import numpy as np

def main():

#   src_img = cv2.imread( "2023_sei1.png" )
#   src_img = cv2.imread( "presence_forward.png" )
#   src_img = cv2.imread( "presence_reverse.png" )
#   src_img = cv2.imread( "RFIDpalette.png" )
#   src_img = cv2.imread( "no_work.png" )
    src_img = cv2.imread( "sei1.png" )
#   src_img = cv2.imread( "sei2.png" )
#   src_img = cv2.imread( "gyaku1.png" )
#   src_img = cv2.imread( "gyaku2.png" )
#   src_img = cv2.imread( "sei2_swnon.png" )
#   src_img = cv2.imread( "pos12_sei_rl.png" )

    temprate_img = cv2.imread( "2023_8_temp.png" )

    Capture_size_r, Capture_size_c, Capture_size_color = src_img.shape   # 入力画像の高さ、幅、（色）を取得

    pixel_mag = 1.0
    pixel_mag = Capture_size_r/480*1.0;	   # 画素数680:480を1.0としたときの入力画像の倍率を求める
    print( pixel_mag )
#   座標の初期値は画素数640:480を基準として設定


    #sw_default_ulc_fr = 60		# 基板正向き時のスイッチの検査範囲の左上座標:行成分
    #sw_default_ulc_fc = 380		# 列成分
    #sw_default_ulc_rr = 295		# 逆向き時:行成分
    #sw_default_ulc_rc = 135     # 逆向き時:列成分

    #sw_offset_fr = int( sw_default_ulc_fr*pixel_mag )	# 入力画像の画素数に合わせて処理時の座標を求める
    #sw_offset_fc = int( sw_default_ulc_fc*pixel_mag )
    #sw_offset_rr = int( sw_default_ulc_rr*pixel_mag )
    #sw_offset_rc = int( sw_default_ulc_rc*pixel_mag )


    sw_default_ulc_fr = 60		# 基板正向き時のスイッチの検査範囲の左上座標:行成分
    sw_default_ulc_fc = 380		# 列成分

    sw_offset_fr = int( sw_default_ulc_fr*pixel_mag )	# 入力画像の画素数に合わせて処理時の座標を求める
    sw_offset_fc = int( sw_default_ulc_fc*pixel_mag )

    sw_height = int( 130*pixel_mag )	# スイッチの検査範囲
    sw_width = int( 130*pixel_mag )		# スイッチの検査範囲

    model_size_r, model_size_c, model_size_color = temprate_img.shape   # 入力画像の高さ、幅、色を取得
    temprate_img = cv2.resize( temprate_img , ( int( model_size_c*pixel_mag ), int( model_size_r*pixel_mag ) ) )

    sw_match_threshold = 0.5	# スイッチのパターンマッチングの一致率しきい値


    # 画像処理
    hsv_img = cv2.cvtColor( src_img, cv2.COLOR_BGR2HSV )	# HSVに変換する。
    split_img = cv2.split( hsv_img )	


# 正向き判定　タクトスイッチの位置を判定する。
    cropped_img = src_img[sw_offset_fr:sw_offset_fr + sw_height, sw_offset_fc:sw_offset_fc + sw_width]
    temprate_img = cv2.cvtColor( temprate_img,cv2.COLOR_BGR2GRAY )
    cropped_img = cv2.cvtColor( cropped_img,cv2.COLOR_BGR2GRAY )
#   cv2.imshow( "sw F image", cropped_img )
    res = cv2.matchTemplate( cropped_img, temprate_img, cv2.TM_CCOEFF_NORMED )	# テンプレートマッチング
    loc = np.where( res >= sw_match_threshold )
    h, w = temprate_img.shape
    cropped_img = cv2.cvtColor( cropped_img, cv2.IMREAD_GRAYSCALE )
    sw_result = 0
    for pt in zip( *loc[::-1] ):	# マッチング率の高い場所表示
        cv2.rectangle( cropped_img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2 )
        sw_result += 1

    cv2.imshow( "result F match", cropped_img )
    print( "match result F:", sw_result)


    if sw_result > 0:	# 緑の面積がある程度以上だったら、
        print( "OK" )
    else:
        print( "NG" )
	

#   gray_img = cv2.cvtColor( src_img, cv2.COLOR_BGR2GRAY )		# グレースケールに変換する。
#   zeros = gray_img * 0										# オール0の画像を生成する。
#   split_img = cv2.split( src_img )							# カラー画像をBGRの3枚に分離する。
#   blue_img = cv2.merge( ( split_img[0], zeros, zeros ) )		# 青画像を作成する。
#   green_img = cv2.merge( ( zeros, split_img[1], zeros ) )		# 緑画像を作成する。
#   red_img = cv2.merge( ( zeros, zeros, split_img[2] ) )		# 赤画像を作成する。
#   inverted_img = 255 - gray_img								# 白黒反転する。

# 画像の表示は、デバッグの時だけ行う。
    cv2.imshow( "source image", src_img )					# 表示する。
#   cv2.imshow( "gray scale image", gray_img )				# 表示する。 
#   cv2.imshow( "blue channel image", blue_img )			# 表示する。 
#   cv2.imshow( "green channel image", green_img )			# 表示する。 
#   cv2.imshow( "red channel image", red_img )				# 表示する。 
#   cv2.imshow( "gray scale inverted image", inverted_img )	# 表示する。 
#   print( "Result", result )

    cv2.waitKey( 0 )	# 表示のアクションを起こす。
    cv2.destroyAllWindows()

# ここまで

#   result[0] = finish   	# 画像処理終了信号　continue:継続中　　       finish:終了
#   result[1] = Presence	# 仮の結果　        Absence:ワークがない　　  Presence:ワークがある
#   result[2] = Forward 	# 仮の結果　        Reverse:ワークが逆向き　  Forward: ワークが順向き
#   result[3] = Presence	# 仮の結果　        Absence:パレットがない    Presence:パレットがある
#   print( "Result", result )

if __name__=="__main__":
    main()