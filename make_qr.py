import qrcode

url = "https://secret-santa-y4uc.onrender.com"
img = qrcode.make(url)
img.save("qr_secret_santa.png")
print("✅ QR code généré : qr_secret_santa.png")
