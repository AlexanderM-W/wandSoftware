from smbus2 import SMBus, i2c_msg
from time import sleep
from math import ceil
    

# Declare I2C Address
_CAP1203Address = 0x28

# Registers as defined in Table 5-1 from datasheet (pg 20-21)
_MAIN_CONTROL = b'\x00'
_GENERAL_STATUS = b'\x02'
_SENSOR_INPUT_STATUS = b'\x03'
_SENSOR_INPUT_1_DELTA_COUNT = b'\x10'
_SENSOR_INPUT_2_DELTA_COUNT = b'\x11'
_SENSOR_INPUT_3_DELTA_COUNT = b'\x12'
_SENSITIVITY_CONTROL = b'\x1F'
_CONFIG = b'\x20'
_INTERRUPT_ENABLE = b'\x27'
_REPEAT_RATE_ENABLE = b'\x28'
_MULTIPLE_TOUCH_CONFIG = b'\x2A'
_MULTIPLE_TOUCH_PATTERN_CONFIG = b'\x2B'
_MULTIPLE_TOUCH_PATTERN = b'\x2D'
_PRODUCT_ID = b'\xFD'

# Product ID - always the same (pg. 22)
_PROD_ID_VALUE = b'\x6D'

def sleep_ms(t):
    sleep(t/1000)

############################
### Generic I2C functons ###
############################

class I2CLinux:
    def __init__(self, bus=None):
        if bus is None:
            bus = 1
        self.i2c = SMBus(bus)

    def readfrom_mem(self, addr, memaddr, nbytes, *, addrsize=8):
        data = [None] * nbytes # initialise empty list
        self.smbus_i2c_read(addr, memaddr, data, nbytes, addrsize=addrsize)
        return data
    
    def writeto_mem(self, addr, memaddr, buf, *, addrsize=8):
        self.smbus_i2c_write(addr, memaddr, buf, len(buf), addrsize=addrsize)
    
    def smbus_i2c_write(self, address, reg, data_p, length, addrsize=8):
        ret_val = 0
        data = []
        for index in range(length):
            data.append(data_p[index])
        if addrsize == 8:
            msg_w = i2c_msg.write(address, [reg] + data)
        elif addrsize == 16:
            msg_w = i2c_msg.write(address, [reg >> 8, reg & 0xff] + data)
        else:
            raise Exception("address must be 8 or 16 bits long only")
        self.i2c.i2c_rdwr(msg_w)
        return ret_val
        
    def smbus_i2c_read(self, address, reg, data_p, length, addrsize=8):
        ret_val = 0
        if addrsize == 8:
            msg_w = i2c_msg.write(address, [reg]) # warning this is set up for 16-bit addresses
        elif addrsize == 16:
            msg_w = i2c_msg.write(address, [reg >> 8, reg & 0xff]) # warning this is set up for 16-bit addresses
        else:
            raise Exception("address must be 8 or 16 bits long only")
        msg_r = i2c_msg.read(address, length)
        self.i2c.i2c_rdwr(msg_w, msg_r)
        if ret_val == 0:
            for index in range(length):
                data_p[index] = ord(msg_r.buf[index])
        return ret_val
    
    def write8(self, addr, reg, data):
        if reg is None:
            d = int.from_bytes(data, 'big')
            self.i2c.write_byte(addr, d)
        else:
            r = int.from_bytes(reg, 'big')
            d = int.from_bytes(data, 'big')
            self.i2c.write_byte_data(addr, r, d)
    
    def read16(self, addr, reg):
        regInt = int.from_bytes(reg, 'big')
        return self.i2c.read_word_data(addr, regInt).to_bytes(2, byteorder='little', signed=False)

#################################
#################################
#################################


##################################
### CAP1203 specific functions ###
##################################

class CAP1203(object):
    
    def __init__(self, bus=None, freq=None, sda=None, scl=None, addr=_CAP1203Address, touchmode = "multi", sensitivity = 3):
        self.i2c =  I2CLinux(bus=bus)
        self.addr = addr
        
        for i in range(0,1):
            try:
                if (touchmode == "single"):
                    self.setBits(_MULTIPLE_TOUCH_CONFIG,b'\x80',b'\x80')
                if (touchmode == "multi"):
                    self.setBits(_MULTIPLE_TOUCH_CONFIG,b'\x00',b'\x80')
                if (sensitivity >= 0 and sensitivity <= 7): # check for valid entry
                    self.setBits(_SENSITIVITY_CONTROL,bytes([sensitivity*16]),b'\x70')
            except:
                print("connection failed")
                sleep_ms(1000)
    
    def setBits(self, address, byte, mask):
        old_byte = int.from_bytes(self.i2c.readfrom_mem(self.addr, int.from_bytes(address,"big"), 1),"big")
        temp_byte = old_byte
        int_byte = int.from_bytes(byte,"big")
        int_mask = int.from_bytes(mask,"big")
        for n in range(8): # Cycle through each bit
            bit_mask = (int_mask >> n) & 1
            if bit_mask == 1:
                if ((int_byte >> n) & 1) == 1:
                    temp_byte = temp_byte | 1 << n
                else:
                    temp_byte = temp_byte & ~(1 << n)
        new_byte = temp_byte
        self.i2c.writeto_mem(self.addr, int.from_bytes(address,"big"), bytes([new_byte]))
    
    def sensorEnable(self, sensor):
        self.setBits(b'\x21',bytes([sensor]),b'\x07')

    def clearInt(self):
        self.setBits(b'\x00',bytes([0]),b'\x01')

    def setRepeatRate(self, sensor):
        self.setBits(b'\x28',bytes([sensor]),b'\x03')

    def setNoiseThresh(self, threshold):
        self.setBits(b'\x38',bytes([threshold]),b'\x03')

    def setAvgSample(self, samples):
        self.setBits(b'\x24',bytes([samples*16]),b'\x70')

    def powerButtonConf(self, time):
        self.setBits(b'\x61',bytes([time]),b'\x07')
        
    def setPowerButton(self, button):
        self.setBits(b'\x60',bytes([button]),b'\x07')

    def getSensitivity(self):
        sensitivity_control = self.i2c.readfrom_mem(self.addr, int.from_bytes(_SENSITIVITY_CONTROL,"big"), 1)

    def getInt(self):
        general_status_value = self.i2c.readfrom_mem(self.addr, int.from_bytes(_MAIN_CONTROL,"big"), 1)
        return general_status_value

    def setSensitivity(self):
        self.i2c.writeto_mem(self.addr, int.from_bytes(_SENSITIVITY_CONTROL,"big"), 0x6F)
        
    def clearInterrupt(self):
        self.i2c.writeto_mem(self.addr, int.from_bytes(_MAIN_CONTROL,"big"), bytes([0x00]))
        main_control_value = self.i2c.readfrom_mem(self.addr, int.from_bytes(_MAIN_CONTROL,"big"), 1)
    
    def read(self):
        """
        Get the status of each touch pad and return a dict. Dict keys match hardware pad labels
        """
        CS1return = 0
        CS2return = 0
        CS3return = 0
        try:
            self.clearInterrupt()
            general_status_value = self.i2c.readfrom_mem(self.addr, int.from_bytes(_GENERAL_STATUS,"big"), 1)
        except:
            print(i2c_err_str.format(self.addr))
            return dict([(1,float('NaN')),(2,float('NaN')),(3,float('NaN'))])     
        mask =  0b00000001
        value = mask & int.from_bytes(general_status_value,'big')
        sensor_input_status = self.i2c.readfrom_mem(self.addr, int.from_bytes(_SENSOR_INPUT_STATUS,"big"), 1)
        sts = int.from_bytes(sensor_input_status,'big')
        CS1 = 0b00000001 & sts
        CS2 = 0b00000010 & sts
        CS3 = 0b00000100 & sts
        if (CS1 > 0):
            CS1return = 1
        if (CS2 > 0):
            CS2return = 1
        if (CS3 > 0):
            CS3return = 1
        return dict([(1,CS1return),(2,CS2return),(3,CS3return)]) # dict key matches hardware label
    
    def readDeltaCounts(self):
        """
        Get the raw sensor reading
        """
        DC1return = 0; DC2return = 0; DC3return = 0
        try:
            DC1 = self.i2c.readfrom_mem(self.addr, int.from_bytes(_SENSOR_INPUT_1_DELTA_COUNT,"big"), 1)
            DC2 = self.i2c.readfrom_mem(self.addr, int.from_bytes(_SENSOR_INPUT_2_DELTA_COUNT,"big"), 1)
            DC3 = self.i2c.readfrom_mem(self.addr, int.from_bytes(_SENSOR_INPUT_3_DELTA_COUNT,"big"), 1)
        except:
            print(i2c_err_str.format(self.addr))
            return dict([(1,float('NaN')),(2,float('NaN')),(3,float('NaN'))])
        return dict([(1,DC1),(2,DC2),(3,DC3)]) # dict key matches hardware label
        

#################################
#################################
#################################

if __name__ == "__main__":
    frontSensor = CAP1203(bus=5,sensitivity=1,touchmode='single')
    backSensor = CAP1203(bus=1,sensitivity=1,touchmode='single')

    sleep(1)
    frontSensor.setNoiseThresh(0)
    frontSensor.setAvgSample(1)
    frontSensor.sensorEnable(1)
    frontSensor.setPowerButton(0)
    frontSensor.powerButtonConf(0)
    frontSensor.setRepeatRate(0)

    backSensor.setNoiseThresh(0)
    backSensor.setAvgSample(1)
    backSensor.sensorEnable(1)
    backSensor.setPowerButton(0)
    backSensor.powerButtonConf(7) # Only generates an interrupt/output after 2.24s. see p. 44 
    backSensor.setRepeatRate(0)


    while True:
        status_frontSensor = frontSensor.read()
        status_backSensor = backSensor.read()
        print("Front touchpad: " + str(status_frontSensor[1]) + " // Rear touchpad: " + str(status_backSensor[1]))
        frontSensor.clearInt()
        backSensor.clearInt()
        sleep_ms(200)

