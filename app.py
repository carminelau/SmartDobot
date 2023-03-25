from flask import Flask, request
from SmartDobot_NOBELT import Panel

app = Flask(__name__)

# route per inizializzare il dobot collegato. Viene richiamata una sola volta oppure dopo ogni volta che si è lanciato il comando stop
@app.route('/')
def home():
    global prova
    prova = Panel()
    return prova.init()

# route per far prendere al dobot un oggetto in una posizione specifica, è possibile specificare anche il raggio di azione del braccio
@app.route('/goto', methods=['GET'])
def goto():
    if ('z' not in request.args.keys()):
        x = request.args.get('x')
        y = request.args.get('y')
        r = request.args.get('r')
        
        prova.prendi(x,y,prova.min_z,r)
    else:
        x = request.args.get('x')
        y = request.args.get('y')
        z = request.args.get('z')
        r = request.args.get('r')
        
        prova.prendi(x,y,z,r)
    
    return "OK"

# route per far spostare il dobot in una posizione specifica
@app.route('/sposta', methods=['GET'])
def sposta():
    
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')
    
    result = prova.sposta(x,y,z)
    return result

# route per far partire il riconoscimento automatico degli oggetti attraverso la webcam
@app.route('/imagedetection', methods=['GET'])
def imagedet():
    prova.imagedetection()
    return "comando inviato"

# route per avviare il rullo, ma non è presente a Frigento
@app.route('/avviarullo', methods=['GET'])
def avviarullo():
    interface=request.args.get('interface')
    if "dist" not in request.args.keys():
        if "speed" not in request.args.keys():
            if "direction" not in request.args.keys():
                prova.avvia_rullo(0.5,1,interface)
            else:
                prova.avvia_rullo(0.5,int(request.args.get("direction")),interface)
        else:
            prova.avvia_rullo(float(request.args.get("speed")),int(request.args.get("direction")),interface)
    else:
        prova.avvia_rullo_sett(float(request.args.get("speed")),int(request.args.get("dist")),int(request.args.get("direction")),interface)
    return "comando inviato"

# route per far partire il rullo, ma non è presente a Frigento
@app.route('/stoprullo', methods=['GET'])
def stoprullo():
    prova.ferma_rullo()
    return "comando inviato"

# route per chiudere la chela 
@app.route('/chiudi_chela', methods=['GET'])
def chiudi_chela():
    prova.chiudi_chela()
    return "comando inviato"

# route per aprire la chela
@app.route('/apri_chela', methods=['GET'])
def apri_chela():
    prova.apri_chela()
    return "comando inviato"

# route per lo stop forzato del dobot, dopo questo comando dovrebbe bastare lanciare la route / per riavviare il dobot. Se non funziona bisogna riavviare il dobot
@app.route('/stop', methods=['GET'])
def stop():
    prova.stopping()
    return "comando inviato"   

if __name__ == "__main__":
    app.run(debug = False,port=5000,host="192.168.0.195")