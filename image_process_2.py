# -*- coding: utf-8 -*-

# 基本的にこのファイルだけをプログラムすれば良い。

import cv2
import numpy as np

# 画像処理用関数
# ワークの有無、ワークの向き、パレットの有無を判別して結果を返す
# 引数src_imgはカメラから読み込んだ画像
# 戻り値は画像処理した結果
def image_process( src_img ):
#   src_img = cv2.imread( "presence_forward.png" )
#   src_img = cv2.imread( "presence_reverse.png" )
#   src_img = cv2.imread("RFIDpalette.png")
#   src_img = cv2.imread("no_work.png")

#   src_img = cv2.imread("sei1.png")
#   src_img = cv2.imread("sei2.png")
#   src_img = cv2.imread("gyaku1.png")
#   src_img = cv2.imread("gyaku2.png")
#   src_img = cv2.imread("sei2_swnon.png")
#   src_img = cv2.imread("pos12_sei_rl.png")

    sw_model_img = cv2.imread("switch_model.png")

    # 有無、順逆でそれぞれ1にするか0にするかをハードウェア、CB05とのインターフェースによって設定する。
    Presence = 1    # 有
    Absence = 0     # 無
    Forward = 1     # 順方向
    Reverse = 0     # 逆方向
    DoNotCare = -1  # 未使用

#   Capture_sizer = 480
#   Capture_sizec = 640

#   Capture_size_r,Caputure_size_c,Capture_size_color = size_check_img.shape   #入力画像の高さ、幅、（色）を取得

    pixel_mag = 1.0;
#   pixel_mag = Capture_size_r/480*1.0;     #画素数680：480を1.0としたときの入力画像の倍率を求める

#座標の初期値は画素数640：480を基準として設定

    led_default_ulc_fr = 357    #led正位置_左上検査座標の列成分
    led_default_ulc_fc = 130    #led正位置　行
    led_default_ulc_rr = 60     #led逆位置　列
    led_default_ulc_rc = 435    #led逆位置　行

    led_height = 80     #LEDの検査範囲
    led_width = 80

    sw_default_ulc_fr = 60      #基板正向き時のスイッチの検査範囲の左上座標:行成分
    sw_default_ulc_fc = 380     #列成分
    sw_default_ulc_rr = 295     #逆向き時：行成分
    sw_default_ulc_rc = 135

    sw_offset_fr = int( sw_default_ulc_fr*pixel_mag )   #入力画像の画素数に合わせて処理時の座標を求める
    sw_offset_fc = int( sw_default_ulc_fc*pixel_mag )
    sw_offset_rr = int( sw_default_ulc_rr*pixel_mag )
    sw_offset_rc = int( sw_default_ulc_rc*pixel_mag )

    sw_height = 130     #スイッチの検査範囲
    sw_width = 130

    sw_match_threshold = 0.5    #スイッチのパターンマッチングの一致率しきい値

    led_offset_fr = int( led_default_ulc_fr*pixel_mag )
    led_offset_fc = int( led_default_ulc_fc*pixel_mag )
    led_offset_rr = int( led_default_ulc_rr*pixel_mag )
    led_offset_rc = int( led_default_ulc_rc*pixel_mag )
    #色相範囲(角度)　0～255の範囲でしか表せないため1/2で表す
    blue_low = 100  #パレットの青の色相範囲の下限(角度)　200度
    blue_high = 140 #パレットの青の上限　280度
    green_low = 70  #基板の緑
    green_high = 85
    red_low = 10    #赤LEDの色相の下限　赤の範囲は20度から0度経由の340度の範囲
    red_high = 170

    result = [DoNotCare, DoNotCare, DoNotCare, DoNotCare]   # 結果の初期値は、全て「未使用」とする。

    # 画像処理
    hsv_img = cv2.cvtColor( src_img, cv2.COLOR_BGR2HSV )    # HSVに変換する。
    split_img = cv2.split( hsv_img )                        # SHVの各チャンネルに分離する。

    # 基板有無判定　緑の面積が広かったら基板があるとみなす。
    hue_img = cv2.inRange( split_img[0], green_low, green_high )    #しきい値内の色相を抽出
    sat_img = cv2.inRange( split_img[1], 128, 255 )                 #しきい値以上の彩度を抽出
    green_img = cv2.bitwise_and( hue_img,sat_img )                  # 色相と彩度のandを取る
    pixel_sum = cv2.reduce( green_img, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F )/255    # 各行の和を求める。
    pixel_sum = cv2.reduce( pixel_sum, 0, cv2.REDUCE_SUM, dtype=cv2.CV_64F )        # 各列の和を求める。
    #print( "Green pixels number:", pixel_sum[0][0] )
    #cv2.imshow( "hue image", hue_img )
    #cv2.imshow( "hue", split_img[0] )
    #cv2.imshow( "saturation image", sat_img )
    #cv2.imshow( "green image", green_img )

    if pixel_sum > (90000*pixel_mag):   # 緑の面積がある程度以上だったら、
        # 正向き判定　赤のLEDの位置で向きを判定する。
        cropped_img = split_img[0][led_offset_fr:led_offset_fr + led_height, led_offset_fc:led_offset_fc + led_width]   # LED$$
        red_img = cv2.inRange( cropped_img, red_low, red_high )                 # 赤ではない範囲を抜き出す。
        #red_img = cv2.bitwise_not( red_img )                                   # 赤ではない範囲が抽出されるので、反転して赤の$
        pixel_sum = cv2.reduce( red_img, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F )/255  # 各行の和を求める。
        pixel_sum = cv2.reduce( pixel_sum, 0, cv2.REDUCE_SUM, dtype=cv2.CV_64F )    # 各列の和を求める。
#       print( "red pixels F number:", led_height*led_width - pixel_sum[0][0] )
#       cv2.imshow( "red F image", red_img )
#       cv2.imshow( "red hue F image", cropped_img )
        if led_height*led_width - pixel_sum > (700*pixel_mag) : # 所定の場所 (順位置) に赤LEDがったら、
            #正向き判定　タクトスイッチの位置を判定する。
            cropped_img = src_img[sw_offset_fr:sw_offset_fr + sw_height, sw_offset_fc:sw_offset_fc + sw_width]
            sw_model_img = cv2.cvtColor(sw_model_img,cv2.COLOR_BGR2GRAY)
            cropped_img = cv2.cvtColor(cropped_img,cv2.COLOR_BGR2GRAY)
#           cv2.imshow( "sw f image", cropped_img )
            res = cv2.matchTemplate(cropped_img, sw_model_img, cv2.TM_CCOEFF_NORMED)    #テンプレートマッチング
            loc = np.where(res >= sw_match_threshold)
            h, w = sw_model_img.shape
            cropped_img = cv2.cvtColor( cropped_img, cv2.IMREAD_GRAYSCALE)
            sw_result = 0
            for pt in zip(*loc[::-1]):  #マッチング率の高い場所表示
                cv2.rectangle(cropped_img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                sw_result += 1;
#           cv2.imshow("result F match",cropped_img)
#           print( "match result F:", sw_result)
            if sw_result >0  :
                result[0] = Presence    # 基板有り
            result[0] = Presence    # 基板有り
            result[1] = Forward     # 順方向
            sw_result = 0;

        else :
            # 逆向き判定　赤のLEDの位置で向きを判定する。
            cropped_img = split_img[0][led_offset_rr:led_offset_rr + led_height, led_offset_rc:led_offset_rc + led_width]   # $
            cropped_src_img = src_img[led_offset_rr:led_offset_rr + led_height, led_offset_rc:led_offset_rc + led_width]
#           cv2.imshow( "cropped src R image", cropped_src_img )
            red_img = cv2.inRange( cropped_img, red_low, red_high )                 # 赤ではない範囲を抜き出す。
            #red_img = cv2.bitwise_not( red_img )                                   # 赤ではない範囲が抽出されるので、反転して$
            pixel_sum = cv2.reduce( red_img, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F )/255  # 各行の和を求める。
            pixel_sum = cv2.reduce( pixel_sum, 0, cv2.REDUCE_SUM, dtype=cv2.CV_64F )    # 各列の和を求める。
#           print( "red pixels R number:", led_height*led_width - pixel_sum[0][0] )
#           cv2.imshow( "red  R image", red_img )
#           cv2.imshow( "red hue R image", cropped_img )

            if led_height*led_width - pixel_sum > (700*pixel_mag) : # 所定の場所 (逆位置) に赤LEDがあったら、
                #逆向き判定　タクトスイッチの位置を判定する。
                cropped_img = src_img[sw_offset_rr:sw_offset_rr + sw_height, sw_offset_rc:sw_offset_rc + sw_width]
                sw_model_img = cv2.cvtColor(sw_model_img,cv2.COLOR_BGR2GRAY)
                cropped_img = cv2.cvtColor(cropped_img,cv2.COLOR_BGR2GRAY)
#               cv2.imshow( "sw f image", cropped_img )
                res = cv2.matchTemplate(cropped_img, sw_model_img, cv2.TM_CCOEFF_NORMED)    #テンプレートマッチング
                loc = np.where(res >= sw_match_threshold)
                h, w = sw_model_img.shape   #モデル画像の高さ、幅を取得（四角の描画に利用）
                cropped_img = cv2.cvtColor( cropped_img, cv2.IMREAD_GRAYSCALE)
                sw_result = 0
                for pt in zip(*loc[::-1]):  #マッチング率の高い場所表示
                    cv2.rectangle(cropped_img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                    sw_result += 1;
#               cv2.imshow("result R match",cropped_img)
#               print("match result R",sw_result)
                if sw_result > 0 :
                    result[0] = Presence    # 基板有り
                    result[1] = Reverse     # 逆方向
                else :
                    result[0] = Absence # 基板無し
    else :
        # パレット有無判定
        hue_img = cv2.inRange( split_img[0], blue_low, blue_high )      #
        sat_img = cv2.inRange( split_img[1], 180, 255 )
        blue_img = cv2.bitwise_and( hue_img, sat_img )
        pixel_sum = cv2.reduce( blue_img, 1, cv2.REDUCE_SUM, dtype=cv2.CV_64F )/255 # 各行の和を求める。
        pixel_sum = cv2.reduce( pixel_sum, 0, cv2.REDUCE_SUM, dtype=cv2.CV_64F )    # 各列の和を求める。
        #print( "Blue pixels number:", pixel_sum[0][0] )
        #cv2.imshow( "hue image", hue_img )
        #cv2.imshow( "saturation image", sat_img )
        #cv2.imshow( "blue image", blue_img )

        if pixel_sum > (180000.0*pixel_mag) :   # 青の面積がある程度以上だったら、
            result[0] = Absence     # 基板無し
            result[1] = Presence    # パレット有り
        else :
            result[0] = Absence     # 基板無し
            result[1] = Absence     # パレット無し

#   gray_img = cv2.cvtColor( src_img, cv2.COLOR_BGR2GRAY )      # グレースケールに変換する。
#   zeros = gray_img * 0                                        # オール0の画像を生成する。
#   split_img = cv2.split( src_img )                            # カラー画像をBGRの3枚に分離する。
#   blue_img = cv2.merge( ( split_img[0], zeros, zeros ) )      # 青画像を作成する。
#   green_img = cv2.merge( ( zeros, split_img[1], zeros ) )     # 緑画像を作成する。
#   red_img = cv2.merge( ( zeros, zeros, split_img[2] ) )       # 赤画像を作成する。
#   inverted_img = 255 - gray_img                               # 白黒反転する。

    # 画像の表示は、デバッグの時だけ行う。
#   cv2.imshow( "source image", src_img )   # 表示する。
#   cv2.imshow( "gray scale image", gray_img )                  # 表示する。
    #cv2.imshow( "blue channel image", blue_img )               # 表示する。
    #cv2.imshow( "green channel image", green_img )             # 表示する。
    #cv2.imshow( "red channel image", red_img )                 # 表示する。
    #cv2.imshow( "gray scale inverted image", inverted_img )    # 表示する。
#   print( "Result", result )

    cv2.waitKey( 1 )    # 表示のアクションを起こす。
    # ここまで

#   result[0] = Presence    # 仮の結果　Absence:ワークがない　　Presence:ワークがある
#   result[1] = Forward     # 仮の結果　Reverse:ワークが逆向き　Forward: ワークが順向き
#   result[2] = DoNotCare   # 仮の結果　Absence:パレットがない　　Presence:パレットがある
#   result[3] = DoNotCare   # 使用しない。

#   print( "Result", result )

    return result