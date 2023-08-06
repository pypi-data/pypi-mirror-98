import serial.tools.list_ports
import serial
import time


class MXSerial:
    def __init__(self, com, bps):
        self.ser = serial.Serial(com, bps, timeout=5)
        time.sleep(1)

    @classmethod
    def getCom(cls, num=None):
        ComPorts = []
        for comPort in serial.tools.list_ports.comports():
            ComPorts.append(str(comPort).replace('/dev/cu.', '/dev/tty.').replace(' - n/a', ''))

        try:
            return ComPorts[num]
        except:
            return ComPorts

    def send(self, data):
        self.ser.write(data.encode())

    def readline(self):
        return self.ser.readline().decode().strip("\r\n")

    def read(self):
        return self.ser.read().decode().strip("\r\n")

    def close(self):
        self.ser.close()
