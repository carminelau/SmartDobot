import time
import threading
from cv2 import destroyAllWindows, waitKey, CAP_PROP_AUTO_WB, CAP_DSHOW, VideoCapture, createTrackbar, namedWindow, bitwise_and, inRange, CHAIN_APPROX_SIMPLE, RETR_EXTERNAL, findContours, threshold, THRESH_BINARY, COLOR_BGR2GRAY, COLOR_BGR2HSV, circle, imshow, cvtColor, getTrackbarPos, FONT_HERSHEY_SIMPLEX, createBackgroundSubtractorKNN, putText, boundingRect, minAreaRect, contourArea, arcLength, drawContours, boxPoints, approxPolyDP, addWeighted, imwrite
from numpy import array, int0
from serial.tools.list_ports import comports
from pydobot import Dobot
import csv
from datetime import datetime
from time import sleep
from ML_Regression import x_predizione, y_predizione, r_predizione, crea_regressore_x, crea_regressore_y, crea_regressore_r
from termcolor import colored
from tkinter import PhotoImage, Tk, Button
from enum import IntEnum


class MODE_PTP(IntEnum):

    JUMP_XYZ = 0x00
    MOVJ_XYZ = 0x01
    MOVL_XYZ = 0x02
    JUMP_ANGLE = 0x03
    MOVJ_ANGLE = 0x04
    MOVL_ANGLE = 0x05
    MOVJ_INC = 0x06
    MOVL_INC = 0x07
    MOVJ_XYZ_INC = 0x08
    JUMP_MOVL_XYZ = 0x09


class Panel:
    # DEFINIZIONE PARAMETRI FUNZIONAMENTO DOBOT

    def init(self):
        self.recording = []
        # per la fase di calibrazione del dobot bisogna modificare questi parametri:
        #   - self.areaMin e self.areaMax per l'area che deve riconoscere
        #   - self.min_z per la distanza dal piano di lavoro
        #   - self.luminosita e self.contrasto per il contrasto e la luminosità della webcam
        #   - self.gain per il gain della webcam
        self.areaMin, self.areaMax, self.min_z, self.stop_flag, self.track_flag, self.luminosita, self.contrasto, self.gain = 400, 50000, - \
            70.0, False, False, 95, 37, -7

        print('Cerco il Dobot...')
        try:
            port = comports()[0].device
            print(comports()[0].device)
            self.device = Dobot(port=port)
            self.device._set_queued_cmd_clear()
            self.homing()
            self.posizione_intermedia()
            return "OK INIT"
        except:
            return "ERRORE INIT"

        # master = Tk()
        # master.title('Dobot Control Panel')
        # master.geometry("350x350")

        # photo1 = PhotoImage(file='frecciaSu.png')
        # photo2 = PhotoImage(file='frecciaGiu.png')
        # photo3 = PhotoImage(file='frecciaSinistra.png')
        # photo4 = PhotoImage(file='frecciaDestra.png')
        # photo5 = PhotoImage(file='home.png')
        # photo6 = PhotoImage(file='air_pump.png')
        # photo7 = PhotoImage(file='record.png')
        # photo8 = PhotoImage(file='play.png')
        # photo9 = PhotoImage(file='imagedetection.png')
        # #photo10 = PhotoImage(file='stop.png')

        # buttonZpiu = Button(master, image=photo1, command = self.zpiu)
        # buttonZpiu.grid(column=0, row=0)
        # buttonZmeno = Button(master, image=photo2, command = self.zmeno)
        # buttonZmeno.grid(column=0, row=2)
        # buttonXpiu = Button(master, image=photo1, command = self.xpiu)
        # buttonXpiu.grid(column=2, row=0)
        # buttonXmeno = Button(master, image=photo2, command = self.xmeno)
        # buttonXmeno.grid(column=2, row=2)
        # buttonYmeno = Button(master, image=photo3, command = self.ymeno)
        # buttonYmeno.grid(column=1, row=1)
        # buttonYpiu = Button(master, image=photo4, command = self.ypiu)
        # buttonYpiu.grid(column=3, row=1)
        # buttonHome = Button(master, image=photo5, command = self.homing)
        # buttonHome.grid(column=2,row=1)
        # buttonPompa = Button(master, image=photo6, command = self.chiudi_pompa_aria)
        # buttonPompa.grid(column=0,row=3)
        # buttonRecord = Button(master, image=photo7, command = self.record)
        # buttonRecord.grid(column=1,row=3)
        # buttonPlay = Button(master, image=photo8, command = self.play)
        # buttonPlay.grid(column=2,row=3)
        # buttonImageDetection = Button(master, image=photo9, command = self.imagedetection)
        # buttonImageDetection.grid(column=0,row=4)
        # #buttonStop = Button(master, image=photo10, command = lambda: stop())
        # #buttonStop.grid(column=1,row=4)

        # master.mainloop()

# FUNZIONALITA' DEL DOBOT
    # funzione per effettuare la home del dobot
    def homing(self):
        try:
            self.device.home()
            return "OK HOMING"
        except:
            return "ERRORE HOMING"

    # funzione per spegnere la pompa di aria del dobot
    def spegni_pompa_aria(self):
        try:
            self.device.set_io(10, False)
            self.device.set_io(11, False)
            self.device.set_io(12, False)
            self.device.set_io(16, False)
            return "OK POMPA SPENTA"
        except:
            return "ERRORE SPEGNIMENTO POMPA"

    # funzione per aprire la chela del dobot
    def apri_chela(self):
        try:
            self.device.grip(enable=False)
            sleep(1)
            return "OK APRI CHELA"
        except:
            return "ERRORE APERTURA CHELA"

    # funzione per chiudere la chela del dobot
    def chiudi_chela(self):
        try:
            self.device.grip(enable=True)
            sleep(1)
            return "OK CHIUDI CHELA"
        except:
            return "ERRORE CHIUSURA CHELA"

    # funzione per avviare il rullo
    def avvia_rullo(self, speed, dir, iterface):

        self.device.conveyor_belt(speed, direction=dir, interface=iterface)

    # funzione per avviare il rullo con distanza
    def avvia_rullo_sett(self, speed, distance, direction, interface):
        self.device.conveyor_belt_distance(
            speed, distance, direction, interface)

    # funzione per fermare il rullo
    def ferma_rullo(self):
        try:
            self.device.conveyor_belt(0)
            return "OK FERMA RULLO"
        except:
            return "ERRORE FERMA RULLO"

    # funzione per stampare la posizione del dobot
    def stampa_posizione(self):
        pose = self.device.get_pose()
        position = pose.position
        print(str(position))

    # MOVIMENTO DEL DOBOT
    def scuoti(self):
        # SCUOTE IL BRACCIO
        posa_x, posa_y, posa_z = 1, -175.0, 50.0
        self.device.move_to(posa_x+50, posa_y, posa_z, 0.0, True)
        self.device.move_to(posa_x-50, posa_y, posa_z, 0.0, True)

    def posa_oggetto(self):
        # POSIZIONE DI LATO
        posa_x, posa_y, posa_z = 1, -175.0, 50.0
        self.device.move_to(posa_x-20, posa_y, posa_z, 0.0, True)
        self.apri_chela()
        self.scuoti()

    # funzione per muovere il dobot nella posizione intermedia
    def posizione_intermedia(self):
        initial_x, initial_y, initial_z = 200.0, 0.0, 170.0
        self.device.move_to(initial_x, initial_y, initial_z, 0.0, True)

    # funzione per la prima fase della presa dell'oggetto
    def prima_fase_presa(self, x, y, r):
        self.device.move_to(x, y, 150.0, 15.0, True)
        sleep(1)  # MOVL_XYZ

    # funzione per muovere il dobot in una positione specifica (x,y,z)
    def sposta(self, x, y, z):
        try:
            self.device.move_to(float(x), float(y), float(z),
                                15.0, mode=MODE_PTP.MOVJ_XYZ)
            sleep(1)
            return "OK DOBOT SI SPOSTA"
        except:
            return "ERRORE SPOSTAMENTO DOBOT"

    # funzione per usare il rail del dobot
    def rail(self, x, y, r):
        self.device.move_to(x, y, z=150.0, r=float(15.0),
                            mode=MODE_PTP.MOVL_XYZ)
        sleep(1)

    # funzione per la seconda fase della presa dell'oggetto
    def seconda_fase_presa(self, x, y, z, r):
        self.device.move_to(x, y, z, r, True)
        sleep(1)
        self.apri_chela()

    # funzione per la terza fase della presa dell'oggetto
    def terza_fase_presa(self, x, y, z, r):
        self.device.move_to(x, y, z+20, r, True)
        sleep(1)
        self.device.move_to(x, y, z, r, True)
        self.chiudi_chela()

    # funzione per prendere l'oggetto all'altezza minima
    def prendi(self, x, y, r):
        self.device.clear_alarms()
        z = self.min_z

        x, y, r = round(float(x), 2), round(float(y), 2), round(float(r), 2)
        self.posizione_intermedia()

        # controllo che la coordinata x calcolata non superi i limiti del Dobot
        x = x+5
        if x <= 195:
            x = 195
        elif x >= 265:
            x = 265

        # controllo che la coordinata y calcolata non superi i limiti del Dobot
        if y < 0:
            y = y+2
        if y > 0:
            y = y+8
        if y > 80:
            y = 80
        elif y < -70:
            y = -70

        # r=15

        # 3 FASI PRESA
        self.prima_fase_presa(x=x, y=y, r=r)
        self.seconda_fase_presa(x=x, y=y, r=r, z=z)
        self.terza_fase_presa(x=x, y=y, r=r, z=z)  # abbasso il braccio

        time.sleep(1)
        self.posizione_intermedia()
        time.sleep(1)
        self.posa_oggetto()
        time.sleep(1)
        self.apri_chela()
        time.sleep(1)
        self.chiudi_pompa_aria()
        time.sleep(1)
        self.posizione_intermedia()
        time.sleep(2)

    # funzione per prendere l'oggetto specificando l'altezza
    def prendi(self, x, y, z, r):
        self.device.clear_alarms()

        x, y, z, r = round(float(x), 2), round(
            float(y), 2), round(float(z), 2), round(float(r), 2)
        self.posizione_intermedia()

        # controllo che la coordinata x calcolata non superi i limiti del Dobot
        x = x+5
        if x <= 195:
            x = 195
        elif x >= 265:
            x = 265

        # controllo che la coordinata y calcolata non superi i limiti del Dobot
        if y < 0:
            y = y+2
        if y > 0:
            y = y+8
        if y > 80:
            y = 80
        elif y < -70:
            y = -70

        if z == -300:
            z = self.min_z

        # mi sposto in posizione x,y dell'oggetto
        self.prima_fase_presa(x=x, y=y, r=r)
        self.seconda_fase_presa(x=x, y=y, z=z, r=r)  # ruoto la chela
        self.terza_fase_presa(x=x, y=y, z=z, r=r)  # abbasso il braccio

        self.posizione_intermedia()
        time.sleep(1)
        self.posa_oggetto()
        time.sleep(1)
        self.apri_chela()
        time.sleep(1)
        self.chiudi_pompa_aria()
        time.sleep(1)
        self.posizione_intermedia()
        time.sleep(2)

    # funzione per prendere tutti gli oggetti riconosciuti, viene richiamata dall'image recognition
    def prendi_tutto(self, c, lista_contorni, regressore_x, regressore_y, regressore_r):
        for cnt in lista_contorni:
            (x, y, w, h) = boundingRect(cnt)

            rect = minAreaRect(cnt)
            punti_inizio, punti_centrali, angolo_rotazione = rect
            box = boxPoints(rect)
            box = int0(box)
            area, perimeter = contourArea(box), arcLength(box, True)

            if area > self.areaMin and area < self.areaMax:
                x_centro, y_centro = int(x + (w/2)), int(y + (w/2))
                x, y, r = x_predizione(regressore_x, x_centro, y_centro), y_predizione(
                    regressore_y, x_centro, y_centro), r_predizione(regressore_r, -angolo_rotazione)
                sleep(1)
                print(c)
                self.prendi(x-6, y-5, -30, r-50)

        try:
            lista_contorni.pop(0)
        except:
            print("nessun contorno tolto")

        self.posizione_intermedia()
        self.spegni_pompa_aria()
        self.imagedetection()
        print(colored('   Fatto!', 'yellow'))

    # funzione per far camminare il rullo
    def avanti_tappeto(self):
        self.avvia_rullo()
        sleep(0.5)
        self.ferma_rullo()

    # FUNZIONI DI IMAGE PROCESSING

    def on_trackbar(self, solo_colori):
        self.luminosita = getTrackbarPos('Luminosita', 'colori')
        self.contrasto = getTrackbarPos('Contrasto', 'colori')
        self.gain = getTrackbarPos('Gain', 'colori')
        btn = getTrackbarPos('Stop', 'colori')
        if btn == 1:
            self.stop_flag = True

    def trova_contorni(self, frame, lista_contorni):
        belt = frame
        gray_belt = cvtColor(belt, COLOR_BGR2GRAY)
        _, _threshold = threshold(gray_belt, 75, 255, THRESH_BINARY)
        contours, _ = findContours(
            _threshold, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
        lista_contorni.extend(contours)
        # imshow('black&white', _threshold)
        return lista_contorni

    def color_detection(self, frame):
        # imshow('originale', frame)
        frame_rosso = frame.copy()
        frame_rosa = frame.copy()
        frame_arancione = frame.copy()
        frame_giallo = frame.copy()
        frame_verde = frame.copy()
        frame_azzurro = frame.copy()
        frame_blu = frame.copy()
        frame_viola = frame.copy()

        frame_colori_selezionati = frame.copy()
        frame = cvtColor(frame, COLOR_BGR2HSV)

        # --------------------- COLORE ROSA -------------------------------------------
        low_rosa, high_rosa = array([0, 0, 70]), array([60, 80, 255])
        rosa_mask = inRange(frame, low_rosa, high_rosa)

        solo_rosa = bitwise_and(frame_rosa, frame_rosa, mask=rosa_mask)

        # ------------------- COLORE ROSSO --------------------------------------------
        lower_red, upper_red = array([0, 75, 75]), array([10, 255, 255])
        rosso_mask1 = inRange(frame, lower_red, upper_red)

        lower_red, upper_red = array([170, 75, 75]), array([180, 255, 255])
        rosso_mask2 = inRange(frame, lower_red, upper_red)
        # maschera rossa completa
        rosso_mask = rosso_mask1 + rosso_mask2
        solo_rosso = bitwise_and(frame_rosso, frame_rosso, mask=rosso_mask)

        # --------------------- COLORE ARANCIONE -------------------------------------------
        low_arancione, high_arancione = array(
            [11, 125, 125]), array([18, 255, 255])
        arancione_mask = inRange(frame, low_arancione, high_arancione)

        solo_arancione = bitwise_and(
            frame_arancione, frame_arancione, mask=arancione_mask)

        # ------------------- COLORE GIALLO --------------------------------------------
        low_giallo, high_giallo = array([19, 75, 75]), array([35, 255, 255])
        giallo_mask = inRange(frame, low_giallo, high_giallo)

        solo_giallo = bitwise_and(frame_giallo, frame_giallo, mask=giallo_mask)

        # ------------------- COLORE VERDE --------------------------------------------
        low_verde, high_verde = array([36, 50, 50]), array([80, 255, 255])
        verde_mask = inRange(frame, low_verde, high_verde)

        solo_verde = bitwise_and(frame_verde, frame_verde, mask=verde_mask)

        # ------------------- COLORE AZZURRO --------------------------------------------
        low_azzurro, high_azzurro = array([81, 50, 50]), array([100, 255, 255])
        azzurro_mask = inRange(frame, low_azzurro, high_azzurro)

        solo_azzurro = bitwise_and(
            frame_azzurro, frame_azzurro, mask=azzurro_mask)

        # ------------------- COLORE BLU --------------------------------------------
        low_blu, high_blu = array([101, 50, 50]), array([127, 255, 255])
        blu_mask = inRange(frame, low_blu, high_blu)

        solo_blu = bitwise_and(frame_blu, frame_blu, mask=blu_mask)

        # ------------------- COLORE VIOLA --------------------------------------------
        low_viola, high_viola = array([128, 50, 50]), array([169, 255, 255])
        viola_mask = inRange(frame, low_viola, high_viola)

        solo_viola = bitwise_and(frame_viola, frame_viola, mask=viola_mask)

        # ------------------- STAMPO E RITORNO --------------------------------------------
        # frame = cvtColor(frame, COLOR_HSV2BGR)
        # imshow('rosso', solo_rosso)
        # imshow('blu', solo_blu)
        # imshow('verde', solo_verde)
        # imshow('giallo', solo_giallo)
        # imshow('rosa', solo_rosa)
        # imshow('arancione', solo_arancione)

        mask_totale = rosso_mask + arancione_mask + giallo_mask + \
            verde_mask + azzurro_mask + blu_mask + viola_mask

        solo_colori = bitwise_and(
            frame_colori_selezionati, frame_colori_selezionati, mask=mask_totale)
        namedWindow('colori')
        if self.track_flag == False:
            self.track_flag = True
            createTrackbar('Luminosita', 'colori', 100, 255,
                           lambda: self.on_trackbar(solo_colori))
            createTrackbar('Contrasto', 'colori', 30, 255,
                           lambda: self.on_trackbar(solo_colori))
            createTrackbar('Gain', 'colori', 5, 10,
                           lambda: self.on_trackbar(solo_colori))
            createTrackbar('Stop', 'colori', 0, 1, self.on_trackbar)
        self.on_trackbar(solo_colori)
        imshow('colori', solo_colori)

        return solo_rosso, solo_arancione, solo_giallo, solo_verde, solo_azzurro, solo_blu, solo_viola

    # funzione che trova i contorni dei colori selezionati e prende quegli oggetti
    def guarda_e_prendi(self, c, frame, lista_contorni, regressore_x, regressore_y, regressore_r):
        solo_rosso, solo_arancione, solo_giallo, solo_verde, solo_azzurro, solo_blu, solo_viola = self.color_detection(
            frame)

        lista_contorni = self.trova_contorni(solo_rosso, lista_contorni)
        lista_contorni = self.trova_contorni(solo_arancione, lista_contorni)
        lista_contorni = self.trova_contorni(solo_giallo, lista_contorni)
        lista_contorni = self.trova_contorni(solo_verde, lista_contorni)
        lista_contorni = self.trova_contorni(solo_azzurro, lista_contorni)
        lista_contorni = self.trova_contorni(solo_blu, lista_contorni)
        lista_contorni = self.trova_contorni(solo_viola, lista_contorni)

        imshow("frame", frame)

        for cnt in lista_contorni:
            # contorni approssimati
            (x, y, w, h) = boundingRect(cnt)

            # contorni precisi
            rect = minAreaRect(cnt)
            punti_inizio, punti_centrali, angolo_rotazione = rect
            box = boxPoints(rect)
            box = int0(box)

            # calcolo area e perimetro in base ai contorni precisi
            area, perimeter = contourArea(box), arcLength(box, True)

            if area > self.areaMin and area < self.areaMax:
                # trovo la forma dell'oggetto
                approx = approxPolyDP(box, 0.1 * arcLength(cnt, True), True)

                # calcolo il centro dell'oggetto
                x_centro, y_centro = int(x + (w/2)), int(y + (h/2))

                # disegno sul frame le informazioni ricavate dai contorni
                drawContours(frame, [box], -1, (0, 0, 255), 2)  # contorni
                # putText(frame, 'area: '+str(area), (x, y-75), 1, 1, (0, 255, 0)) # scrivo l'area
                circle(frame, (int(x_centro), int(y_centro)),
                       2, (255, 255, 255), 2)  # sx
                putText(frame, str('x: '+str(x_centro)+'| y: ' + str(y_centro)),
                        (int(x_centro-15), int(y_centro-15)), 1, 1, (255, 255, 255))  # scrivo la forma

                print(colored('   Prendo gli oggetti', 'yellow'))
                # print("1x")
                # imwrite("C:\\Users\\Utente\\Desktop\\SmartDobot30-03\\SmartDobot\\Frame\\frame%d.jpg"% round(time.time()),frame)

                self.prendi_tutto(c, lista_contorni,
                                  regressore_x, regressore_y, regressore_r)
                lista_contorni = lista_contorni.clear()
            else:
                self.imagedetection()

    # funzione per l'arresto forzato del dobot
    def stopping(self):
        self.device._set_queued_cmd_clear()
        self.device.close()


# -------------------------------------------------------------------------

# >>>>>>>>>>>>>>>>>>>>>>> MAIN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # funzione per l'image detection, parte con la ricerca della videocamera e prosegue con i vari settaggi e il riconoscimento degli oggetti. Dopo che ha riconosciuto gli oggetti, li prende con la funzione prendi_tutto

    def imagedetection(self):
        self.stop_flag = self.track_flag = False

        sub_background = createBackgroundSubtractorKNN()
        event = threading.Event()
        # print('Cerco il Dobot...')
        # try:
        # port = comports()[1].device
        # print(colored('  [ V ] Trovato!', 'green'))
        # device = Dobot(port=port)
        # homing(device)
        # posizione_intermedia()
        # except:
        # print(colored('  [ X ] Non ho trovato il Dobot', 'red'))

        print('Cerco la camera...')
        try:
            cap = VideoCapture(0, CAP_DSHOW)
            print(colored('   [ V ] Trovata!', 'green'))
        except:
            print(colored('   [ X ] Non ho trovato la camera', 'red'))

        print("Avvio gli algoritmi di IA...")
        try:
            regressore_x, regressore_y, regressore_r = crea_regressore_x(
            ), crea_regressore_y(), crea_regressore_r()
            print(colored('   [ V ] Fatto!', 'green'))
        except:
            print(colored('   [ X ] Ops, problema con gli algoritmi ', 'red'))

        print('Ok, tutto fatto! Inizio a lavorare')
        # ferma_rullo(device)
        c = 0
        while self.stop_flag == False:
            # CALIBRAZIONE DELLA CAMERA
            # auto-bilanciamento del bianco[1 = disattivato]
            cap.set(CAP_PROP_AUTO_WB, 1)
            # luminosità [min: 0, max: 255]
            cap.set(10, self.luminosita)
            # contrasto [min: 0, max: 255]
            cap.set(11, self.contrasto)
            cap.set(12, 30)                   # saturazione [min: 0, max: 255]
            # gain [-5 = immagine piu luminosa]
            cap.set(15, -self.gain)
            # temperatura del bianco [0 - 10000]
            cap.set(45, 4000)
            # cap.set(cv2.CAP_PROP_SETTINGS, 1)   # visualizzare pannello della webcam

            lista_contorni = []

            # avanti_tappeto(device) # sposto la belt
            sleep(0.4)
            # frame=None
            rec, frame = cap.read()  # vedo l'immagine
            print(rec)
            # imwrite("C:\\Users\\Utente\\Desktop\\SmartDobot30-03\\SmartDobot\\Frame\\frame%d.jpg"% c,frame)
            c += 1
            self.color_detection(frame)

            self.guarda_e_prendi(c, frame, lista_contorni, regressore_x,
                                 regressore_y, regressore_r)  # prendo gli oggetti
            event.wait(20)
            if waitKey(1) & 0xFF == ord('q'):
                break

            # -------------- FUNZIONI UTILI --------------------------

            if waitKey(1) & 0xFF == ord('p'):
                pose = self.device.get_pose()
                position = pose.position
                self.stampa_posizione()

            if waitKey(1) & 0xFF == ord('a'):
                pose = self.device.get_pose()
                position = pose.position
                self.device.move_to(position.x, position.y,
                                    position.z, position.r+10, True)

            if waitKey(1) & 0xFF == ord('b'):
                pose = self.device.get_pose()
                position = pose.position
                self.device.move_to(position.x, position.y,
                                    position.z, position.r-10, True)

            if waitKey(1) & 0xFF == ord('h'):
                print("Riposizioni il braccio...")
                self.homing()
                self.posizione_intermedia()
                print("   [ V ] Riposizionato!")

            if waitKey(1) & 0xFF == ord('k'):
                self.device.clear_alarms()
                self.posizione_intermedia()

        print(colored('>>> Termino l algoritmo <<<', 'blue'))
        # ferma_rullo(device)
        cap.release()

        destroyAllWindows()

    # funzione per muovere il dobot con z + 30
    def zpiu(self):
        sleep(1)
        pose = self.device.get_pose()
        position = pose.position
        self.device.move_to(position.x, position.y,
                            position.z + 30, position.r)

    # funzione per muovere il dobot con z - 30
    def zmeno(self):
        sleep(1)
        pose = self.device.get_pose()
        position = pose.position
        self.device.move_to(position.x, position.y,
                            position.z - 30, position.r)

    # funzione per muovere il dobot con x - 30
    def xmeno(self):
        sleep(1)
        pose = self.device.get_pose()
        position = pose.position
        self.device.move_to(position.x - 30, position.y,
                            position.z, position.r)

    # funzione per muovere il dobot con x + 30
    def xpiu(self):
        sleep(1)
        pose = self.device.get_pose()
        position = pose.position
        self.device.move_to(position.x + 30, position.y,
                            position.z, position.r)

    # funzione per muovere il dobot con y + 30
    def ypiu(self):
        sleep(1)
        pose = self.device.get_pose()
        position = pose.position
        self.device.move_to(position.x, position.y +
                            30, position.z, position.r)

    # funzione per muovere il dobot con y - 30
    def ymeno(self):
        sleep(1)
        pose = self.device.get_pose()
        position = pose.position
        self.device.move_to(position.x, position.y -
                            30, position.z, position.r)

    # funzione per chiudere la pompa dell'aria
    def chiudi_pompa_aria(self):
        self.device.set_io(10, False)
        self.device.set_io(11, False)
        self.device.set_io(12, False)
        self.device.set_io(16, False)

    # funzione per registrare le posizioni del dobot per poi replicarle, NON FUNZIONA
    def record(self):
        pose = self.device.get_pose()
        position = pose.position
        self.recording.append(position)

    # funzione per riprodurre le posizioni registrate, NON FUNZIONA
    def play(self):
        for position in self.recording:
            self.device.move_to(position.x, position.y, position.z, position.r)
        self.recording.clear()
