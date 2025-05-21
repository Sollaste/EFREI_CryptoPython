import os
from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, request
from urllib.parse import unquote

app = Flask(__name__)

# Charger la clé depuis la variable d'environnement
fernet_key = os.environ.get("FERNET_KEY")

if not fernet_key:
    raise ValueError("Clé Fernet manquante. Définis FERNET_KEY dans tes variables d'environnement.")

f = Fernet(fernet_key.encode())

@app.route('/')
def hello_world():
    return "Hello, world!"

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"

@app.route('/decrypt/<path:valeur>')
def decryptage(valeur):
    try:
        valeur = unquote(valeur)
        valeur_bytes = valeur.encode()
        token = f.decrypt(valeur_bytes)
        return f"Valeur decryptée : {token.decode()}"
    except InvalidToken:
        return "Erreur : Token invalide", 400

                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
