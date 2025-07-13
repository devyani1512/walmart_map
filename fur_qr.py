import qrcode
qr = qrcode.make("http://127.0.0.1:5500")  # or your actual hosted URL
qr.save("store_qr.png")
