import ddddocrgpu.ddddocrgpu
from PIL import Image

det = ddddocrgpu.ddddocrgpu.DdddOcr(det=False, ocr=False, show_ad=False)
res = det.slide_match(open('tile.png', 'rb').read(), open('bg.png', 'rb').read(), simple_target=True)
print(res)
x1, y1, x2, y2 = res["target"]
im = Image.open("bg.png")
im2 = Image.open("tile.png")
im.paste(im2, (x1, y1), im2)
im.save("result.png")
