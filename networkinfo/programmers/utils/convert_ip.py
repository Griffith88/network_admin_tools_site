import socket
import struct


class IpAddress:
    """
    Class for converting ip from binary to normal view
    :return normal ip
    """

    def __init__(self, input: str):
        self.address_long = int(input, 10)

    def convert(self):
        hex(self.address_long)
        ip_address_raw = socket.inet_ntoa(struct.pack("<L", self.address_long))
        return self.reverse_ip(ip_address_raw)

    def reverse_ip(self, raw_ip):
        ip_list = raw_ip.split('.')[::-1]
        ip_reversed = '.'.join(octet for octet in ip_list)
        return ip_reversed
