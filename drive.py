
dummy = True
try:
    import smbus
    dummy = False
    print 'smbus is available'
except:
    print 'smbus not available; in dummy mode'
    
import time

MD25_DEFAULT_ADDRESS = 0x58
MD25_DEFAULT_MODE = 0

MD25_REGISTER_SPEED1 =              0x00
MD25_REGISTER_SPEED2_TURN =         0x01
MD25_REGISTER_ENC1A =               0x02
MD25_REGISTER_ENC1B =               0x03
MD25_REGISTER_ENC1C =               0x04
MD25_REGISTER_ENC1D =               0x05
MD25_REGISTER_ENC2A =               0x06
MD25_REGISTER_ENC2B =               0x07
MD25_REGISTER_ENC2C =               0x08
MD25_REGISTER_ENC2D =               0x09
MD25_REGISTER_BATTERY_VOLTS =       0x0A
MD25_REGISTER_MOTOR1_CURRENT =      0x0B
MD25_REGISTER_MOTOR2_CURRENT =      0x0C
MD25_REGISTER_SOFTWARE_REV =        0x0D
MD25_REGISTER_ACCELERATION_RATE =   0x0E
MD25_REGISTER_MODE =                0x0F
MD25_REGISTER_COMMAND =             0x10

class md25:
    def __init__(self, mode=MD25_DEFAULT_MODE, bus=1, address=MD25_DEFAULT_ADDRESS):
        self.mode = mode
        self.address = address
        self.bus = None
        print 'dummy is',dummy
        if not dummy:
            print 'setting up SMBus'
            self.bus = smbus.SMBus(bus)
            self.bus.write_byte_data(self.address,MD25_REGISTER_MODE, self.mode)
        
    def ensureSet(self,args,message='',all=True):
        for name in args:
            if None == args[name]:
                if all:
                    raise ValueError("%s was not set. %s"%(name,message));
            else:
                return
        raise ValueError("one of %s should be set. %s"%(args.keys(),message));
        
    def ensureRange(self,range,args,message=''):
        for name in args:
            if args[name] and (args[name] < range[0] or args[name] > range[1]):
                raise ValueError("%s (%i) was out of range (%i - %i). %s"%(name, args[name], range[0], range[1], message))
    
    def drive(self, motor0=None, motor1=None, speed=None, turn=None):
        print motor0, motor1, speed, turn
        if 0 == self.mode:
            self.ensureSet({'motor0':motor0,'motor1':motor1}, all=False)
            self.ensureRange((1,255),{'motor0':motor0,'motor1':motor1})
        if 1 == self.mode:
            self.ensureSet({'motor0':motor0,'motor1':motor1}, all=False)
            self.ensureRange((-128,127),{'motor0':motor0,'motor1':motor1})
        if (0 == self.mode or 1 == self.mode) and self.bus:
            if motor0:
                self.bus.write_byte_data(self.address, MD25_REGISTER_SPEED1, motor0)
            if motor1:
                self.bus.write_byte_data(self.address, MD25_REGISTER_SPEED2_TURN, motor1)
        if 2 == self.mode:
            self.ensureSet({'speed':speed,'turn':turn}, all=False)
            self.ensureRange((1,255),{'speed':speed,'turn':turn})
        if 3 == self.mode:
            self.ensureSet({'speed':speed,'turn':turn}, all=False)
            self.ensureRange((-128,127),{'speed':speed,'turn':turn})
        if (2 == self.mode or 3 == self.mode) and self.bus:
            if speed:
                self.bus.write_byte_data(self.address, MD25_REGISTER_SPEED1, speed)
            if turn:
                self.bus.write_byte_data(self.address, MD25_REGISTER_SPEED2_TURN, turn)
                
    def stop(self):
        print('STOP!!!')
        if (0 == self.mode or 2 == self.mode) and self.bus:
            self.bus.write_byte_data(self.address, MD25_REGISTER_SPEED1, 128)
            self.bus.write_byte_data(self.address, MD25_REGISTER_SPEED2_TURN, 128)
        if (1 == self.mode or 3 == self.mode) and self.bus:
            self.bus.write_byte_data(self.address, MD25_REGISTER_SPEED1, 0)
            self.bus.write_byte_data(self.address, MD25_REGISTER_SPEED2_TURN, 0)
        
    def battery(self):
        if self.bus:
            return self.bus.read_byte_data(self.address, MD25_REGISTER_BATTERY_VOLTS)
        else:
            return 120