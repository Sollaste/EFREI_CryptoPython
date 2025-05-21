from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, request
from urllib.parse import unquote

app = Flask(__name__)

# Génération d'une clé au lancement (non persistée, donc encrypt/decrypt doivent être dans une même session)
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()
    token = f.encrypt(valeur_bytes)
    return f"Valeur encryptée : {token.decode()}"

@app.route('/decrypt/<path:valeur>')  # Utilise <path:...> pour inclure les `/` éventuels
def decryptage(valeur):
    try:
        valeur = unquote(valeur)  # Décodage URL si besoin
        valeur_bytes = valeur.encode()
        token = f.decrypt(valeur_bytes)
        return f"Valeur decryptée : {token.decode()}"
    except InvalidToken:
        return "Erreur : Token invalide ou corrompu", 400
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
