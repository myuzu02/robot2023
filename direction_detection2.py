# -*- coding: utf-8 -*-

import cv2
import numpy as np

def main():

#   src_img = cv2.imread( "2023_sei1.png" )
    src_img = cv2.imread( "2023_gyaku1.png" )
#   src_img = cv2.imread( "2023_noboard.png" )
#   src_img = cv2.imread( "2023_palette.png" )
#   src_img = cv2.imread( "2023_nopalette.png" )
#   src_img = cv2.imread( "2023_ng1.png" )
#   src_img = cv2.imread( "2023_ng2.png" )
#   src_img = cv2.imread( "2023_ng3.png" )
#   src_img = cv2.imread( "2023_ng4.png" )
#   src_img = cv2.imread( "2023_ng5.png" )
    
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

    # テンプレート画像の読み込み
    temprate_img = cv2.imread( "2023_switch_temp.png" )

    Capture_size_r, Capture_size_c, Capture_size_color = src_img.shape   # 入力画像の高さ、幅、（色）を取得
    print( src_img.shape )

    pixel_mag = 1.0
    pixel_mag = Capture_size_r/480*1.0;	   # 画素数680:480を1.0としたときの入力画像の倍率を求める
    #print( pixel_mag )
#   座標の初期値は画素数640:480を基準として設定

    sw_offset = int( Capture_size_c/2 )	# 検査範囲　1回目：終点(左端)　2回目：始点(右端)

# 入力画像の高さ、幅、色を取得
    model_size_r, model_size_c, model_size_color = temprate_img.shape
# テンプレート画像を、入力画像の大きさに合わせてresizeする
    temprate_img = cv2.resize( temprate_img , ( int( model_size_c*pixel_mag ), int( model_size_r*pixel_mag ) ) )

    sw_match_threshold = 0.5	# スイッチのパターンマッチングの一致率しきい値


# 画像処理
    hsv_img = cv2.cvtColor( src_img, cv2.COLOR_BGR2HSV )	# HSVに変換する。
    split_img = cv2.split( hsv_img )	


# 正向き判定　タクトスイッチの位置を判定する。
    #cropped_img = src_img
    cropped_img = src_img[:, :sw_offset]
    #print( cropped_img.shape )
    temprate_img = cv2.cvtColor( temprate_img,cv2.COLOR_BGR2GRAY )
    cropped_img = cv2.cvtColor( cropped_img,cv2.COLOR_BGR2GRAY )
#   cv2.imshow( "sw F image", cropped_img )
    res = cv2.matchTemplate( cropped_img, temprate_img, cv2.TM_CCOEFF_NORMED )	# テンプレートマッチング
    h, w = temprate_img.shape[::-1]
    cropped_img = cv2.cvtColor( cropped_img, cv2.IMREAD_GRAYSCALE )
    sw_result = 0

    value = 0
    while True:
        # 結果が最大、最小の位置を検出
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print("MaxValue = ", max_val)

        if max_val < sw_match_threshold:
            break
        value = value + 1

        # 検出位置を描画
        cv2.rectangle(cropped_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 3)
        # 検出した位置の近辺の値を０にする
        range = 10
        cv2.rectangle(res, (max_loc[0] - range, max_loc[1] - range), (max_loc[0] + range, max_loc[1] + range), 0, -1)

    print("検出数", value)
    #print( "match result F:", sw_result)
    if value == 2:	# SWを検出した値がある程度以上だったら、
        cv2.imshow( "result F match", cropped_img )
        cv2.imshow("Template", temprate_img)
        #cv2.imshow("Template Result", res / max_val)
        print( "順方向" )

    else:
        #print( "範囲を変更して再検査" )
        cropped_img = src_img[:, 320:]
        print( cropped_img.shape )
        cropped_img = cv2.cvtColor( cropped_img,cv2.COLOR_BGR2GRAY )
        #cv2.imshow( "sw F image", cropped_img )
        res = cv2.matchTemplate( cropped_img, temprate_img, cv2.TM_CCOEFF_NORMED )	# テンプレートマッチング
        cropped_img = cv2.cvtColor( cropped_img, cv2.IMREAD_GRAYSCALE )
        sw_result = 0

        value = 0
        while True:
            # 結果が最大、最小の位置を検出
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print("MaxValue = ", max_val)

            if max_val < sw_match_threshold:
                break
            value = value + 1

            # 検出位置を描画
            cv2.rectangle(cropped_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 3)
            # 検出した位置の近辺の値を０にする
            range = 10
            cv2.rectangle(res, (max_loc[0] - range, max_loc[1] - range), (max_loc[0] + range, max_loc[1] + range), 0, -1)

        print("検出数", value)
        #print( "match result F:", sw_result)
        if value == 2:
            cv2.imshow( "result F match", cropped_img )
            cv2.imshow("Template", temprate_img)
            #cv2.imshow("Template Result", res / max_val)
            print( "逆方向" )

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