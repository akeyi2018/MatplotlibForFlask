import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

# I2Cバス初期化
i2c = busio.I2C(SCL, SDA)

# PCA9685初期化
pca = PCA9685(i2c, address=0x40)  # アドレス0x40を指定
pca.frequency = 1000  # 周波数 1kHz（LED向け）

led_channel = pca.channels[8]  # CH0に接続したLED

print("LEDフェードテスト開始（Ctrl+Cで停止）")

try:
    while True:
        # 明るくする
        for duty in range(0, 0x1000, 50):  # 0x1000 = 4096段階
            led_channel.duty_cycle = duty
            time.sleep(0.01)
        # 暗くする
        for duty in range(0x1000, 0, -50):
            led_channel.duty_cycle = duty
            time.sleep(0.01)
except KeyboardInterrupt:
    led_channel.duty_cycle = 0
    print("\n終了")
