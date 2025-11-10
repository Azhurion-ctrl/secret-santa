from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

with open("data/assignments.json", encoding="utf-8") as f:
    ASSIGNMENTS = json.load(f)

@app.route("/form.html")
def form():
    user = request.args.get("user")
    return render_template("form.html", user=user)

@app.route("/", methods=["POST"])
def result():
    name = request.form.get("name")
    password = request.form.get("password")
    entry = ASSIGNMENTS.get(name)

    if entry and entry.get("password") == password:
        return render_template("result.html", name=name, target=entry["target"])
    return "<h1>⛔ Accès refusé</h1><p>Prénom ou mot de passe incorrect.</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

