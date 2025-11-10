print("🚀 Script setup_secret_santa.py lancé")

import csv, json, random, string, sys, os
from pathlib import Path
import qrcode

# 📁 Chemins
PARTICIPANTS_PATH = Path("participants.csv")
ASSIGNMENTS_PATH = Path("data/assignments.json")
QR_DIR = Path("cartes")
QR_DIR.mkdir(exist_ok=True)
BASE_URL = "https://secret-santa-y4uc.onrender.com/form.html?user="

# 📄 Lecture des participants avec exclusions
def read_participants(path):
    with open(path, encoding="utf-8") as f:
        return [
            {
                "name": row["name"].strip(),
                "exclude": [e.strip() for e in row["exclude"].split(",") if e.strip()]
            }
            for row in csv.DictReader(f, delimiter=",")
            if row["name"].strip()
        ]

# ✅ Validation de la liste
def validate(participants):
    names = [p["name"] for p in participants]
    if len(names) < 2 or len(set(names)) != len(names):
        sys.exit("❌ Liste invalide : doublons ou trop peu de noms.")

# 🎯 Attribution des cibles en respectant les exclusions
def assign_targets(participants):
    names = [p["name"] for p in participants]
    for _ in range(1000):
        targets = names.copy()
        random.shuffle(targets)
        result = {}
        used = set()
        valid = True

        for p in participants:
            for t in targets:
                if t != p["name"] and t not in p["exclude"] and t not in used:
                    result[p["name"]] = t
                    used.add(t)
                    break
            else:
                valid = False
                break

        if valid:
            return result

    sys.exit("❌ Attribution impossible avec les exclusions.")

# 🔐 Génération de mot de passe
def generate_password():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

# 💾 Sauvegarde JSON
def save(assignments, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(assignments, f, indent=2, ensure_ascii=False)

# 📱 Génération des QR codes manquants
def generate_qrcodes(assignments):
    for name in assignments:
        qr_path = QR_DIR / f"{name}_qr.png"
        if not qr_path.exists():
            qrcode.make(f"{BASE_URL}{name}").save(qr_path)
            print(f"🆕 QR code généré pour {name}")
        else:
            print(f"✅ QR code déjà présent pour {name}")

# 🚀 Exécution principale
if __name__ == "__main__":
    participants = read_participants(PARTICIPANTS_PATH)
    validate(participants)
    targets = assign_targets(participants)
    assignments = {
        p["name"]: {
            "password": generate_password(),
            "target": targets[p["name"]]
        }
        for p in participants
    }
    print(assignments)
    save(assignments, ASSIGNMENTS_PATH)
    print("✅ assignments.json généré avec succès !")

    generate_qrcodes(assignments)
    print("🎉 QR codes mis à jour dans le dossier cartes/")
