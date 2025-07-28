import Adafruit_DHT
from time import sleep

class TemperatureSensor:
    def __init__(self, sensor_model='DHT22', gpio_pin=18):
        """
        :param sensor_model: 'DHT11' or 'DHT22'
        :param gpio_pin: 接続しているGPIOピン番号 (例: GPIO4なら 4)
        """
        sensor_map = {
            'DHT11': Adafruit_DHT.DHT11,
            'DHT22': Adafruit_DHT.DHT22
        }

        if sensor_model not in sensor_map:
            raise ValueError("対応センサー: 'DHT11' or 'DHT22' のみ")

        self.sensor = sensor_map[sensor_model]
        self.gpio_pin = gpio_pin

        self.pre_temp = 0
        self.pre_humid = 0

    def read(self):
        """
        温度と湿度を取得する

        :param retries: 再試行回数
        :param delay: 失敗時の再試行までの待ち時間（秒）
        :return: (湿度, 温度) または None（失敗時）
        """
      
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio_pin)

        if self.pre_humid != humidity or self.pre_temp != temperature:
            self.pre_humid = humidity
            self.pre_temp = temperature


if __name__ == "__main__":

    sensor = TemperatureSensor(sensor_model='DHT11')

    while True:
        sensor.read()
        print(f"温度: {sensor.pre_temp}℃, 湿度: {sensor.pre_humid}%")

        sleep(1.0)
