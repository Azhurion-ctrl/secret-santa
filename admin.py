from flask import Flask, request, render_template, redirect
import csv
from pathlib import Path
import setup_secret_santa  # ton script existant

app = Flask(__name__)
CSV_PATH = Path("participants.csv")

def lire_participants():
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def ecrire_participants(lignes):
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "exclusions"])
        writer.writeheader()
        writer.writerows(lignes)

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

if __name__ == "__main__":
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
 
