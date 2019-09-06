import socket
import struct
import unittest
from model.ip_addr import IPAddr


def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]



class TestCase(unittest.TestCase):
    def test_parse_regular(self):
        ipaddr = '192.168.0.1'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr))

    def test_parse_withspace(self):
        # 192.<space>168.0.1
        # <space><space><space>192.168.0.1
        ipaddr = '192.168.0.1'
        ipaddr_withspace = '192. 168.0.1'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr_withspace))

        ipaddr_withspace = '   192.168.0.1'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr_withspace))

    def test_parse_with_zero(self):
        # 192.168.00000.001
        ipaddr = '192.168.0.1'
        ipaddr_with_zero = '192.168.00000.001'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr_with_zero))

    def test_parse_over255(self):
        # 192.168.256.1 -> 0 -> NotValidAddressException
        ipaddr = '192.168.256.1'
        self.assertEqual(0, IPAddr.ipaddr_aton(ipaddr))

    def test_parse_special_struct(self):
        # 192.168.1 -> 192.168.0.1
        ipaddr = '192.168.1'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr))

    def test_parse_bad_struct(self):
        # 192.168.1.2.3 -> 0 -> NotValidAddressException
        ipaddr = '192.16 8.0.1'
        self.assertEqual(0, IPAddr.ipaddr_aton(ipaddr))

        ipaddr = '192.16 8.0.1 '
        self.assertEqual(0, IPAddr.ipaddr_aton(ipaddr))

    def test_parse_bad_struct2(self):
        # 192.168.1.2.3 -> 0 -> NotValidAddressException
        ipaddr = '192.168.1.2.3'
        self.assertEqual(0, IPAddr.ipaddr_aton(ipaddr))

    def test_parse_hex(self):
        # 0xc0.0x1e.0xff.0x70 -> 192.30.255.112 (github.com)
        ipaddr = '0xc0.0x1e.0xff.0x70'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr))

    def test_parse_hex_with_space(self):
        ipaddr = '0xc0.0x1e.0xff.0x70'
        ipaddr_withspace = '0xc0.0x1e.0xff.0x70  '
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr_withspace))

        ipaddr = '0xc0.0x1e.0xff.0x70'
        ipaddr_withspace = '0xc0.  0x1e.0xff.0x70'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr_withspace))

    def test_parse_invalid_hex(self):
        ipaddr = '0xc0.0x1e.0xff.0xfff'
        self.assertEqual(0, IPAddr.ipaddr_aton(ipaddr))

    def test_many_spaces(self):
        # 192.168.1 -> 192.168.0.1
        ipaddr = '192.168.0.1'
        ipaddr_withspace = '  192. 168.0.1'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr_withspace))

        ipaddr_withspace = '  192. 168.0 .1'
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr_withspace))

        ipaddr_withspace = '  192. 168.0.1 '
        self.assertEqual(ip2int(ipaddr), IPAddr.ipaddr_aton(ipaddr_withspace))
