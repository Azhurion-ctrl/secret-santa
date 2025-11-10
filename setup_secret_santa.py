print("🚀 Script setup_secret_santa.py lancé")

import csv, json, random, string, sys, os

def read_participants(path):
    with open(path, encoding="utf-8") as f:
        return [
            {
                "name": row["name"].strip(),
                "exclude": [e.strip() for e in row["exclude"].split(",") if e.strip()]
            }
            for row in csv.DictReader(f)
            if row["name"].strip()
        ]

def validate(participants):
    names = [p["name"] for p in participants]
    if len(names) < 2 or len(set(names)) != len(names):
        sys.exit("❌ Liste invalide : doublons ou trop peu de noms.")

def assign_targets(participants):
    names = [p["name"] for p in participants]
    for _ in range(1000):  # Tentatives pour éviter boucle infinie
        targets = names.copy()
        random.shuffle(targets)
        result = {}
        used = set()

        valid = True
        for p in participants:
            for t in targets:
                if (
                    t != p["name"]
                    and t not in p["exclude"]
                    and t not in used
                ):
                    result[p["name"]] = t
                    used.add(t)
                    break
            else:
                valid = False
                break

        if valid:
            return result

    sys.exit("❌ Attribution impossible avec les exclusions.")

def generate_password():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

def save(assignments, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(assignments, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    participants = read_participants("participants.csv")
    validate(participants)
    targets = assign_targets(participants)
    assignments = {
        p["name"]: {"password": generate_password(), "target": targets[p["name"]]}
        for p in participants
    }
    print(assignments)
    save(assignments, "data/assignments.json")
    print("✅ assignments.json généré avec succès !")
