import sys, base64
sys.stdout.reconfigure(encoding='utf-8')

DEPLOY = "C:/Users/dashp/OneDrive/Desktop/website/deploy"
HTML   = "C:/Users/dashp/OneDrive/Desktop/website/opload/index.html"

# Convert image to base64
with open(f"{DEPLOY}/card-holder.jpg", "rb") as f:
    img_src = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add to PRODUCTS_MAP ──
old_pm = "'name-necklace':  'Name necklace — нэрийн зүүлт',\n};"
new_pm = ("'name-necklace':  'Name necklace — нэрийн зүүлт',\n"
          "  'card-holder':    'Металл карт холдер',\n};")
if old_pm in content:
    content = content.replace(old_pm, new_pm)
    print("1. PRODUCTS_MAP updated ✓")
else:
    print("1. PRODUCTS_MAP NOT FOUND")

# ── 2. Add product card after name-necklace card ──
old_card_end = '</a>\n<div id="detail-screen">'
new_card = f'''<a href="#card-holder" class="card" data-category="other" data-ptype="laser">
      <div class="card-img"><img src="{img_src}" alt="Металл карт холдер"></div>
      <div class="card-body">
        <div class="card-name">Металл карт холдер</div>
        <div class="card-desc">Картны мэдээлэл гаднаас уншигдахгүй, лазер UV хэвлэлтэй гарын бэлэг.</div>
        <div class="card-footer"><span class="card-tag tag-blue">Лазер хэвлэл</span><span class="card-tag tag-purple">UV хэвлэл</span><span class="card-arrow">→</span></div>
      </div></a>
<div id="detail-screen">'''

if old_card_end in content:
    content = content.replace(old_card_end, new_card)
    print("2. Product card added ✓")
else:
    print("2. Card insert point NOT FOUND")

# ── 3. Add detail section before </div> that closes the product grid, before detail-screen ──
# Insert before last detail section closing + detail-screen
old_detail_anchor = '\n<div id="detail-screen"></div>'
new_detail = f'''
<div class="detail-section" id="card-holder">
  <div class="detail-inner">
    <div class="section-label" style="text-align:left;margin-bottom:1.5rem">✦ Металл карт холдер</div>
    <div class="detail-grid">
      <div class="gallery gallery-one">
        <div class="gallery-img"><img src="{img_src}" style="width:100%;height:100%;object-fit:contain;padding:8px"></div>
      </div>
      <div class="detail-content">
        <h2>Металл карт холдер</h2>
        <p>Холдерын гаднаас картны мэдээлэл уншигдахгүй. Лазер, UV хэвлэлтэй гарын бэлэгнд тохиромжтой.</p>
        <div class="specs-grid"><div class="spec-item"><div class="spec-label">Материал</div><div class="spec-val">Алюминий</div></div><div class="spec-item"><div class="spec-label">Өнгө</div><div class="spec-val">7 өнгийн сонголт</div></div><div class="spec-item"><div class="spec-label">Хэвлэлт</div><div class="spec-val">Лазер, UV</div></div><div class="spec-item"><div class="spec-label">Хэвлэл</div><div class="spec-val">Үнэгүй</div></div><div class="spec-item"><div class="spec-label">Утас</div><div class="spec-val">86681144</div></div><div class="spec-item"><div class="spec-label">Утас 2</div><div class="spec-val">85882030</div></div></div>
        <ul class="features"><li>Холдерын гаднаас картны мэдээлэл уншигдахгүй</li><li>Хэвлэлтэй гарын бэлэгнд тохиромжтой</li><li>7 өнгийн алюминий биет</li><li>Лазер болон UV хэвлэл боломжтой</li><li>Хэвлэл үнэгүй</li></ul>
        <div id="ds_card-holder" class="detail-stock-wrap"></div>
              <div id="dp_card-holder" class="detail-price-wrap"></div>
        <div class="order-btns-wrap"><button class="order-btn-online" onclick="openOrderModal(this)" data-product="Металл карт холдер" data-prints="Лазер хэвлэл|UV хэвлэл">📦 Онлайн захиалга</button><a href="https://www.facebook.com/profile.php?id=100063665375091" target="_blank" class="order-btn-fb">✦ Facebook</a></div>
      </div>
    </div>
  </div>
</div>

<div id="detail-screen"></div>'''

if '\n<div id="detail-screen"></div>' in content:
    content = content.replace('\n<div id="detail-screen"></div>', new_detail)
    print("3. Detail section added ✓")
else:
    print("3. detail-screen anchor NOT FOUND")

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone!")
