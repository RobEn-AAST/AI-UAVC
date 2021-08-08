import qrcode
counter = 0

for i in range(8):
    x = input()
    img = qrcode.make(f"{x}")
    img.save(f"{x}.png")

print('done')
