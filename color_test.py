# -*- coding: utf-8 -*-

import cv2
import numpy as np

def main():

    src_img = cv2.imread( "2023_sei1.png" )
#   src_img = cv2.imread( "2023_gyaku1.png" )
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
    temp_img = cv2.imread( "2023_switch_temp.png" )

    #青を抽出
    #bgr = [210, 150, 40]
    #thresh = 40
    #赤を抽出
    #bgr = [-30,-30,150]
    #thresh = 40

    #色の閾値
    #minBGR = np.array([bgr[0] - thresh, bgr[1] - thresh, bgr[2] - thresh])
    #maxBGR = np.array([bgr[0] + thresh, bgr[1] + thresh, bgr[2] + thresh])

    #画像の2値化
    #maskBGR = cv2.inRange(src_img,minBGR,maxBGR)
    #画像のマスク（合成）
    #resultBGR = cv2.bitwise_and(src_img, src_img, mask = maskBGR)

    b = temp_img[:, :, 0]
    g = temp_img[:, :, 1]
    r = temp_img[:, :, 2]

    blue_img = src_img[:, :, 0]
    res = cv2.matchTemplate( blue_img, b, cv2.TM_CCOEFF_NORMED )	# テンプレートマッチング
    h, w = b.shape[::-1]
    sw_result = 0

    value = 0
    while True:
        # 結果が最大、最小の位置を検出
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print("MaxValue = ", max_val)

        if max_val < 0.5:
            break
        value = value + 1

        # 検出位置を描画
        cv2.rectangle(blue_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 3)
        # 検出した位置の近辺の値を０にする
        range = 10
        cv2.rectangle(res, (max_loc[0] - range, max_loc[1] - range), (max_loc[0] + range, max_loc[1] + range), 0, -1)

    print("検出数", value)

    cv2.imshow("Result B", b)
    cv2.imshow("Result G", g)
    cv2.imshow("Result R", r )
    #cv2.imshow("Result BGR", resultBGR)
    #cv2.imshow("Result mask", maskBGR)
    cv2.imshow( "source image", temp_img )    # 表示する。

    cv2.waitKey( 0 )	# 表示のアクションを起こす。
    cv2.destroyAllWindows()

# ここまで

if __name__=="__main__":
    main()