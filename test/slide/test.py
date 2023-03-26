import ddddocrgpu.ddddocrgpu

det = ddddocrgpu.ddddocrgpu.DdddOcr(det=False, ocr=False, show_ad=False)
res = det.slide_match(open('tile.png', 'rb').read(), open('bg.png', 'rb').read(), simple_target=True)
print(res)
