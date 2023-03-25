from serial.tools import list_ports
from pydobot import Dobot
import time

port = list_ports.comports()[1].device
device = Dobot(port=port)

device.set_io(10, False)
device.set_io(11, False)
device.set_io(12, False)
device.set_io(16, False)


