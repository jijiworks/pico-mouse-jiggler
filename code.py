import time
import usb_hid
import board
import digitalio
from adafruit_hid.mouse import Mouse

JIGGLE_DISTANCE = 1   # ジグル距離（px）
JIGGLE_INTERVAL = 170 # ジグル間隔（秒）
MOUSE_HOLD_TIME = 0.2 # マウスが片方向に止まってる時間（秒）

# USB HID経由でマウス操作を行うためのインスタンスを作成
mouse = Mouse(usb_hid.devices)

# Pico本体のLED（GPIO25）
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False  # 最初はLED OFF

# 最後にマウスジグルを実行した時間
# 起動直後に１回動かすため「- JIGGLE_INTERVAL」を追加
last_jiggle_time = time.monotonic() - JIGGLE_INTERVAL

while True:
    now = time.monotonic()
    # ジグル間隔が経過したらマウス位置を動かす
    if now - last_jiggle_time >= JIGGLE_INTERVAL:
        led.value = True # LED ON
        
        # マウスジグル（右→左）
        mouse.move(x=JIGGLE_DISTANCE)
        time.sleep(MOUSE_HOLD_TIME) 
        mouse.move(x=-JIGGLE_DISTANCE)

        led.value = False # LED　OFF
        # 次回ジグル用のタイマー更新
        last_jiggle_time = time.monotonic()

    time.sleep(0.01)
