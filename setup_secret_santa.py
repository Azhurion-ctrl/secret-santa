print("🚀 Script setup_secret_santa.py lancé")

import csv, json, random, string, sys, os

def read_participants(path):
    with open(path, encoding="utf-8") as f:
        return [row["name"].strip() for row in csv.DictReader(f) if row["name"].strip()]

def validate(names):
    if len(names) < 2 or len(set(names)) != len(names):
        sys.exit("❌ Liste invalide : doublons ou trop peu de noms.")

def assign_targets(names):
    for _ in range(100):
        targets = names.copy()
        random.shuffle(targets)
        if all(n != t for n, t in zip(names, targets)):
            return targets
    sys.exit("❌ Attribution impossible sans auto-cible.")

def generate_password():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

def save(assignments, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(assignments, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    names = read_participants("participants.csv")
    validate(names)
    targets = assign_targets(names)
    assignments = {
        name: {"password": generate_password(), "target": target}
        for name, target in zip(names, targets)
    }
    print(assignments)
    save(assignments, "data/assignments.json")
    print("✅ assignments.json généré avec succès !")

