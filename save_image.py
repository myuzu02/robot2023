# -*- coding: utf-8 -*-

import cv2
import datetime

# カメラを開く
cap = cv2.VideoCapture(0)

indexNo = 0
while True:
    # 画像をキャプチャする
    ret, frame = cap.read()

    # 画像を表示する
    cv2.imshow("Image", frame)

    now = datetime.datetime.now()
    image_time = now.strftime('%Y%m%d_%H%M%S')

    # `q`キーを押すとループを終了する
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('c'):
        cv2.imwrite(f"{image_time}.png", frame)
        #cv2.imwrite(f"image{indexNo:05d}.png", frame)
        #indexNo = indexNo + 1
# カメラを閉じる
cap.release()
# すべてのウィンドウを閉じる
cv2.destroyAllWindows()