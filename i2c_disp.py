import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont  # Pillowが必要

# I2C初期化
i2c = busio.I2C(board.SCL, board.SDA)

# OLEDディスプレイ初期化（128x64の場合）
WIDTH = 128
HEIGHT = 64
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# 画面クリア
oled.fill(0)
oled.show()

# Pillowで描画用イメージ作成
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

# フォント設定（省略可、デフォルトを使用）
font = ImageFont.load_default()

# 文字描画
draw.text((0, 0), "Hello OLED!", font=font, fill=255)
draw.text((0, 20), "I2C Test OK", font=font, fill=255)

# OLEDに表示
oled.image(image)
oled.show()

# サンプルループ（数字カウント）
counter = 0
try:
    while True:
        draw.rectangle((0, 40, WIDTH, 60), outline=0, fill=0)  # カウンタ領域クリア
        draw.text((0, 40), f"Count: {counter}", font=font, fill=255)
        oled.image(image)
        oled.show()
        counter += 1
        time.sleep(1)
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print("終了")
