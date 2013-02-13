__author__ = 'Yakimov'

from time import sleep
from Nrf24 import *

nrf = Nrf24()

nrf.set_channel(110)
nrf.set_address("\xb3\xb4\xb5\xb6\x04")
nrf.set_payload_size(32)
nrf.set_rf(Nrf24.DATA_RATE_2Mbps, Nrf24Registers.RF_SETUP_PWR_m18dBm)
nrf.set_transmit_address("\xb3\xb4\xb5\xb6\x05")

print "My address: "
print nrf.as_hex(nrf.get_address())

nrf.send(nrf.as_bytes_fixed_length("Hello x05! \xA5 \xA3 \x1FC", 32))

if not nrf.wait_packet_sent():
    print "Packets not sent!"
else:
    print "Packets sent"

if nrf.wait_available_timeout(100):
    data = nrf.recv()
    print nrf.as_str(data)
else:
    print "No data from server"

nrf.stop()