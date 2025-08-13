from gpiozero import PWMLED
import socket
from time import sleep, time


class Udp_server_led:
    def __init__(self,
                 led_pins=[21, 20, 16, 26, 19, 13, 6, 5],
                 status_led_pin=12,
                 udp_ip="0.0.0.0",
                 udp_port=5005,
                 timeout_seconds=1.0,
                 gamma=2.2):
        
        # LEDセットアップ
        self.led_list = [PWMLED(pin) for pin in led_pins]
        self.status_led = PWMLED(status_led_pin)

        # UDP設定
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        self.sock.settimeout(0.1)

        # その他パラメータ
        self.last_received_time = time()
        self.timeout_seconds = timeout_seconds
        self.gamma = gamma

        print(f"Listening for UDP packets on port {self.udp_port}...")

    def gamma_correct(self, val):
        return pow(val, self.gamma)

    def process_packet(self, packet):
        parts = packet.decode().strip().split(",")
        if len(parts) != len(self.led_list):
            print("Invalid packet length")
            return

        values = []
        for raw in parts:
            try:
                val = float(raw)
                val = max(0.0, min(1.0, val))
                val = self.gamma_correct(val)
                values.append(val)
            except ValueError:
                values.append(0.0)

        # LED出力
        for led, val in zip(self.led_list, values):
            led.value = val

    def run(self):
        try:
            while True:
                try:
                    data, _ = self.sock.recvfrom(1024)
                    self.process_packet(data)
                    self.last_received_time = time()

                except socket.timeout:
                    pass
                except Exception as e:
                    print(f"Invalid data received — {e}")

                # 通信状態でstatus_led制御
                if time() - self.last_received_time > self.timeout_seconds:
                    for led in self.led_list:
                        led.value = 0.0
                    self.status_led.value = 0.0
                else:
                    self.status_led.value = 0.2

                sleep(0.05)

        except KeyboardInterrupt:
            print("\n終了します")
            self.cleanup()

    def cleanup(self):
        for led in self.led_list:
            led.off()
        self.status_led.off()
        self.sock.close()


if __name__ == "__main__":
    server = Udp_server_led()
    server.run()
