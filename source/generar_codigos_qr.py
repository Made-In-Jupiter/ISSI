import qrcode

# Generar 10 códigos QR con nombres de pieza_1 a pieza_10
for i in range(1, 11):
    data = f"pieza_{i}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(f"pieza_{i}_qr.png")
