# -*- coding: utf-8 -*-

import numpy as np
import cv2
import subprocess
import time
import sys
import image_process
import mylib
import variable as g
import image_process2023

def main():
    ACT = -1		# 能動状態の値 (INACTの逆)
    INACT = -1		# 非能動状態の値 (ACTの逆)
    CONT_REQ = -1	# ロボットコントローラからの連続運転指示ビットの番号
    frame_rate = 30
    frame_width = 640
    frame_height = 480

    args = sys.argv

    mylib.global_variable_init()	# グローバル変数を初期化する。

    # P_IN[]をGPIOの番号に結び付ける。
    P_IN, ACT, INACT, CONT_REQ = image_process.pin_init()
    P_OUT = image_process.pout_init()
    in_bit_num = len( P_IN )		# 取り扱うGPIOのビット数 (入力)
    out_bit_num = len( P_OUT )		# 取り扱うGPIOのビット数 (出力)
#	print( "IN:", in_bit_num, P_IN, " OUT:", out_bit_num, P_OUT, " SIGNALs:", ACT, INACT, CONT_REQ )

    for cnt in range( in_bit_num ):
        res_gpio = mylib.use_gpio( P_IN[cnt], "in" )	# GPIOを入力モードで使用する。現在、pull upタクトスイッチが付いている。
        if res_gpio > 1:	# 警告を処理する。警告は2以上、0, 1はGPIOの値
            print( "Warning (" + str( res_gpio ) + "): GPIO" + str( P_IN[cnt] ) + " " + g.WARNING_MESSAGE[res_gpio] )
        elif res_gpio < 0:	# エラーを処理する。
            print( "Error (" + str( abs( res_gpio ) ) + "): GPIO" + str( P_IN[cnt] ) + " " + g.ERROR_MESSAGE[abs( res_gpio )] )
        else:
            print( "GPIO " + str( P_IN[cnt] ) + " opened input mode." )

    for cnt in range( out_bit_num ):
        res_gpio = mylib.use_gpio( P_OUT[cnt], "out" )	# GPIOを出力モードで使用する。現在、Hi点灯LEDが付いている。
        if res_gpio > 1:	# 警告を処理する。警告は2以上、0, 1はGPIOの値
            print( "Warning (" + str( res_gpio ) + "): GPIO" + str( P_OUT[cnt] ) + " " + g.WARNING_MESSAGE[res_gpio] )
        elif res_gpio < 0:	# エラーを処理する。
            print( "Error (" + str( abs( res_gpio ) ) + "): GPIO" + str( P_OUT[cnt] ) + " " + g.ERROR_MESSAGE[abs( res_gpio )] )
        else:
            print( "GPIO " + str( P_OUT[cnt] ) + " opened output mode." )


    #GPIOに出力する
    mylib.write_gpio( P_OUT[0], 0)
    #mylib.write_gpio( P_OUT[0], 1)
    #mylib.write_gpio( P_OUT[1], 0)
    #mylib.write_gpio( P_OUT[1], 1)
    #mylib.write_gpio( P_OUT[2], 0)
    #mylib.write_gpio( P_OUT[2], 1)
    #mylib.write_gpio( P_OUT[3], 0)
    #mylib.write_gpio( P_OUT[3], 1)

    #GPIOの状態を確認
    if ( mylib.read_gpio( CONT_REQ ) == INACT ):
        print( "非能動" )
    else:
        print( "能動" )
    if ( mylib.read_gpio(5) == 0 ):
        print( "基板撮影位置" )
    else:
        print( "パレット撮影位置" )

    src_img = cv2.imread( "2023_sei1.png" )
    result = image_process2023.image_process( src_img )
    print( result )


    for cnt in range( 4 ):
        res_gpio = mylib.unuse_gpio( P_IN[cnt] )
        if res_gpio > 1:	# 警告を処理する。警告は2以上、0, 1はGPIOの値
            print( "Warning: GPIO " + str( P_IN[cnt] ) + " (" + str( res_gpio ) + ")" )
        elif res_gpio < 0:	# エラーを処理する。
            print( "Error:   GPIO " + str( P_IN[cnt] ) + " (" + str( res_gpio ) + ")" )
        else:
            print( "GPIO " + str( P_IN[cnt] ) + " close successful." )
        res_gpio = mylib.unuse_gpio( P_OUT[cnt] )
        if res_gpio > 1:	# 警告を処理する。警告は2以上、0, 1はGPIOの値
            print( "Warning: GPIO " + str( P_OUT[cnt] ) + " (" + str( res_gpio ) + ")" )
        elif res_gpio < 0:	# エラーを処理する。
            print( "Error:   GPIO " + str( P_OUT[cnt] ) + " (" + str( res_gpio ) + ")" )
        else:
            print( "GPIO " + str( P_OUT[cnt] ) + " close successful." )



if __name__ == "__main__":
    main()