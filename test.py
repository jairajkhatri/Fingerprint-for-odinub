
import serial
import struct
import time
import sys


ser = serial.Serial('/dev/ttyS1', 57600,timeout = 2)
pack = [0xef01, 0xffffffff, 0x01]

def readPacket():
    time.sleep(1)
    w = ser.inWaiting()
    ret = []
    if w >= 9:
        s = ser.read(9)
        ret.extend(struct.unpack('!HIBH', s))
        ln = ret[-1]
        time.sleep(1)
        w = ser.inWaiting()
        if w >= ln:
              s = ser.read(ln)
              print (s)
              form = '!' + 'B' * (ln - 2) + 'H'
              ret.extend(struct.unpack(form, s))
              print (s)
              return ret


def writePacket(data):
    pack2 = pack + [(len(data) + 2)]
    a = sum(pack2[-2:] + data)
    pack_str = '!HIBH' + 'B' * len(data) + 'H'
    l = pack2 + data + [a]
    s = struct.pack(pack_str, *l)
    ser.write(s)


def verifyFinger():
    data = [0x13, 0x0, 0, 0, 0]
    writePacket(data)
    s = readPacket()
    return 

def genImg():
    data = [0x1]
    writePacket(data)
    s = readPacket()
    return  

def img2Tz(buf):
    data = [0x2, buf]
    writePacket(data)
    s = readPacket()
    return 

def regModel():
    data = [0x5]
    writePacket(data)
    s = readPacket()
    return 

def store(id):
    data = [0x6, 0x1, 0x0, id]
    writePacket(data)
    s = readPacket()
    return 


if verifyFinger():
    print ('Verification Error')
    sys.exit(0)

print ('Put finger')
sys.stdout.flush()

time.sleep(1)   
while genImg():
    time.sleep(0.1)

    print ('.')
    sys.stdout.flush()

print ('')
sys.stdout.flush()

if img2Tz(1):
    print ('Conversion Error')
    sys.exit(0)

print ('Put finger again')
sys.stdout.flush()

time.sleep(1)   
while genImg():
    time.sleep(0.1)
    print ('.')
    sys.stdout.flush()

print ('')
sys.stdout.flush()

if img2Tz(2):
    print ('Conversion Error')
    sys.exit(0)

if regModel():
    print ('Template Error')
    sys.exit(0)
id = 4
if store(id):
    print ('Store Error')
    sys.exit(0) 

print ("Enrolled successfully at id %d"%id)
