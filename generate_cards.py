from fpdf import FPDF
import json
from pathlib import Path
from fpdf.enums import XPos, YPos

# 📁 Fichiers
DATA_PATH = Path("data/assignments.json")
OUTPUT_DIR = Path("cartes")
FONT_PATH = Path("fonts/NotoSans-Regular.ttf")
EMOJI_DIR = Path("emojis")
OUTPUT_DIR.mkdir(exist_ok=True)

class CartePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L", format="A4")
        self.set_auto_page_break(auto=False)
        self.add_font("Noto", "", str(FONT_PATH))
        self.set_font("Noto", "", 11)

    def ajouter_carte(self, nom, mdp, qr_path, x, y):
        # 🎁 Fond de carte
        self.set_fill_color(255, 250, 240)
        self.set_draw_color(200, 0, 0)
        self.set_line_width(1)
        self.rect(x, y, 135, 90, style='FD')

        # 🎅 Titre
        self.image(str(EMOJI_DIR / "santa.png"), x=x + 5, y=y + 5, w=10)
        self.set_xy(x + 20, y + 5)
        self.set_font("Noto", "", 16)
        self.cell(100, 10, "🎅 Mission Secret Santa", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 🔐 Identité
        self.image(str(EMOJI_DIR / "lock.png"), x=x + 5, y=y + 20, w=8)
        self.set_xy(x + 15, y + 20)
        self.set_font("Noto", "", 12)
        self.cell(120, 8, f"Nom : {nom}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_xy(x + 15, y + 28)
        self.cell(120, 8, f"Code secret : {mdp}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # 🕵️‍♂️ Mission
        self.image(str(EMOJI_DIR / "detective.png"), x=x + 5, y=y + 40, w=8)
        self.set_xy(x + 15, y + 40)
        self.set_font("Noto", "", 11)
        self.multi_cell(110, 6, "Votre mission, si vous l’acceptez, est d’offrir un cadeau à la personne mystère révélée.")

        # 📱 QR Code
        self.image(str(qr_path), x=x + 85, y=y + 50, w=30)

        # 🎁 Message final
        self.image(str(EMOJI_DIR / "secret.png"), x=x + 5, y=y + 80, w=8)
        self.set_xy(x + 15, y + 80)
        self.set_font("Noto", "", 9)
        self.cell(120, 5, "Scanne ton QR code pour découvrir ta cible 🎁", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
            if qr_path.exists():
                x, y = positions[j]
                pdf.ajouter_carte(nom, mdp, qr_path, x, y)
            else:
                print(f"⚠️ QR code manquant pour {nom} : {qr_path.name}")

pdf.output(str(OUTPUT_DIR / "SecretSanta_Cartes_4parPage_Paysage_Final.pdf"))
print("✅ PDF final amélioré généré avec QR codes existants et mise en page festive")
