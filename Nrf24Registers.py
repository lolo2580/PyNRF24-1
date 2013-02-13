__author__ = 'Yakimov'

class Nrf24Registers:

    REGISTER_MASK = 0x1f
    REG_00_CONFIG = 0x00
    REG_01_EN_AA = 0x01
    REG_02_EN_RXADDR = 0x02
    REG_03_SETUP_AW = 0x03
    REG_04_SETUP_RETR = 0x04
    REG_05_RF_CH = 0x05
    REG_06_RF_SETUP = 0x06
    REG_07_STATUS = 0x07
    REG_08_OBSERVE_TX = 0x08
    REG_09_RPD = 0x09
    REG_0A_RX_ADDR_P0 = 0x0a
    REG_0B_RX_ADDR_P1 = 0x0b
    REG_0C_RX_ADDR_P2 = 0x0c
    REG_0D_RX_ADDR_P3 = 0x0d
    REG_0E_RX_ADDR_P4 = 0x0e
    REG_0F_RX_ADDR_P5 = 0x0f
    REG_10_TX_ADDR = 0x10
    REG_11_RX_PW_P0 = 0x11
    REG_12_RX_PW_P1 = 0x12
    REG_13_RX_PW_P2 = 0x13
    REG_14_RX_PW_P3 = 0x14
    REG_15_RX_PW_P4 = 0x15
    REG_16_RX_PW_P5 = 0x16
    REG_17_FIFO_STATUS = 0x17
    REG_1C_DYNPD = 0x1c
    REG_1D_FEATURE = 0x1d

    CONFIG_MASK_RX_DR = 0x40
    CONFIG_MASK_TX_DS = 0x20
    CONFIG_MASK_MAX_RT = 0x10
    CONFIG_EN_CRC = 0x08
    CONFIG_CRCO = 0x04
    CONFIG_PWR_UP = 0x02
    CONFIG_PRIM_RX = 0x01

    # #define NRF24_REG_01_EN_AA                              0x01
    AUTOACK_ENAA_P5 = 0x20
    AUTOACK_ENAA_P4 = 0x10
    AUTOACK_ENAA_P3 = 0x08
    AUTOACK_ENAA_P2 = 0x04
    AUTOACK_ENAA_P1 = 0x02
    AUTOACK_ENAA_P0 = 0x01

    # #define NRF24_REG_02_EN_RXADDR                          0x02
    RXADDR_ERX_P5 = 0x20
    RXADDR_ERX_P4 = 0x10
    RXADDR_ERX_P3 = 0x08
    RXADDR_ERX_P2 = 0x04
    RXADDR_ERX_P1 = 0x02
    RXADDR_ERX_P0 = 0x01

    # #define NRF24_REG_03_SETUP_AW                           0x03
    ADDRWIDTH_AW_3_BYTES = 0x01
    ADDRWIDTH_AW_4_BYTES = 0x02
    ADDRWIDTH_AW_5_BYTES = 0x03

    # #define NRF24_REG_04_SETUP_RETR                         0x04
    AUTORTR_ARD = 0xf0
    AUTORTR_ARC = 0x0f

    # #define NRF24_REG_05_RF_CH                              0x05
    FREQUENCY_RF_CH = 0x7f

    # #define NRF24_REG_06_RF_SETUP                           0x06
    RF_SETUP_CONT_WAVE = 0x80
    RF_SETUP_RF_DR_LOW = 0x20
    RF_SETUP_PLL_LOCK = 0x10
    RF_SETUP_RF_DR_HIGH = 0x08
    RF_SETUP_PWR = 0x06

    RF_SETUP_PWR_m18dBm = 0x00
    RF_SETUP_PWR_m12dBm = 0x02
    RF_SETUP_PWR_m6dBm = 0x04
    RF_SETUP_PWR_0dBm = 0x06

    # #define NRF24_REG_07_STATUS                             0x07
    STATUS_RX_DR = 0x40
    STATUS_TX_DS = 0x20
    STATUS_MAX_RT = 0x10
    STATUS_RX_P_NO = 0x0e
    STATUS_TX_FULL = 0x01

    # #define NRF24_REG_08_OBSERVE_TX                         0x08
    OBSERVE_PLOS_CNT = 0xf0
    OBSERVE_ARC_CNT = 0x0f

    # #define NRF24_REG_09_RPD                                0x09
    RPD = 0x01

    # #define NRF24_REG_17_FIFO_STATUS                        0x17
    TX_REUSE = 0x40
    TX_FULL = 0x20
    TX_EMPTY = 0x10
    RX_FULL = 0x02
    RX_EMPTY = 0x01

    # #define NRF24_REG_1C_DYNPD                              0x1c
    DPL_P5 = 0x20
    DPL_P4 = 0x10
    DPL_P3 = 0x08
    DPL_P2 = 0x04
    DPL_P1 = 0x02
    DPL_P0 = 0x01

    # #define NRF24_REG_1D_FEATURE                            0x1d
    EN_DPL = 0x04
    EN_ACK_PAY = 0x02
    EN_DYN_ACK = 0x01

    def describe_register(self, address):
        return ""