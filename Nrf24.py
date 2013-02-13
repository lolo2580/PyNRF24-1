import PyBCM2835

from Nrf24Registers import *

class Nrf24:

    COMMAND_READ_REGISTER = 0x00
    COMMAND_WRITE_REGISTER = 0x20
    COMMAND_READ_RX_PAYLOAD = 0x61
    COMMAND_WRITE_TX_PAYLOAD = 0xa0
    COMMAND_FLUSH_TX = 0xe1
    COMMAND_FLUSH_RX = 0xe2
    COMMAND_REUSE_TX_PAYLOAD = 0xe3
    COMMAND_READ_RX_PAYLOAD_WIDTH = 0x60
    COMMAND_WRITE_ACK_PAYLOAD = 0xa8
    COMMAND_WRITE_TX_PAYLOAD_NOACK = 0xb0
    COMMAND_NOP = 0xff

    MODE_IDLE = 0
    MODE_RX = 1
    MODE_TX = 2

    DATA_RATE_250Kbps = 11
    DATA_RATE_1Mbps = 12
    DATA_RATE_2Mbps = 13

    def __init__(self):
        if not (PyBCM2835.init()):
           raise EnvironmentError("Cannot initialize BCM2835.")

        PyBCM2835.gpio_fsel(PyBCM2835.RPI_V2_GPIO_P1_22, PyBCM2835.GPIO_FSEL_OUTP)

        PyBCM2835.spi_begin()
        PyBCM2835.spi_setBitOrder(PyBCM2835.SPI_BIT_ORDER_MSBFIRST)
        PyBCM2835.spi_setDataMode(PyBCM2835.SPI_MODE0)
        PyBCM2835.spi_setClockDivider(PyBCM2835.SPI_CLOCK_DIVIDER_32768)
        PyBCM2835.spi_chipSelect(PyBCM2835.SPI_CS0)
        PyBCM2835.spi_setChipSelectPolarity(PyBCM2835.SPI_CS0, PyBCM2835.LOW)

        PyBCM2835.delay(100)

        self.write_register(Nrf24Registers.REG_07_STATUS, Nrf24Registers.STATUS_RX_DR | Nrf24Registers.STATUS_TX_DS | Nrf24Registers.STATUS_MAX_RT )

        self.power_down()

        self.flush_rx()
        self.flush_tx()

        self.power_up_rx()

    def stop(self):
        PyBCM2835.spi_end()
        PyBCM2835.close()

    def read_bit(self, byte, bit_location):
        if bit_location > 7 or bit_location < 0:
            raise ValueError("Bit location >= 0 and <= 7")
        return (byte >> bit_location) & 1

    def command(self, bytes):
        result = ""
        for byte in bytes:
            result += chr(byte)
        return result

    def as_hex(self, bytes):
        result = ""
        for byte in bytes:
            result += "{0:#x} ".format(byte)
        return result

    def as_str(self, bytes):
        result = ""
        for byte in bytes:
            result += chr(byte)
        return result

    def as_bits(self, byte, prefix = " "):
        print prefix
        print "bits 0 1 2 3 4 5 6 7"
        bits = "vals "
        for i in xrange(8):
            bits += "{0:d} ".format((byte >> i) & 1)
        print bits

    def as_bytes(self, string):
        bytes = []
        for char in string:
            bytes.append(ord(char))
        return bytes

    def as_bytes_fixed_length(self, string, length):
        bytes = []
        for char in string:
            bytes.append(ord(char))

        if len(bytes) < length:
            for idx in range(length-len(bytes)):
                bytes.append(ord(" "))

        return bytes

    def write_register(self, register_address, value):
        register_address = (register_address & Nrf24Registers.REGISTER_MASK) | self.COMMAND_WRITE_REGISTER
        outbuffer = self.command([register_address, value])
        PyBCM2835.spi_transfern(outbuffer, len(outbuffer))

    def write_register_bytes(self, register_address, bytes):
        register_address = (register_address & Nrf24Registers.REGISTER_MASK) | self.COMMAND_WRITE_REGISTER
        self.burst_write(register_address, bytes)

    def read_register_bytes(self, register_address, length):
        register_address = (register_address & Nrf24Registers.REGISTER_MASK) | self.COMMAND_READ_REGISTER
        return self.burst_read(register_address, length)

    def read_register(self, register_address):
        register_address = (register_address & Nrf24Registers.REGISTER_MASK) | self.COMMAND_READ_REGISTER
        outbuffer = self.command([register_address, 0])
        PyBCM2835.spi_transfern(outbuffer, len(outbuffer))
        return ord(outbuffer[1])

    def spi_read(self, command):
        outbuffer = self.command([command, 0])
        PyBCM2835.spi_transfern(outbuffer, len(outbuffer))
        return ord(outbuffer[1])

    def burst_read(self, spi_command, response_len):
        cmd_seq = [spi_command]
        for x in range(response_len):
            cmd_seq.append(0)

        resp_buffer = ""
        for x in xrange(response_len+1):
            resp_buffer += chr(0)

        command_buf = self.command(cmd_seq)
        PyBCM2835.spi_transfernb(command_buf, resp_buffer, response_len + 1)

        response = []
        for char in resp_buffer:
            response.append(ord(char))

        response.pop(0)

        return response

    def burst_write(self, spi_command, data):
        cmd_seq = [spi_command]
        for byte in data:
            cmd_seq.append(byte)

        out_buffer = self.command(cmd_seq)
        PyBCM2835.spi_transfern(out_buffer, len(cmd_seq))
        return ord(out_buffer[0])

    def chip_enabled(self, value):
        PyBCM2835.gpio_write(PyBCM2835.RPI_V2_GPIO_P1_22, value)

    def power_down(self):
        self.write_register(Nrf24Registers.REG_00_CONFIG, Nrf24Registers.CONFIG_EN_CRC)
        self.chip_enabled(PyBCM2835.LOW)

    def power_up_rx(self):
        self.write_register(Nrf24Registers.REG_00_CONFIG, Nrf24Registers.CONFIG_EN_CRC | Nrf24Registers.CONFIG_PWR_UP | Nrf24Registers.CONFIG_PRIM_RX)
        self.chip_enabled(PyBCM2835.HIGH)

    def power_up_tx(self):
        self.write_register(Nrf24Registers.REG_00_CONFIG, Nrf24Registers.CONFIG_EN_CRC | Nrf24Registers.CONFIG_PWR_UP)
        self.chip_enabled(PyBCM2835.LOW)
        PyBCM2835.delay(1)
        self.chip_enabled(PyBCM2835.HIGH)

    def pulse_ce(self):
        self.chip_enabled(PyBCM2835.LOW)
        PyBCM2835.delay(1)
        self.chip_enabled(PyBCM2835.HIGH)

    def flush_tx(self):
        return PyBCM2835.spi_transfer(Nrf24.COMMAND_FLUSH_TX)

    def flush_rx(self):
        return PyBCM2835.spi_transfer(Nrf24.COMMAND_FLUSH_RX)

    def status(self):
        return self.read_register(Nrf24Registers.REG_07_STATUS)

    def set_channel(self, channel_no):
        if channel_no < 0 or channel_no > 127:
            raise ValueError("Channel number must be >= 0 and <= 127")

        self.write_register(Nrf24Registers.REG_05_RF_CH, channel_no & Nrf24Registers.FREQUENCY_RF_CH)

    def set_address(self, address):
        if len(address) > 5:
            raise ValueError("Address must be 5 bytes max")

        return self.write_register_bytes(Nrf24Registers.REG_0B_RX_ADDR_P1, self.as_bytes(address))

    def get_address(self):
        return self.read_register_bytes(Nrf24Registers.REG_0B_RX_ADDR_P1, 5)

    def set_transmit_address(self, address):
        if len(address) > 5:
            raise ValueError("Address must be 5 bytes max")

        self.write_register_bytes(Nrf24Registers.REG_0A_RX_ADDR_P0, self.as_bytes(address))
        self.write_register_bytes(Nrf24Registers.REG_10_TX_ADDR, self.as_bytes(address))

    def get_transmit_address(self):
        rx_p0 = self.read_register_bytes(Nrf24Registers.REG_0A_RX_ADDR_P0, 5)
        tx_addr = self.read_register_bytes(Nrf24Registers.REG_10_TX_ADDR, 5)
        return [rx_p0, tx_addr]

    def set_payload_size(self, size):
        if size < 1 or size > 32:
            raise ValueError("Payload size must be >= 1 and <= 32 bytes. Spec. page #60")

        self.write_register(Nrf24Registers.REG_11_RX_PW_P0, size)
        self.write_register(Nrf24Registers.REG_12_RX_PW_P1, size)

    def set_rf(self, data_rate, rf_power):
        value = 0

        if data_rate == self.DATA_RATE_250Kbps:
           value |= (Nrf24Registers.RF_SETUP_RF_DR_LOW | Nrf24Registers.RF_SETUP_RF_DR_HIGH)
        elif data_rate == self.DATA_RATE_2Mbps:
           value |= Nrf24Registers.RF_SETUP_RF_DR_HIGH

        value |= rf_power

        self.write_register(Nrf24Registers.REG_06_RF_SETUP, value)

    def send(self, data, noack = False):
        command = self.COMMAND_WRITE_TX_PAYLOAD_NOACK if noack else self.COMMAND_WRITE_TX_PAYLOAD
        self.burst_write(command, data)
        self.power_up_tx()

    def wait_packet_sent(self):
        status = self.status()
        while not (status & (Nrf24Registers.STATUS_TX_DS | Nrf24Registers.STATUS_MAX_RT)):
            status = self.status()

        self.write_register(Nrf24Registers.REG_07_STATUS, Nrf24Registers.STATUS_TX_DS | Nrf24Registers.STATUS_MAX_RT)
        if status & Nrf24Registers.STATUS_MAX_RT:
            self.flush_tx()

        return status & Nrf24Registers.STATUS_TX_DS

    def clear_maxrt(self):
        self.write_register(Nrf24Registers.REG_07_STATUS, Nrf24Registers.STATUS_TX_DS | Nrf24Registers.STATUS_MAX_RT)

    def is_sending(self):
        return not (self.status() & (Nrf24Registers.STATUS_TX_DS | Nrf24Registers.STATUS_MAX_RT))

    def wait_available(self):
        self.power_up_rx()
        available = self.available()
        while not available:
            available = self.available()
        self.chip_enabled(PyBCM2835.LOW)

    def available(self):
        if self.read_register(Nrf24Registers.REG_17_FIFO_STATUS) & Nrf24Registers.RX_EMPTY:
            return False

        if self.read_register(self.COMMAND_READ_RX_PAYLOAD_WIDTH) > 32:
            self.flush_rx()
            return False

        return True

    def wait_available_timeout(self, timeout):
        self.power_up_rx()
        PyBCM2835.delay(timeout)
        if self.available():
            return True
        return False

    def recv(self):
        self.write_register(Nrf24Registers.REG_07_STATUS, Nrf24Registers.STATUS_RX_DR)
        if not self.available():
            return None

        length = self.spi_read(self.COMMAND_READ_RX_PAYLOAD_WIDTH)

        print "Length is {0:d}".format(length)

        return self.burst_read(self.COMMAND_READ_RX_PAYLOAD, length)
