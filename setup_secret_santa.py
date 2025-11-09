import csv, json, random, secrets, string
from pathlib import Path

# Dossier où sera stocké le fichier JSON
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Lecture du fichier CSV
def charger_participants(csv_path):
    noms, exclusions = [], {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nom = row["name"].strip()
            noms.append(nom)
            ex = (row.get("exclusions") or "").strip()
            exclusions[nom] = set(e.strip() for e in ex.split(";") if e.strip())
    return noms, exclusions

# Tirage au sort avec exclusions
def tirage_valide(noms, exclusions):
    for _ in range(5000):
        receveurs = noms[:]
        random.shuffle(receveurs)
        ok = True
        for donneur, receveur in zip(noms, receveurs):
            if donneur == receveur or receveur in exclusions.get(donneur, set()):
                ok = False
                break
        if ok:
            return dict(zip(noms, receveurs))
    raise RuntimeError("Impossible de trouver un tirage valide. Vérifie les exclusions.")

# Génération d’un mot de passe aléatoire
def mot_de_passe(longueur=4):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(longueur))

# Fonction principale
def main(csv_path="participants.csv"):
    noms, exclusions = charger_participants(csv_path)
    assignations = tirage_valide(noms, exclusions)
    data = {
        nom: {"receiver": assignations[nom], "password": mot_de_passe(4)}
        for nom in noms
    }
    (DATA_DIR / "assignments.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print("✅ Fichier data/assignments.json créé")
    print("🔐 Mots de passe à distribuer :")
    for nom in noms:
        print(f"- {nom} : {data[nom]['password']}")

if __name__ == "__main__":
    main()
