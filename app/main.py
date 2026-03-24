import logging
import os
import random
import traceback
from datetime import datetime

from flask import Flask, jsonify

# Correction de l'import de version
try:
    from version import __version__
    VERSION = __version__
except ImportError:
    VERSION = os.environ.get("APP_VERSION", "unknown")

# Configuration du logging structuré 
logging.basicConfig( 
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s", 
) 
logger = logging.getLogger(__name__) 

app = Flask(__name__) 

@app.route("/") 
def hello(): 
    logger.info("Route / appelée") 
    return jsonify({ 
        "message": "Hello, DevOps!", 
        "version": VERSION, 
        "timestamp": datetime.utcnow().isoformat(), 
    }) 

@app.route("/health") 
def health(): 
    """Endpoint de health check -- toujours disponible.""" 
    return jsonify({"status": "ok", "version": VERSION}) 

@app.route("/compute") 
def compute(): 
    """ 
    Simule un calcul. 
    Désormais stable (bug corrigé). 
    """ 
    logger.info("Route /compute appelée") 

    # On garde la structure mais on appelle la fonction corrigée
    roll = random.random() 
    if roll < 0.3: 
        logger.info("Exécution du calcul alternatif -- roll=%.3f", roll) 
        result = _buggy_computation() 
        return jsonify({"result": result}) 

    value = random.randint(1, 100) 
    logger.info("Calcul réussi : valeur=%d", value) 
    return jsonify({ 
        "result": value * 2, 
        "input": value, 
    }) 

def _buggy_computation(): 
    """Fonction corrigée : ne plante plus.""" 
    # Correction : data n'est plus None
    data = {"value": random.randint(1, 50)} 
    return data["value"] 

@app.route("/slow") 
def slow(): 
    """Simule un endpoint lent.""" 
    import time 
    delay = random.uniform(1, 4) 
    logger.info("Route /slow appelée -- délai=%.2fs", delay) 
    time.sleep(delay) 
    return jsonify({"message": "Réponse lente", "delay_seconds": round(delay, 2)}) 

@app.errorhandler(500) 
def handle_500(e): 
    logger.error("Erreur 500 : %s\n%s", str(e), traceback.format_exc()) 
    return jsonify({ 
        "error": "Erreur interne du serveur", 
        "detail": str(e), 
    }), 500 

if __name__ == "__main__": 
    app.run( 
        debug=False, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 8080)), 
    )