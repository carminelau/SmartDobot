---------------- INSTALLAZIONE ----------------------------------
- Installare i driver del Dobot inclusi nella cartella "Driver Dobot", file x64
- Installare driver CH340 dal file zip nella directory
- Installare Thonny 3.2.7
- Da Thonny selezionare Strumenti -> Gestisci i pacchetti ->
	cercare e installare i seguenti pacchetti:
	- sklearn
	- opencv-python 
	- pydobot2
	- numpy, pandas, random, pyserial, tools, time, termcolor
	- matplotlib

--------------- COMANDI DA TASTIERA -------------------------------
- Per terminare correttamente l'algoritmo durante la sua esecuzione
  digitare "q" (lettera q piccola) 
- Per ripristinare la posizione del Dobot e fargli assumere la posizione 
  originale tenere premuto "h" (lettera h piccola)

----------CONTENUTO DELLA CARTELLA-------------------------------
Descrizione dei file:
- cartella Temp conterrà dei file temporanei che l'algoritmo utilizza
- i file .csv contengono dati per l'addestramento dell'IA (non modificare)
- ML_Regression.py è l'algoritmo di IA (non necessita di essere aperto)
	
Per far funzionare l'algoritmo:
   AL PRIMO AVVIO:
	- test_DobotCamera.py per settare il dobot e controllare che tutto
	  funzioni
   POI:
	- "SmartDobot_BELT.py" per utilizzare la belt del Dobot, oppure
	- OPPURE "SmartDobot_NOBELT" per NON utilizzare la belt


------------ GRANDEZZA OGGETTI DA RACCOGLIERE -----------------------
- Per modificare la grandezza degli oggetti che il Dobot prende,
  modificare le variabili AREA_MIN e AREA MAX 
  nei file "SmartDobot_BELT.py" oppure "SmartDobot_NOBELT"
- segue il pattern AREA_MIN < area_oggetto < AREA MAX (ovvero l'oggetto, 
  per essere preso, deve avere un area compresa tra i 2 valori 
  AREA_MIN e AREA MAX)


-------------PROFONDITA' DEL DOBOT-----------------------------
- Per modificare quanto il braccio scende in profondità per prendere
  gli oggetti modificare la variabile MIN_Z nei file "SmartDobot_BELT.py"
  oppure "SmartDobot_NOBELT"
- valori minori faranno scendere di più il braccio durante la presa


--------------------------BELT------------------------------
Per muovere la belt bisogna modificare leggeremente la libreria:

- in Thonny nei file "SmartDobot_BELT.py" oppure "SmartDobot_NOBELT"; 
  in alto localizzare "from pydobot import Dobot" 
- cliccare tenendo premuto CTRL sulla parola "Dobot"
- si aprirà la libreria "dobot.py"
- localizzare la funzione "_set_stepper_motor"
- alla prima riga sotto tale funzione inserire: "speed = int(speed)"