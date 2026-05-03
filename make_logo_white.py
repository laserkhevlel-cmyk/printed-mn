import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

src = "C:/Users/dashp/OneDrive/Desktop/website/opload/logo.png"
out = "C:/Users/dashp/OneDrive/Desktop/website/opload/logo_white.png"

img = Image.open(src).convert("RGBA")
pixels = img.load()
w, h = img.size

for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        # Black background blob → transparent
        if r < 60 and g < 60 and b < 60:
            pixels[x, y] = (0, 0, 0, 0)
        else:
            # All other visible pixels → white
            pixels[x, y] = (255, 255, 255, 255)

img.save(out)
print(f"Saved: {out}  ({w}x{h})")
