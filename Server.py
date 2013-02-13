__author__ = 'Yakimov'

from time import sleep
from Nrf24 import *

nrf = Nrf24()

nrf.set_channel(110)
nrf.set_address("\xb3\xb4\xb5\xb6\x05")
nrf.set_payload_size(32)
nrf.set_rf(Nrf24.DATA_RATE_2Mbps, Nrf24Registers.RF_SETUP_PWR_m18dBm)
nrf.set_transmit_address("\xb3\xb4\xb5\xb6\x04")

print "My address: "
print nrf.as_hex(nrf.get_address())

var = 1
while var == 1:
    print "Waiting for packetz"
    nrf.wait_available()

    data = nrf.recv()
    print nrf.as_str(data)

    nrf.send(nrf.as_bytes_fixed_length("Hello there x04", 32))

    nrf.wait_packet_sent()

nrf.stop()