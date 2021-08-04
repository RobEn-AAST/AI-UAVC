import qrcode
counter = 0

for i in range(150):
    img = qrcode.make(f"test code {counter}")
    img.save(f"img{counter}.jpg")
    counter+=1
print("done")
