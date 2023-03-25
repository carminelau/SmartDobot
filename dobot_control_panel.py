import tkinter as tk
from serial.tools import list_ports
from pydobot import Dobot
import time

def zpiu(device):
    time.sleep(1)
    pose = device.get_pose()
    position = pose.position
    device.move_to(position.x, position.y, position.z + 30, position.r)

def zmeno(device):
    time.sleep(1)
    pose = device.get_pose()
    position = pose.position
    device.move_to(position.x, position.y, position.z - 30, position.r)
   

def xmeno(device):
    time.sleep(1)
    pose = device.get_pose()
    position = pose.position
    device.move_to(position.x - 30, position.y, position.z, position.r)

def xpiu(device):
    time.sleep(1)
    pose = device.get_pose()
    position = pose.position
    device.move_to(position.x + 30, position.y, position.z, position.r)
    
def ypiu(device):
    time.sleep(1)
    pose = device.get_pose()
    position = pose.position
    device.move_to(position.x, position.y + 30, position.z, position.r)

def ymeno(device):
    time.sleep(1)
    pose = device.get_pose()
    position = pose.position
    device.move_to(position.x, position.y - 30, position.z, position.r)

def homing(device):
    device.home()
    time.sleep(4)
    
def chiudi_pompa_aria(device):
    device.set_io(10, False)
    device.set_io(11, False)
    device.set_io(12, False)
    device.set_io(16, False)
    
def record(device):
    pose = device.get_pose()
    position = pose.position
    recording.append(position)

def play(device):
    for position in recording:
        device.move_to(position.x, position.y, position.z, position.r)

def control_panel():
    port = list_ports.comports()[1].device
    device = Dobot(port=port)

    master = tk.Tk()
    master.title('Dobot Control Panel')
    master.geometry("1000x700")

    photo1 = tk.PhotoImage(file='frecciaSu.png')
    photo2 = tk.PhotoImage(file='frecciaGiu.png')
    photo3 = tk.PhotoImage(file='frecciaSinistra.png')
    photo4 = tk.PhotoImage(file='frecciaDestra.png')
    photo5 = tk.PhotoImage(file='home.png')
    photo6 = tk.PhotoImage(file='air_pump.png')
    photo7 = tk.PhotoImage(file='record.png')
    photo8 = tk.PhotoImage(file='play.png')

    buttonZpiu = tk.Button(master, image=photo1, command = lambda: zpiu(device))
    buttonZpiu.place(x=50, y=50)
    buttonZmeno = tk.Button(master, image=photo2, command = lambda: zmeno(device))
    buttonZmeno.place(x=50, y=110)
    buttonXpiu = tk.Button(master, image=photo1, command = lambda: xpiu(device))
    buttonXpiu.place(x=200, y=15)
    buttonXmeno = tk.Button(master, image=photo2, command = lambda: xmeno(device))
    buttonXmeno.place(x=200, y=125)
    buttonYmeno = tk.Button(master, image=photo3, command = lambda: ymeno(device))
    buttonYmeno.place(x=140, y=70)
    buttonYpiu = tk.Button(master, image=photo4, command = lambda: ypiu(device))
    buttonYpiu.place(x=260, y=70)
    buttonHome = tk.Button(master, image=photo5, command = lambda: homing(device))
    buttonHome.place(x=200, y=70)
    buttonPompa = tk.Button(master, image=photo6, command = lambda: chiudi_pompa_aria(device))
    buttonPompa.place(x=200, y=500)
    buttonRecord = tk.Button(master, image=photo7, command = lambda: record(device))
    buttonRecord.place(x=400, y=500)
    buttonPlay = tk.Button(master, image=photo8, command = lambda: play(device))
    buttonPlay.place(x=600, y=500)

    master.mainloop()

    device.close()
    
if __name__ == '__main__':
    control_panel()
