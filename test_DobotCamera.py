import cv2
import numpy as np
from termcolor import colored
from serial.tools import list_ports
from pydobot import Dobot

def homing(device):
    device.home()
    
def posizione_intermedia():
    initial_x = 200.0
    initial_y = 0.0
    initial_z = 170.0
    device.move_to(initial_x, initial_y, initial_z, 0.0, True)
    
def color_detection(frame):
    #cv2.imshow('originale', frame)
    frame_rosso = frame.copy()
    frame_rosa = frame.copy()
    frame_arancione = frame.copy()
    frame_giallo = frame.copy()
    frame_verde = frame.copy()
    frame_azzurro = frame.copy()
    frame_blu = frame.copy()
    frame_viola = frame.copy()
    
    frame_colori_selezionati = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #--------------------- COLORE ROSA -------------------------------------------
    low_rosa = np.array(  [0,0,70])
    high_rosa = np.array(  [60,80,255])
    rosa_mask = cv2.inRange(frame, low_rosa, high_rosa)
    
    solo_rosa = cv2.bitwise_and(frame_rosa, frame_rosa, mask=rosa_mask)
    
    # ------------------- COLORE ROSSO --------------------------------------------
    lower_red = np.array(  [0,75,75])
    upper_red = np.array(  [10,255,255])
    rosso_mask1= cv2.inRange(frame, lower_red, upper_red)

    lower_red = np.array(  [170,75,75])
    upper_red = np.array(  [180,255,255])
    rosso_mask2 = cv2.inRange(frame,lower_red,upper_red)
    # maschera rossa completa
    rosso_mask = rosso_mask1 + rosso_mask2
    solo_rosso = cv2.bitwise_and(frame_rosso, frame_rosso, mask=rosso_mask)
    
    #--------------------- COLORE ARANCIONE -------------------------------------------
    low_arancione = np.array(  [11,125,125])
    high_arancione = np.array(  [18,255,255])
    arancione_mask = cv2.inRange(frame, low_arancione, high_arancione)
    
    solo_arancione = cv2.bitwise_and(frame_arancione, frame_arancione, mask=arancione_mask)
    
    # ------------------- COLORE GIALLO --------------------------------------------
    low_giallo = np.array(  [19, 100, 100])
    high_giallo = np.array(  [35, 255, 255])
    giallo_mask = cv2.inRange(frame, low_giallo, high_giallo)
    
    solo_giallo = cv2.bitwise_and(frame_giallo, frame_giallo, mask=giallo_mask)
    
    # ------------------- COLORE VERDE --------------------------------------------
    low_verde = np.array(  [36 , 25, 25])
    high_verde = np.array(  [80, 255, 255])
    verde_mask = cv2.inRange(frame, low_verde, high_verde)
    
    solo_verde = cv2.bitwise_and(frame_verde, frame_verde, mask=verde_mask)
    
    # ------------------- COLORE AZZURRO --------------------------------------------
    low_azzurro = np.array(  [81, 25, 25])
    high_azzurro = np.array(  [100, 255, 255])
    azzurro_mask = cv2.inRange(frame, low_azzurro, high_azzurro)
    
    solo_azzurro = cv2.bitwise_and(frame_azzurro, frame_azzurro, mask=azzurro_mask)

    # ------------------- COLORE BLU --------------------------------------------
    low_blu = np.array(  [101, 25, 25])
    high_blu = np.array(  [127, 255, 255])
    blu_mask = cv2.inRange(frame, low_blu, high_blu)
    
    solo_blu = cv2.bitwise_and(frame_blu, frame_blu, mask=blu_mask)
    
    # ------------------- COLORE VIOLA --------------------------------------------
    low_viola = np.array(  [128, 25, 25])
    high_viola = np.array(  [169, 255, 255])
    viola_mask = cv2.inRange(frame, low_viola, high_viola)
    
    solo_viola = cv2.bitwise_and(frame_viola, frame_viola, mask=viola_mask)
    
    # ------------------- STAMPO E RITORNO --------------------------------------------
    #frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    #cv2.imshow('rosso', solo_rosso)
    #cv2.imshow('blu', solo_blu)
    #cv2.imshow('verde', solo_verde)
    #cv2.imshow('giallo', solo_giallo)
    #cv2.imshow('rosa', solo_rosa)
    #cv2.imshow('arancione', solo_arancione)
    
    mask_totale =  rosso_mask + arancione_mask + giallo_mask + verde_mask + azzurro_mask + blu_mask + viola_mask
    solo_colori = cv2.bitwise_and(frame_colori_selezionati, frame_colori_selezionati, mask=mask_totale)
    cv2.imshow('solo_colori', solo_colori)
    
    return solo_rosso,solo_arancione,solo_giallo,solo_verde,solo_azzurro,solo_blu,solo_viola

# MAIN ------------------------------------
print('Cerco il Dobot...')
try:
    port = list_ports.comports()[1].device
    print(colored('   [ V ] Trovato!', 'green'))
    device = Dobot(port=port)
    #device.set_home(200.0, 0.0, 100.0, 0.0)
                            # settare la posizione home del Dobot perchè di default
                            # è troppo basse
    homing(device)
    posizione_intermedia()
except:
    print(colored('  [ X ] Non ho trovato il Dobot', 'red'))

print('Cerco la camera...')
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print(colored('   [ V ] Trovata!', 'green'))
except:
    print(colored('   [ X ] Non ho trovato la camera', 'red'))

# CALIBRAZIONE DELLA CAMERA
    cap.set(cv2.CAP_PROP_AUTO_WB , 1) # auto-bilanciamento del bianco[1 = disattivato]
    cap.set(10, 100)                  # luminosità [min: 0, max: 255]  
    cap.set(11, 30)                   # contrasto [min: 0, max: 255]     
    cap.set(12, 30)                   # saturazione [min: 0, max: 255] 
    cap.set(15, -5)                   # gain [-5 = immagine piu luminosa]
    cap.set(45, 4000)                 # temperatura del bianco [0 - 10000]
    #cap.set(cv2.CAP_PROP_SETTINGS, 1)   # visualizzare pannello della webcam

while True:
    cap.set(45,4000)
    _, frame = cap.read()
    cv2.imshow('frame_catturato', frame)
    color_detection(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
    
    