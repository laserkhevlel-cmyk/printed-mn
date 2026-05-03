import sys, base64, re, os
sys.stdout.reconfigure(encoding='utf-8')

DEPLOY = "C:/Users/dashp/OneDrive/Desktop/website/deploy"
HTML   = "C:/Users/dashp/OneDrive/Desktop/website/opload/index.html"

def b64(filename):
    path = os.path.join(DEPLOY, filename)
    if not os.path.exists(path):
        print(f"  WARNING: {filename} not found, skipping")
        return None
    ext = filename.rsplit('.', 1)[-1].lower()
    mime = 'image/webp' if ext == 'webp' else 'image/jpeg' if ext in ('jpg','jpeg') else 'image/png'
    with open(path, 'rb') as f:
        return f'data:{mime};base64,{base64.b64encode(f.read()).decode()}'

# ── Single-image products ──────────────────────────────────────────────────────
SINGLE = {
    'bottle300':     'bottle300.jpg',
    'bottle580':     'bottle580.jpg',
    'cable-tag':     'Photoroom_20260501_005959.jpg',
    'coffee-cup':    'coffee-cup.jpg',
    'notebook':      'notebook.jpg',
    'notebook2':     'notebook2.jpg',
    'notebook3':     'notebook3.jpg',
    'paper-bag':     'paper-bag.jpg',
    'pen-luxury':    'pen-luxury.jpg',
    'pen-slim':      'pen-slim.jpg',
    'stanley':       'stanley.jpg',
    'tor-bag':       'tor-bag.jpg',
    'vacuum-bottle': 'vacuum-bottle.jpg',
}

# ── Multi-image products ───────────────────────────────────────────────────────
MULTI = {
    'medallion': [
        'Photoroom_20260430_211629.jpg',
        'Photoroom_20260430_213655.jpg',
        'Photoroom_20260430_213901.jpg',
        'Photoroom_20260501_004546.jpg',
    ],
    'dogtag': [
        'dogtag1.jpg',
        'dogtag2.jpg',
        'dogtag3.jpg',
    ],
}

with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

def find_gallery_bounds(content, pid):
    """Find start and end of gallery div inside product section."""
    sec_idx = content.find(f'id="{pid}"')
    if sec_idx == -1:
        return None, None
    # Find gallery div after section start
    g_idx = content.find('<div class="gallery', sec_idx)
    if g_idx == -1:
        return None, None
    # Find matching closing </div> by counting depth
    pos = g_idx
    depth = 0
    while pos < len(content):
        open_tag = content.find('<div', pos)
        close_tag = content.find('</div>', pos)
        if open_tag == -1: open_tag = len(content)
        if close_tag == -1: close_tag = len(content)
        if open_tag < close_tag:
            depth += 1
            pos = open_tag + 4
        else:
            depth -= 1
            pos = close_tag + 6
            if depth == 0:
                return g_idx, pos
    return None, None

def single_gallery(src):
    return (f'<div class="gallery gallery-one">\n'
            f'        <div class="gallery-img"><img src="{src}" style="width:100%;height:100%;object-fit:contain;padding:8px"></div>\n'
            f'      </div>')

def multi_gallery(srcs):
    cols = '1fr 1fr' if len(srcs) == 2 else '1fr 1fr'
    imgs = '\n        '.join(
        f'<div class="gallery-img"><img src="{s}" style="width:100%;height:100%;object-fit:contain;padding:8px"></div>'
        for s in srcs
    )
    return (f'<div class="gallery" style="display:grid;grid-template-columns:{cols};gap:10px">\n'
            f'        {imgs}\n'
            f'      </div>')

# ── Replace single-image products ─────────────────────────────────────────────
for pid, fname in SINGLE.items():
    src = b64(fname)
    if src is None: continue
    g_start, g_end = find_gallery_bounds(content, pid)
    if g_start is None:
        print(f"  {pid}: gallery NOT FOUND")
        continue
    new_gallery = single_gallery(src)
    content = content[:g_start] + new_gallery + content[g_end:]
    print(f"  {pid}: replaced ✓")

# ── Replace multi-image products ──────────────────────────────────────────────
for pid, fnames in MULTI.items():
    srcs = [b64(f) for f in fnames]
    srcs = [s for s in srcs if s is not None]
    if not srcs: continue
    g_start, g_end = find_gallery_bounds(content, pid)
    if g_start is None:
        print(f"  {pid}: gallery NOT FOUND")
        continue
    new_gallery = multi_gallery(srcs)
    content = content[:g_start] + new_gallery + content[g_end:]
    print(f"  {pid}: {len(srcs)} images replaced ✓")

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll done!")
