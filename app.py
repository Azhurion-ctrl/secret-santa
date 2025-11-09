from flask import Flask, request, render_template
import json
from pathlib import Path

app = Flask(__name__)
DATA = Path("data") / "assignments.json"

def charger_data():
    return json.loads(DATA.read_text(encoding="utf-8"))

@app.route("/", methods=["GET", "POST"])
def reveal():
    if request.method == "POST":
        nom = (request.form.get("name") or "").strip()
        mdp = (request.form.get("password") or "").strip().upper()
        data = charger_data()
        info = data.get(nom)
        if not info:
            return render_template("result.html", error="Nom inconnu.")
        if mdp != info["password"]:
            return render_template("result.html", error="Mot de passe incorrect.")
        return render_template("result.html", giver=nom, receiver=info["receiver"])
    return render_template("form.html")

if __name__ == "__main__":
   import os
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
