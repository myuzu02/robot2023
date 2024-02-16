#!/usr/bin/python3
# -*- coding: utf-8 -*-

global GPIO_SUCCESS					# GPIOの操作に成功した。
global GPIO_ERROR_OPEN_FAIL			# GPIOのオープンに失敗した。
global GPIO_ERROR_DIREC_FAIL		# GPIOの入出力設定に失敗した。
global GPIO_ERROR_DIREC_UNMATCH		# GPIOが存在していて、入出力方向が一致していなかった。
global GPIO_ERROR_CHANGE_IN_2_OUT	# 入力ポートを出力しようとした。
global GPIO_ERROR_CHANGE_OUT_2_IN	# 出力ポートを入力しようとした。
global GPIO_ERROR_UNTIL_OPEN		# GPIOが開かれていない。
global GPIO_ERROR_OTHERS			# その他のエラー
global GPIO_ERROR_NOT_OPEN			# GPIOが開かれていない。
global GPIO_WARNING_DIREC_MATCH		# GPIOが存在していて、入出力方向が一致していた。
global GPIO_WARNING_INVALID_DATA	# 無効なデータである。

global ERROR_MESSAGE
global WARNING_MESSAGE

#global ACT
#global INACT
"""
def global_variable_init():
	g.GPIO_SUCCESS = 0						# GPIOの操作に成功した。
	g.GPIO_ERROR_OPEN_FAIL = -1				# GPIOのオープンに失敗した。
	g.GPIO_ERROR_DIREC_FAIL = -2			# GPIOの入出力設定に失敗した。
	g.GPIO_ERROR_DIREC_UNMATCH = -3			# GPIOが存在していて、入出力方向が一致していなかった。
	g.GPIO_ERROR_CHANGE_IN_2_OUT = -4		# 入力を出力に変更しようとした。
	g.GPIO_ERROR_CHANGE_OUT_2_IN = -5		# 出力を入力に変更しようとした。
	g.GPIO_ERROR_NOT_OPEN = -6				# GPIOが開かれていない。
	g.GPIO_ERROR_WRITE_TO_INPUT_PORT = -7	# 入力ポートに出力しようとした。
	g.GPIO_ERROR_OTHERS = -8				# その他のエラー
   											# 値0と1は、GPIOの読み出し値と一致するので警告番号に使用しない。
	g.GPIO_WARNING_DIREC_MATCH = 2			# GPIOが存在していて、入出力方向が一致していた。
	g.GPIO_WARNING_UNTIL_OPEN = 3			# 開かれていないGPIOに操作しようとした。

	g.ERROR_MESSAGE = ["成功"]
	g.ERROR_MESSAGE.append( "GPIOのオープンに失敗した。" )
	g.ERROR_MESSAGE.append( "GPIOの入出力設定に失敗した。" )
	g.ERROR_MESSAGE.append( "GPIOが存在していて、入出力方向が一致していなかった。" )
	g.ERROR_MESSAGE.append( "入力を出力に変更しようとした。" )
	g.ERROR_MESSAGE.append( "出力を入力に変更しようとした。" )
	g.ERROR_MESSAGE.append( "GPIOが開かれていない。" )
	g.ERROR_MESSAGE.append( "入力ポートに出力しようとした。" )
	g.ERROR_MESSAGE.append( "その他のエラー" )
	g.WARNING_MESSAGE = ["成功",""]
	g.WARNING_MESSAGE.append( "GPIOが存在していて、入出力方向が一致していた。" )
	g.WARNING_MESSAGE.append( "開かれていないGPIOに操作しようとした。" )
"""