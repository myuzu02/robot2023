#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import subprocess
import time
import sys
import image_process
import mylib
import variable as g

def main():
        ACT = -1                # 能動状態の値 (INACTの逆)
        INACT = -1              # 非能動状態の値 (ACTの逆)
        CONT_REQ = -1   # ロボットコントローラからの連続運転指示ビットの番号
        frame_rate = 30	#1秒ごとの処理数
        frame_width = 640	#画像サイズ
        frame_height = 480

        args = sys.argv

        for cnt in range( 1, len( args ) ):
                if ( args[cnt][0:3] == "-fr" ):
                        cnt = cnt + 1
                        if cnt < len( args ):
                                frame_rate = int( args[cnt] )
                elif ( args[cnt][0:13] == "--frame-rate=" ):
                        frame_rate = int( args[cnt][13:] )
                elif ( args[cnt][0:2] == "-w" ):
                        cnt = cnt + 1
                        if cnt < len( args ):
                                frame_width = int( args[cnt] )
                elif ( args[cnt][0:8] == "--width=" ):
                        frame_width = int( args[cnt][8:] )
                elif ( args[cnt][0:2] == "-h" ):
                        cnt = cnt + 1
                        if cnt < len( args ):
                                if args[cnt].isdecimal():
                                        frame_height = int( args[cnt] )
                                else:
                                        # ヘルプメッセージを表示する。
                                        print( "HELP!!" )
                        else:
                                # ヘルプメッセージを表示する。
                                print( "HELP!!" )
                elif ( args[cnt][0:9] == "--height=" ):
                        frame_height = int( args[cnt][9:] )
                elif ( args[cnt][0:2] == "-s" ):
                        cnt = cnt + 1
                        if cnt < len( args ):
                                if ',' in args[cnt]:
                                        frame_width, frame_height = args[cnt].split( ',' )
                                        frame_width = int( frame_width )
                                        frame_height = int( frame_height )
                                elif ':' in args[cnt]:
                                        frame_width, frame_height = args[cnt].split( ':' )
                                        frame_width = int( frame_width )
                                        frame_height = int( frame_height )
                                elif 'x' in args[cnt]:
                                        frame_width, frame_height = args[cnt].split( 'x' )
                                        frame_width = int( frame_width )
                                        frame_height = int( frame_height )
                elif ( args[cnt][0:7] == "--size=" ):
                        if ',' in args[cnt][7:]:
                                frame_width, frame_height = args[cnt][7:].split( ',' )
                                frame_width = int( frame_width )
                                frame_height = int( frame_height )
                        elif ':' in args[cnt][7:]:
                                frame_width, frame_height = args[cnt][7:].split( ':' )
                                frame_width = int( frame_width )
                                frame_height = int( frame_height )
                        elif 'x' in args[cnt][7:]:
                                frame_width, frame_height = args[cnt][7:].split( 'x' )
                                frame_width = int( frame_width )
                                frame_height = int( frame_height )

        print( "Frame Rate:", frame_rate, "\nFrame Size:", frame_width, "x", frame_height )

        mylib.global_variable_init()    # グローバル変数を初期化する。

        # P_IN[]をGPIOの番号に結び付ける。
        P_IN, ACT, INACT, CONT_REQ = image_process.pin_init()
        P_OUT = image_process.pout_init()
        in_bit_num = len( P_IN )                # 取り扱うGPIOのビット数 (入力)
        out_bit_num = len( P_OUT )              # 取り扱うGPIOのビット数 (出力)
#       print( "IN:", in_bit_num, P_IN, " OUT:", out_bit_num, P_OUT, " SIGNALs:", ACT, INACT, CONT_REQ )

        for cnt in range( in_bit_num ):
                res_gpio = mylib.use_gpio( P_IN[cnt], "in" )    # GPIOを入力モードで使用する。現在、pull upタクトスイッチが付いて いる。
                if res_gpio > 1:        # 警告を処理する。警告は2以上、0, 1はGPIOの値
                        print( "Warning (" + str( res_gpio ) + "): GPIO" + str( P_IN[cnt] ) + " " + g.WARNING_MESSAGE[res_gpio] )
                elif res_gpio < 0:      # エラーを処理する。
                        print( "Error (" + str( abs( res_gpio ) ) + "): GPIO" + str( P_IN[cnt] ) + " " + g.ERROR_MESSAGE[abs( res_gpio )] )
                else:
                        print( "GPIO " + str( P_IN[cnt] ) + " opened input mode." )

        for cnt in range( out_bit_num ):
                res_gpio = mylib.use_gpio( P_OUT[cnt], "out" )  # GPIOを出力モードで使用する。現在、Hi点灯LEDが付いている。
                if res_gpio > 1:        # 警告を処理する。警告は2以上、0, 1はGPIOの値
                        print( "Warning (" + str( res_gpio ) + "): GPIO" + str( P_OUT[cnt] ) + " " + g.WARNING_MESSAGE[res_gpio] )
                elif res_gpio < 0:      # エラーを処理する。
                        print( "Error (" + str( abs( res_gpio ) ) + "): GPIO" + str( P_OUT[cnt] ) + " " + g.ERROR_MESSAGE[abs( res_gpio )] )
                else:
                        print( "GPIO " + str( P_OUT[cnt] ) + " opened output mode." )

        """ # IO test START

        # LEDの点灯テスト
        for cnt in range( out_bit_num ):
                res_gpio = mylib.write_gpio( P_OUT[cnt], 1 )    # LEDを点灯する。
                if res_gpio > 1:        # 警告を処理する。警告は2以上、0, 1はGPIOの値
                        print( "Warning (" + str( res_gpio ) + "): LED " + str( cnt ) + " " + g.WARNING_MESSAGE[res_gpio] )
                elif res_gpio < 0:      # エラーを処理する。
                        print( "Error (" + str( abs( res_gpio ) ) + "): LED " + str( cnt ) + " " + g.ERROR_MESSAGE[abs( res_gpio)] )
                else:
                        time.sleep( 1 ) # 時間待ち
                        mylib.write_gpio( P_OUT[cnt], 0 )       # LEDを消灯する。点灯の時に確認しているのでエラーチェックは省略し た。

        # スイッチの状態テスト
        switch_status = ["PUSHED", "RELEASED"]

        for cnt in range( in_bit_num ):
                res_gpio = mylib.read_gpio( P_IN[cnt] )
                if res_gpio > 1:        # 警告を処理する。警告は2以上、0, 1はGPIOの値
                        print( "Warning (" + str( res_gpio ) + "): SW " + str( cnt ) + " " + g.WARNING_MESSAGE[res_gpio] )
                if res_gpio < 0:        # エラーを処理する。
                        print( "Error (" + str( abs( res_gpio ) ) + "): SW " + str( cnt ) + " " + g.ERROR_MESSAGE[abs( res_gpio )] )
                else:
                        print( "SW " + str( cnt ) + " is " + switch_status[res_gpio] + "." )

                """ # IOtest END

        cap = cv2.VideoCapture( 0 )     # ビデオを生成する。

        if ( cap.isOpened() ):  # ビデオがオープンできているか、
                cap.set(cv2.CAP_PROP_FPS, 30 )                                          # カメラFPSを設定
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width )         # カメラ画像の横幅を設定
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height )       # カメラ画像の縦幅を設定

#               print( "FPS", cap.get(cv2.CAP_PROP_FPS) )
#               print( "WIDTH", cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
#               print( "HEIGHT", cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )

                mode = "CONTINUOUS"     # 最初のモードは連続モード
                ikey = 0                        # 一応、終了条件を設定する。
                while ( ikey != ord( 'q' ) ):   # キーボードから「q」が入力されたら終了する。…事実上、対応できていない。と言うか 、必要ない。
                        while ( mode == "CONTINUOUS" ): # 連続モード
                                ret, source_img = cap.read()    # 1フレーム読み込む。

                                result = image_process.image_process( source_img )      # 処理する。

                                for cnt in range( out_bit_num ):
                                        mylib.write_gpio( P_OUT[cnt], result[cnt] )     # 処理結果より、GPIOを設定する。

                                if ( mylib.read_gpio( CONT_REQ ) == INACT ):    # CONT_REQがインアクティブになったら、
                                        mode = "SINGLE_SHOT"    # シングルショットモードに移行する。

                        while ( mode == "SINGLE_SHOT" ):        # 単発モード
                                ret, source_img = cap.read()    # 1フレーム読み込む。

                                result = image_process.image_process( source_img )      # 処理する。

                                for cnt in range( out_bit_num ):
                                        mylib.write_gpio( P_OUT[cnt], result[cnt] )     # 処理結果より、GPIOを設定する。

                                while ( mylib.read_gpio( CONT_REQ ) != ACT ):   # CONT_REQがアクティブになるまで待つ。
                                        pass

                                mode = "CONTINUOUS"

#                               ikey = cv2.waitKey( 1 ) & 0xff  # 64ビット版では「& 0xff」が要るらしい。

                # 終了処理
                cap.release()
                cv2.destroyAllWindows()

                for cnt in range( 4 ):
                        res_gpio = mylib.unuse_gpio( P_IN[cnt] )
                        if res_gpio > 1:        # 警告を処理する。警告は2以上、0, 1はGPIOの値
                                print( "Warning: GPIO " + str( P_IN[cnt] ) + " (" + str( res_gpio ) + ")" )
                        elif res_gpio < 0:      # エラーを処理する。
                                print( "Error:   GPIO " + str( P_IN[cnt] ) + " (" + str( res_gpio ) + ")" )
                        else:
                                print( "GPIO " + str( P_IN[cnt] ) + " close successful." )
                        res_gpio = mylib.unuse_gpio( P_OUT[cnt] )
                        if res_gpio > 1:        # 警告を処理する。警告は2以上、0, 1はGPIOの値
                                print( "Warning: GPIO " + str( P_OUT[cnt] ) + " (" + str( res_gpio ) + ")" )
                        elif res_gpio < 0:      # エラーを処理する。
                                print( "Error:   GPIO " + str( P_OUT[cnt] ) + " (" + str( res_gpio ) + ")" )
                        else:
                                print( "GPIO " + str( P_OUT[cnt] ) + " close successful." )


if __name__ == "__main__":
        main()
