import qrcode

url = "https://secret-santa-1-zf2s.onrender.com"
img = qrcode.make(url)
img.save("qr_secret_santa.png")
print("✅ QR code généré : qr_secret_santa.png")
