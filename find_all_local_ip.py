# import socket
# from socket import AddressFamily


# def get_ips():
#     ipv4 = list()
#     ipv6 = list()
#     for item in socket.getaddrinfo(socket.gethostname(), None):
#         protocol, *_, (ip, *_) = item
#         if protocol == AddressFamily.AF_INET:
#             ipv4.append(ip)
#         elif protocol == AddressFamily.AF_INET6:
#             ipv6.append(ip)

#     return ipv4, ipv6

# from socket import getaddrinfo, AF_INET, gethostname
# def ip4_addresses_list():
#     ip_list = []
#     for ip in getaddrinfo(host=gethostname(), port=None, family=AF_INET):   
#         ip_list.append(ip[4][0])
#     return ip_list

# # import ipaddress
# # network = ipaddress.ip_network('192.168.0.0/24')
# # for ip in network:
# #     # Ignore e.g. 192.168.1.0 and 192.168.1.255
# #     if ip == network.broadcast_address or ip == network.network_address:
# #         continue
# #     print(ip)

# # import socket

# def get_local_ip():
#     try:
#         # ホスト名を取得
#         hostname = socket.gethostname()
#         # ホスト名からローカルIPアドレスを解決
#         local_ip = socket.gethostbyname(hostname)
#         return local_ip
#     except socket.error as e:
#         print(f"エラーが発生しました: {e}")
#         return None

# # ローカルIPアドレスを取得して表示
# local_ip = get_local_ip()
# if local_ip:
#     print(f"ローカルIPアドレス: {local_ip}")
# else:
#     print("ローカルIPアドレスを取得できませんでした。")

# print(ip4_addresses_list())


# if __name__ == '__main__':
#     all_ipv4, all_ipv6 = get_ips()
#     print(all_ipv4)
#     print(all_ipv6)
#     print(ip4_addresses_list())


import subprocess

def get_devices_with_ip():
    arp_output_bytes = subprocess.check_output(["arp", "-a"])
    arp_output = arp_output_bytes.decode("cp932")  # もしくはエンコーディングに合わせた適切な文字コードを指定
    devices = []

    for line in arp_output.split("\n"):
        if len(line.strip()) == 0:
            continue
        parts = line.split()
        ip_address = parts[0]
        mac_address = parts[1]
        devices.append((ip_address, mac_address))
    
    return devices

# デバイスのIPアドレスとMACアドレスを取得して表示
devices = get_devices_with_ip()
if devices:
    print("デバイスのリスト:")
    for ip_address, mac_address in devices:
        print(f"IPアドレス: {ip_address}, MACアドレス: {mac_address}")
else:
    print("デバイスの情報を取得できませんでした。")

