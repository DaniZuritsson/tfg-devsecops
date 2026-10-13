# app.py - demo VULNERABLE a proposito - TFG Zurita, Daniel
from flask import Flask, request
import sqlite3
app = Flask(__name__)

@app.route("/user")
def user():
    uid = request.args.get("id")
    con = sqlite3.connect("app.db")
    # VULN 1 (OWASP A03 Inyeccion): concatenacion directa -> SQLi
    row = con.execute("SELECT name FROM users WHERE id = " + uid).fetchone()
    # VULN 2 (OWASP A03 XSS): devuelve entrada sin escapar
    return f"<h1>Hola {row[0]}</h1> buscado: {request.args.get('id')}"

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["f"]
    # VULN 3 (OWASP A04/A08): guarda cualquier fichero sin validar tipo
    f.save("/var/www/uploads/" + f.filename)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
