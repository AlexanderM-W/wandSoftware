import smbus
import time

class MAX17048:
    def __init__(self):
        self.MAX17048_ADDRESS = 0x36
        self.VCELL_REGISTER = 0x02
        self.SOC_REGISTER = 0x04
        self.MODE_REGISTER = 0x06
        self.VERSION_REGISTER = 0x08
        self.CONFIG_REGISTER = 0x0C
        self.COMMAND_REGISTER = 0xFE
        self.REGISTER_CRATE = 0x16
        self.bus = smbus.SMBus(1)


    #def readRegister(self, register):
    #    swappedWord = self.bus.read_word_data(self.MAX17048_ADDRESS, register )
    #    word = (swappedWord & 0xff) << 8 | (swappedWord >> 8)
    #    return word

    def readRegister(self, reg):
        buf = self.bus.read_i2c_block_data(self.MAX17048_ADDRESS, reg, 2)
        return ((buf[0] << 8) | buf[1])

    def makeWordSigned( self, word ):
        if ((word & 0x8000) != 0):
            return word - 0x10000
        else:
            return word


    def getVCell(self):
        VCell = self.readRegister(self.VCELL_REGISTER)
        return VCell* 0.000078125

    #state of charge (should be self calibrating)
    def getSoC(self):
        SoC = self.readRegister(self.SOC_REGISTER)
        return ((SoC >> 8) + 0.003906 * (SoC & 0x00ff))
        #return SoC/256.0

    def getVersion(self):
        version = self.readRegister(self.VERSION_REGISTER)
        return version

    def getCompensateValue(self):
        compVal = self.readRegister(self.VERSION_REGISTER)
        return compVal

    def getAlertThreshold(self):
        alertThreshold = self.bus.read_block_data(self.MAX17048_ADDRESS, self.VERSION_REGISTER)
        return 32 - (alertThreshold[1] & 0x1F)

    def getChargingRate(self):
        register = self.readRegister(self.REGISTER_CRATE)
        crate = self.makeWordSigned( register )
        return crate * 0.00208


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


if __name__ == "__main__":
    i = 0
    while(i<10):
        time.sleep(1)
        bat = MAX17048()
        print(str(bat.getSoC()) + " " + str(bat.getVCell()))
        i = i+1
