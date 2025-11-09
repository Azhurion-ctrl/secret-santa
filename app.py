from flask import Flask, request, render_template, redirect
import json
import csv
from pathlib import Path
import setup_secret_santa  # ton script de génération
import os

app = Flask(__name__)

# Fichiers de données
DATA = Path("data") / "assignments.json"
CSV_PATH = Path("participants.csv")

# 🔄 Fonctions utilitaires
def charger_data():
    return json.loads(DATA.read_text(encoding="utf-8"))

def lire_participants():
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def ecrire_participants(lignes):
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "exclusions"])
        writer.writeheader()
        writer.writerows(lignes)

# 🎁 Page principale : formulaire de révélation
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

# 🔧 Interface admin pour modifier les exclusions
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        noms = request.form.getlist("name")
        exclusions = request.form.getlist("exclusions")
        lignes = [{"name": n.strip(), "exclusions": e.strip()} for n, e in zip(noms, exclusions)]
        ecrire_participants(lignes)
        setup_secret_santa.main()  # régénère assignments.json
        return redirect("/admin")
    participants = lire_participants()
    return render_template("admin.html", participants=participants)

# 🚀 Lancement de l'app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
