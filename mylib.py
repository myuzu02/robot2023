# -*- coding: utf-8 -*-

import subprocess
import os
import variable as g

def global_variable_init():
	g.GPIO_SUCCESS = 0						# GPIOの操作に成功した。
	g.GPIO_ERROR_OPEN_FAIL = -1				# GPIOのオープンに失敗した。
	g.GPIO_ERROR_DIREC_FAIL = -2			# GPIOの入出力設定に失敗した。
	g.GPIO_ERROR_DIREC_UNMATCH = -3			# GPIOが存在していて、入出力方向が一致していなかった。
	g.GPIO_ERROR_CHANGE_IN_2_OUT = -4		# 入力ポートを出力ポートに変更しようとした。
	g.GPIO_ERROR_CHANGE_OUT_2_IN = -5		# 出力ポートを入力ポートに変更しようとした。
	g.GPIO_ERROR_GPIO_NOT_OPEN = -6			# GPIOが開かれていない。
	g.GPIO_ERROR_WRITE_TO_INPUT_PORT = -7	# 入力ポートに出力しようとした。
	g.GPIO_ERROR_OTHERS = -8				# その他のエラーが発生した。
				   							# 値0と1は、GPIOの読み出し値と一致するので警告番号に使用しない。
	g.GPIO_WARNING_DIREC_MATCH = 2			# GPIOが存在していたが、入出力方向が一致していたので何もしなかった。
	g.GPIO_WARNING_UNTIL_OPEN = 3			# 開かれていないGPIOに操作しようとした。
	g.GPIO_WARNING_INVALID_DATA = 4			# 無効なデータである。

	g.ERROR_MESSAGE = ["Success"]
	g.ERROR_MESSAGE.append( "Failed to open GPIO." )
	g.ERROR_MESSAGE.append( "GPIO input / output direction setting failed." )
	g.ERROR_MESSAGE.append( "GPIO was present and the input / output direction was not consistent." )
	g.ERROR_MESSAGE.append( "An attempt was made to change input port to output port." )
	g.ERROR_MESSAGE.append( "An attempt was made to change output port to input port." )
	g.ERROR_MESSAGE.append( "GPIO not open." )
	g.ERROR_MESSAGE.append( "An attempt was made to output to input port." )
	g.ERROR_MESSAGE.append( "Other error has occurred." )
	g.WARNING_MESSAGE = ["Success","Success"]
	g.WARNING_MESSAGE.append( "GPIO was present, but input / output direction matched, so done nothing." )
	g.WARNING_MESSAGE.append( "Attempted to operate on a GPIO that is not open." )
	g.WARNING_MESSAGE.append( "Invalid data." )


def use_gpio( gpio_num, direc ):	# 番号と入出力方向を指定してGPIOを生成する。
	if os.path.exists( "/sys/class/gpio/gpio" + str( gpio_num ) ):	# GPIOが存在するか、
		if subprocess.run( "cat /sys/class/gpio/gpio" + str( gpio_num ) + "/direction", shell=True, capture_output=True, text=True ).stdout.rstrip() == direc:	# GPIOの入出力方向と設定値が合っているか、
			result = g.GPIO_WARNING_DIREC_MATCH	# GPIOが存在していて、入出力方向が一致していた。
		else:
			result = g.GPIO_ERROR_DIREC_UNMATCH	# GPIOが存在していて、入出力方向が一致していなかった。
	else:
		subprocess.run( "echo " + str( gpio_num ) + " > /sys/class/gpio/export", shell=True )
		if os.path.exists( "/sys/class/gpio/gpio" + str( gpio_num ) ):	# GPIOが存在するか、
#			subprocess.run( "ls /sys/class/gpio/gpio" + str( gpio_num ) + "/direction > /dev/null", shell=True )	# ダミーで実行　これをやらないとタイミング的に書き込みできないっぽい。原因不明。
			subprocess.run( "sudo /bin/sh -c 'echo " + direc + " > /sys/class/gpio/gpio" + str( gpio_num ) + "/direction'", shell=True )	# sudoで実行した方が安全。
			if subprocess.run( "cat /sys/class/gpio/gpio" + str( gpio_num ) + "/direction", shell=True, capture_output=True, text=True ).stdout.rstrip() == direc:	# GPIOの入出力方向と設定値が合っているか、
				result = g.GPIO_SUCCESS	# GPIOのオープンとGPIOの入出力設定に成功した。
			else:
				result = g.GPIO_ERROR_DIREC_FAIL	# GPIOのオープンに成功したけどGPIOの入出力設定に失敗した。

		else:
			result = g.GPIO_ERROR_OPEN_FAIL	# GPIOのオープンに失敗した。

	return result

def read_gpio( gpio_num ):	# GPIOオブジェクトが存在したら読み出したGPIOの値、存在しなかったらエラーコードを返す。
	if os.path.exists( "/sys/class/gpio/gpio" + str( gpio_num ) ):	# GPIOが存在するか、
		result = int( subprocess.run( "cat /sys/class/gpio/gpio" + str( gpio_num ) + "/value", shell=True, capture_output=True, text=True ).stdout.rstrip() )
	else:
		result = g.GPIO_ERROR_GPIO_NOT_OPEN	# GPIOが開かれていない。

	return result


def write_gpio( gpio_num, value ):	# GPIOオブジェクトが存在し、値が有効であったら、GPIOに書き込む。書き込み条件に合わなかったらエラーコードを返す。
	if os.path.exists( "/sys/class/gpio/gpio" + str( gpio_num ) ):	# GPIOが存在するか、
		if subprocess.run( "cat /sys/class/gpio/gpio" + str( gpio_num ) + "/direction", shell=True, capture_output=True, text=True ).stdout.rstrip() == "out":	# GPIOは出力モードか、
			if value == 0 or value == 1:	# 値は0か1であるか、
				subprocess.run( "echo " + str( value ) + " > /sys/class/gpio/gpio" + str( gpio_num ) + "/value", shell=True )
				result = g.GPIO_SUCCESS	# 出力に設定されたGPIOに値を書き込んだ。
			else:
				result = g.GPIO_WARNING_INVALID_DATA	# 無効な値が指定された。
		elif subprocess.run( "cat /sys/class/gpio/gpio" + str( gpio_num ) + "/direction", shell=True, capture_output=True, text=True ).stdout.rstrip() == "in":	# GPIOが入力モードであったら、
			result = g.GPIO_ERROR_WRITE_TO_INPUT_PORT	# 入力ポートに出力しようとした。
		else:
			result = g.GPIO_ERROR_OTHERS	# その他のエラー
	else:
		result = g.GPIO_ERROR_GPIO_NOT_OPEN	# GPIOが開かれていない。

	return result


def unuse_gpio( gpio_num ):
	if os.path.exists( "/sys/class/gpio/gpio" + str( gpio_num ) ):	# GPIOが存在するか、
		subprocess.run( "echo " + str( gpio_num ) + " > /sys/class/gpio/unexport", shell=True )
		if os.path.exists( "/sys/class/gpio/gpio" + str( gpio_num ) ):	# GPIOが存在するか、
			result = g.GPIO_WARNING_UNTIL_OPEN	# GPIOのクローズに失敗した。
		else:
			result = g.GPIO_SUCCESS	# GPIOのクローズに成功した。
	else:
		result = g.GPIO_WARNING_UNTIL_OPEN	# GPIOが無くてクローズできない。

	return result