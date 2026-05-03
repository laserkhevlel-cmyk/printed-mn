"""
Generate Android app icons and splash screens from logo_transparent.png
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw

LOGO_PATH   = "C:/Users/dashp/OneDrive/Desktop/website/opload/logo_transparent.png"
ANDROID_RES = "C:/Users/dashp/OneDrive/Desktop/website/opload/android/app/src/main/res"

BG_COLOR  = (30, 27, 75)   # #1e1b4b  dark navy/purple
BG_DARK   = (15, 23, 42)   # #0f172a  very dark for splash

# ─── Icon sizes (regular + round + foreground) ────────────────────────────────
ICON_SIZES = {
    'mipmap-mdpi':    48,
    'mipmap-hdpi':    72,
    'mipmap-xhdpi':   96,
    'mipmap-xxhdpi':  144,
    'mipmap-xxxhdpi': 192,
}
FG_SIZES = {
    'mipmap-mdpi':    108,
    'mipmap-hdpi':    162,
    'mipmap-xhdpi':   216,
    'mipmap-xxhdpi':  324,
    'mipmap-xxxhdpi': 432,
}

# ─── Splash screen sizes ───────────────────────────────────────────────────────
SPLASH_SIZES = {
    'drawable-port-mdpi':    (320, 480),
    'drawable-port-hdpi':    (480, 800),
    'drawable-port-xhdpi':   (720, 1280),
    'drawable-port-xxhdpi':  (960, 1600),
    'drawable-port-xxxhdpi': (1280, 1920),
    'drawable-land-mdpi':    (480, 320),
    'drawable-land-hdpi':    (800, 480),
    'drawable-land-xhdpi':   (1280, 720),
    'drawable-land-xxhdpi':  (1600, 960),
    'drawable-land-xxxhdpi': (1920, 1280),
}

logo = Image.open(LOGO_PATH).convert('RGBA')

def make_icon(size, bg=(255,255,255)):
    """Logo on colored square background with padding."""
    canvas = Image.new('RGBA', (size, size), bg + (255,))
    pad = int(size * 0.15)
    max_logo = size - pad * 2
    ratio = min(max_logo / logo.width, max_logo / logo.height)
    lw, lh = int(logo.width * ratio), int(logo.height * ratio)
    resized = logo.resize((lw, lh), Image.LANCZOS)
    x = (size - lw) // 2
    y = (size - lh) // 2
    canvas.paste(resized, (x, y), resized)
    return canvas.convert('RGB')

def make_round_icon(size, bg=(255,255,255)):
    """Round icon with logo."""
    sq = make_icon(size, bg)
    sq = sq.convert('RGBA')
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, size, size], fill=255)
    result = Image.new('RGBA', (size, size), (0,0,0,0))
    result.paste(sq, mask=mask)
    return result

def make_foreground(size):
    """Transparent foreground with logo + extra padding for adaptive icon."""
    canvas = Image.new('RGBA', (size, size), (0,0,0,0))
    # safe zone is 72/108 of total, we use 60% to be safe
    max_logo = int(size * 0.60)
    ratio = min(max_logo / logo.width, max_logo / logo.height)
    lw, lh = int(logo.width * ratio), int(logo.height * ratio)
    resized = logo.resize((lw, lh), Image.LANCZOS)
    x = (size - lw) // 2
    y = (size - lh) // 2
    canvas.paste(resized, (x, y), resized)
    return canvas

def make_splash(w, h):
    """Logo centered on dark branded background."""
    canvas = Image.new('RGBA', (w, h), BG_DARK + (255,))
    max_w = int(w * 0.60)
    max_h = int(h * 0.35)
    ratio = min(max_w / logo.width, max_h / logo.height)
    lw, lh = int(logo.width * ratio), int(logo.height * ratio)
    resized = logo.resize((lw, lh), Image.LANCZOS)
    x = (w - lw) // 2
    y = (h - lh) // 2
    canvas.paste(resized, (x, y), resized)
    return canvas.convert('RGB')

# ── Generate icons ──
print("Generating icons...")
for folder, size in ICON_SIZES.items():
    path = os.path.join(ANDROID_RES, folder)
    make_icon(size, BG_COLOR).save(os.path.join(path, 'ic_launcher.png'))
    rnd = make_round_icon(size, BG_COLOR)
    rnd.convert('RGB').save(os.path.join(path, 'ic_launcher_round.png'))
    print(f"  {folder}: {size}x{size} ✓")

# ── Generate foreground (adaptive) ──
print("Generating adaptive icon foreground...")
for folder, size in FG_SIZES.items():
    path = os.path.join(ANDROID_RES, folder)
    fg_path = os.path.join(path, 'ic_launcher_foreground.png')
    if os.path.exists(path):
        make_foreground(size).save(fg_path)
        print(f"  {folder}: {size}x{size} foreground ✓")

# ── Update adaptive icon background color to brand color ──
bg_xml_path = os.path.join(ANDROID_RES, 'values', 'ic_launcher_background.xml')
with open(bg_xml_path, 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#1e1b4b</color>\n</resources>\n')
print("Adaptive icon background color → #1e1b4b ✓")

# ── Generate splash screens ──
print("Generating splash screens...")
for folder, (w, h) in SPLASH_SIZES.items():
    path = os.path.join(ANDROID_RES, folder, 'splash.png')
    if os.path.exists(os.path.dirname(path)):
        make_splash(w, h).save(path)
        print(f"  {folder}: {w}x{h} ✓")

# ── Also update the base drawable/splash.png ──
make_splash(480, 800).save(os.path.join(ANDROID_RES, 'drawable', 'splash.png'))
print("  drawable/splash.png ✓")

print("\nAll done! ✓")
