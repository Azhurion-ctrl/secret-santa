from fpdf import FPDF
import json
import qrcode
from pathlib import Path
from fpdf.enums import XPos, YPos

# 📁 Fichiers
DATA_PATH = Path("data/assignments.json")
OUTPUT_DIR = Path("cartes")
FONT_PATH = Path("fonts/NotoSans-Regular.ttf")
EMOJI_DIR = Path("emojis")
OUTPUT_DIR.mkdir(exist_ok=True)

# 🌐 URL avec prénom uniquement
BASE_URL = "https://secret-santa-y4uc.onrender.com/form.html?user="

class CartePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L", format="A4")
        self.set_auto_page_break(auto=False)
        self.add_font("Noto", "", str(FONT_PATH))
        self.set_font("Noto", "", 11)

    def ajouter_carte(self, nom, mdp, qr_path, x, y):
        self.set_xy(x, y)
        self.set_fill_color(255, 250, 240)
        self.rect(x, y, 135, 90, style='F')

        self.image(str(EMOJI_DIR / "santa.png"), x=x + 5, y=y + 5, w=8)
        self.set_xy(x + 15, y + 5)
        self.set_font("Noto", "", 14)
        self.cell(120, 8, "Mission Secret Santa", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.image(str(EMOJI_DIR / "lock.png"), x=x + 5, y=y + 20, w=8)
        self.set_xy(x + 15, y + 20)
        self.set_font("Noto", "", 11)
        self.cell(120, 6, f"Nom : {nom}   |   Code secret : {mdp}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.image(str(EMOJI_DIR / "detective.png"), x=x + 5, y=y + 30, w=8)
        self.set_xy(x + 15, y + 30)
        self.multi_cell(120, 6, "Votre mission, si vous l’acceptez…")

        self.image(str(qr_path), x=x + 95, y=y + 55, w=35)

        self.image(str(EMOJI_DIR / "secret.png"), x=x + 5, y=y + 80, w=8)
        self.set_xy(x + 15, y + 80)
        self.set_font("Noto", "", 9)
        self.cell(120, 5, "Scanne ton QR code le jour J 🎁", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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
            qrcode.make(f"{BASE_URL}{nom}").save(qr_path)
            x, y = positions[j]
            pdf.ajouter_carte(nom, mdp, qr_path, x, y)

pdf.output(str(OUTPUT_DIR / "SecretSanta_Cartes_4parPage_Paysage_Final.pdf"))
print("✅ PDF final généré avec prénom dans l’URL et mot de passe sur la carte")
