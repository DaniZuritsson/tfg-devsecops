# app.py version CORREGIDA - TFG Daniel ZUrita
from flask import Flask, request
from markupsafe import escape
import sqlite3, os
app = Flask(__name__)

@app.route("/user")
def user():
    uid = request.args.get("id", "")
    # FIX 1 (SQLi): validacion de entrada
    if not uid.isdigit():
        return "parametro invalido", 400
    con = sqlite3.connect("app.db")
    # FIX 2 (SQLi): consulta parametrizada
    row = con.execute("SELECT name FROM users WHERE id = ?", (uid,)).fetchone()
    # FIX 3 (XSS): escape de la salida
    nombre = escape(row[0]) if row else "desconocido"
    return f"<h1>Hola {nombre}</h1>"

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["f"]
    # FIX 4 (subida insegura): lista blanca de extensiones + nombre seguro
    permitidas = {".png", ".jpg", ".pdf"}
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in permitidas:
        return "tipo de fichero no permitido", 400
    nombre_seguro = os.path.basename(f.filename)
    f.save(os.path.join("/var/www/uploads", nombre_seguro))
    return "ok"

if __name__ == "__main__":
    # FIX 5: no exponer en 0.0.0.0 en produccion
    app.run(host="127.0.0.1", port=5000)
