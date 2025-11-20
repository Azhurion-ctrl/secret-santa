from fpdf import FPDF
import json
from pathlib import Path
from fpdf.enums import XPos, YPos

# 📁 Fichiers
DATA_PATH = Path("data/assignments.json")
OUTPUT_DIR = Path("cartes")
FONT_CINZEL = Path("fonts/Cinzel-Regular.ttf")        # Police magique
FONT_MANUSCRIT = Path("fonts/Manuscrit.ttf")          # Police manuscrite (ex: GreatVibes renommée en Manuscrit.ttf)
PARCHMENT_IMG = Path("static/parchment.jpg")          # Fond parchemin
OUTPUT_DIR.mkdir(exist_ok=True)

class CartePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L", format="A4")
        self.set_auto_page_break(auto=False)
        # Polices
        self.add_font("Cinzel", "", str(FONT_CINZEL))
        self.add_font("Manuscrit", "", str(FONT_MANUSCRIT))
        self.set_font("Cinzel", "", 11)

    def ajouter_carte(self, nom, mdp, qr_path, x, y):
        # 🎨 Fond parchemin
        if PARCHMENT_IMG.exists():
            self.image(str(PARCHMENT_IMG), x=x, y=y, w=135, h=90)
        else:
            self.set_fill_color(244, 233, 211)
            self.set_draw_color(176, 141, 87)
            self.set_line_width(1.5)
            self.rect(x, y, 135, 90, style='FD')

        # ✨ Titre magique
        self.set_xy(x + 15, y + 8)
        self.set_font("Cinzel", "", 16)
        self.set_text_color(43, 42, 40)  # noir/brun
        self.cell(70, 10, "✨ Quête Secret Santa ✨", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 🔮 QR code en haut à droite
        if qr_path.exists():
            self.image(str(qr_path), x=x + 95, y=y + 8, w=30)

        # 🧙 Identité manuscrite dorée avec ombre
        self.set_font("Manuscrit", "", 20)

        # Ombre pour le nom
        self.set_text_color(43, 42, 40)  # brun foncé
        self.set_xy(x + 15.5, y + 30.5)
        self.cell(70, 10, f"Sorcier : {nom}")

        # Texte doré par-dessus
        self.set_text_color(184, 134, 11)  # doré foncé
        self.set_xy(x + 15, y + 30)
        self.cell(70, 10, f"Sorcier : {nom}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Ombre pour le code secret
        self.set_font("Cinzel", "", 18)
        self.set_text_color(43, 42, 40)
        self.set_xy(x + 15.5, y + 45.5)
        self.cell(70, 10, f"Code secret : {mdp}")

        # Texte doré par-dessus
        self.set_text_color(184, 134, 11)
        self.set_xy(x + 15, y + 45)
        self.cell(70, 10, f"Code secret : {mdp}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 📜 Mission (texte classique)
        self.set_text_color(43, 42, 40)  # retour noir/brun
        self.set_xy(x + 15, y + 60)
        self.set_font("Cinzel", "", 11)
        self.multi_cell(110, 6,
            "Par décret du Ministère de la Magie,\n"
            "Votre mission est d’offrir un présent enchanté à la personne mystère révélée."
        )

        # 🪄 Message final
        self.set_xy(x + 15, y + 82)
        self.set_font("Cinzel", "", 9)
        self.cell(70, 5, "Scanne ton sceau magique pour révéler ta cible ✨", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# 🔄 Lecture des données
data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
pdf = CartePDF()

positions = [(10, 10), (155, 10), (10, 110), (155, 110)]
noms = list(data.keys())

for i in range(0, len(noms), 4):
    pdf.add_page()
    for j in range(4):
        if i + j < len(noms):
            nom = noms[i + j]
            mdp = data[nom]["password"]
            qr_path = OUTPUT_DIR / f"{nom}_qr.png"
            x, y = positions[j]
            pdf.ajouter_carte(nom, mdp, qr_path, x, y)

pdf.output(str(OUTPUT_DIR / "SecretSanta_HP_Parchemin.pdf"))
print("✅ PDF magique généré avec fond parchemin, écriture manuscrite dorée + ombre, QR en haut à droite")
