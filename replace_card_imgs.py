import sys, base64, re, os
sys.stdout.reconfigure(encoding='utf-8')

DEPLOY = "C:/Users/dashp/OneDrive/Desktop/website/deploy"
HTML   = "C:/Users/dashp/OneDrive/Desktop/website/opload/index.html"

def b64src(filename):
    path = os.path.join(DEPLOY, filename)
    if not os.path.exists(path):
        return None
    ext = filename.rsplit('.', 1)[-1].lower()
    mime = 'image/webp' if ext == 'webp' else 'image/jpeg' if ext in ('jpg','jpeg') else 'image/png'
    with open(path, 'rb') as f:
        return f'data:{mime};base64,{base64.b64encode(f.read()).decode()}'

# Card thumbnail: product_id → image file (first image if multi)
CARD_IMGS = {
    'medallion':     'Photoroom_20260501_004546.jpg',
    'bottle580':     'bottle580.jpg',
    'bottle300':     'bottle300.jpg',
    'notebook':      'notebook.jpg',
    'pen-luxury':    'pen-luxury.jpg',
    'pen-slim':      'pen-slim.jpg',
    'cable-tag':     'Photoroom_20260501_005959.jpg',
    'stanley':       'stanley.jpg',
    'notebook2':     'notebook2.jpg',
    'notebook3':     'notebook3.jpg',
    'coffee-cup':    'coffee-cup.jpg',
    'keychain-opener':'keychain.jpg',
    'vacuum-bottle': 'vacuum-bottle.jpg',
    'dogtag':        'dogtag1.jpg',
    'paper-bag':     'paper-bag.jpg',
    'tor-bag':       'tor-bag.jpg',
}

with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

for pid, fname in CARD_IMGS.items():
    src = b64src(fname)
    if src is None:
        print(f"  {pid}: file not found, skip")
        continue

    # Find the card anchor for this product
    card_idx = content.find(f'href="#{pid}" class="card"')
    if card_idx == -1:
        print(f"  {pid}: card not found")
        continue

    # Find card-img div and its img src
    card_img_idx = content.find('<div class="card-img">', card_idx)
    if card_img_idx == -1:
        print(f"  {pid}: card-img not found")
        continue

    # Find the img src= within card-img (within next 200 chars to stay in scope)
    src_start = content.find('src="', card_img_idx, card_img_idx + 300)
    if src_start == -1:
        print(f"  {pid}: img src not found")
        continue

    src_start += 5  # skip 'src="'
    src_end = content.find('"', src_start)

    content = content[:src_start] + src + content[src_end:]
    print(f"  {pid}: card thumbnail replaced ✓")

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone!")
