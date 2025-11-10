from flask import Flask, render_template, request
import json

app = Flask(__name__)

# 🔐 Chargement des affectations
with open("data/assignments.json", encoding="utf-8") as f:
    ASSIGNMENTS = json.load(f)

@app.route("/form.html")
def form():
    user = request.args.get("user")  # récupère ?user=Alice
    return render_template("form.html", user=user)

@app.route("/", methods=["POST"])
def result():
    name = request.form.get("name")
    password = request.form.get("password")

    if name in ASSIGNMENTS and ASSIGNMENTS[name]["password"] == password:
        target = ASSIGNMENTS[name]["target"]
        return f"""
        <h1>🎁 Bonjour {name} !</h1>
        <p>Ta cible est : <strong>{target}</strong></p>
        <p>Garde le secret jusqu’au jour J 🤫</p>
        """
    else:
        return """
        <h1>⛔ Accès refusé</h1>
        <p>Le prénom ou le code secret est incorrect.</p>
        <a href="/form.html">Réessayer</a>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
