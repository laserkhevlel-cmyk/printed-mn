import sys, re
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

PRODUCTS = [
    'medallion','bottle580','bottle300','notebook','pen-luxury',
    'pen-slim','cable-tag','stanley','notebook2','notebook3',
    'coffee-cup','keychain-opener','keychain-plain','vacuum-bottle',
    'dogtag','paper-bag','tor-bag','name-necklace'
]

# ── 1. Add dp_ div after each ds_ div ──
inserted = 0
for pid in PRODUCTS:
    old = f'<div id="ds_{pid}" class="detail-stock-wrap"></div>'
    new = f'<div id="ds_{pid}" class="detail-stock-wrap"></div>\n              <div id="dp_{pid}" class="detail-price-wrap"></div>'
    if old in content and f'id="dp_{pid}"' not in content:
        content = content.replace(old, new)
        inserted += 1
        print(f"Added dp_{pid} ✓")
    elif f'id="dp_{pid}"' in content:
        print(f"dp_{pid} already exists")
    else:
        print(f"ds_{pid} NOT FOUND")

print(f"\nInserted: {inserted}")

# ── 2. Add CSS ──
css = """
.detail-price-wrap{margin-bottom:0.75rem}
.detail-price-table{display:flex;flex-direction:column;gap:4px;margin-top:4px}
.detail-price-row{display:flex;align-items:center;gap:10px;font-size:13px;padding:6px 12px;border-radius:8px;background:#f1f5f9}
.detail-price-row.active-tier{background:#ede9fe;font-weight:700;color:#6d28d9}
.detail-price-range{color:#64748b;min-width:110px}
.detail-price-row.active-tier .detail-price-range{color:#6d28d9}
.detail-price-amount{font-weight:700;color:#1e3a8a}
.detail-price-row.active-tier .detail-price-amount{color:#6d28d9}
.detail-price-label{font-size:12px;font-weight:700;color:#64748b;margin-bottom:2px}
"""
if '.detail-price-wrap' not in content:
    content = content.replace('</style>', css + '</style>', 1)
    print("CSS added ✓")

# ── 3. Add displayPriceTiers function before loadStockData() call ──
old_js = 'window.updateOrderPrice = () => {'
new_js = """window.displayPriceTiers = (qty) => {
  Object.keys(PRODUCTS_MAP).forEach(pid => {
    const el = document.getElementById('dp_' + pid);
    if(!el) return;
    const tiers = _priceMap[pid];
    if(!tiers || !tiers.length) { el.innerHTML = ''; return; }
    const rows = tiers.map(t => {
      const range = t.max === null ? t.min + '+' : t.min + '-' + t.max;
      const isActive = qty && qty >= t.min && (t.max === null || qty <= t.max);
      return '<div class="detail-price-row' + (isActive ? ' active-tier' : '') + '">'
        + '<span class="detail-price-range">&#x2022; ' + range + ' ширхэг</span>'
        + '<span class="detail-price-amount">' + t.price.toLocaleString() + '&#x20AE;/ш</span>'
        + (isActive ? '<span style="margin-left:auto;font-size:11px">&#x2190; таны захиалга</span>' : '')
        + '</div>';
    }).join('');
    el.innerHTML = '<div class="detail-price-label">&#x1F4B0; &#x422;&#x43E;&#x43E;&#x43D;&#x43E;&#x43E;&#x441; &#x445;&#x430;&#x43C;&#x430;&#x430;&#x440;&#x430;&#x445; &#x4AF;&#x43D;&#x44D;</div>'
      + '<div class="detail-price-table">' + rows + '</div>';
  });
};

window.updateOrderPrice = () => {"""

if old_js in content:
    content = content.replace(old_js, new_js)
    print("displayPriceTiers function added ✓")
else:
    print("updateOrderPrice NOT FOUND")

# ── 4. Call displayPriceTiers when prices load ──
old_load = """async function loadPriceData(){
  try{
    const snap=await getDocs(collection(db,'prices'));
    snap.forEach(d=>{_priceMap[d.id]=d.data().tiers||[];});
  }catch(e){console.log('price err',e.message);}
}"""
new_load = """async function loadPriceData(){
  try{
    const snap=await getDocs(collection(db,'prices'));
    snap.forEach(d=>{_priceMap[d.id]=d.data().tiers||[];});
    displayPriceTiers(null);
  }catch(e){console.log('price err',e.message);}
}"""
if old_load in content:
    content = content.replace(old_load, new_load)
    print("loadPriceData updated ✓")
else:
    print("loadPriceData NOT FOUND")

# ── 5. Update updateOrderPrice to highlight active tier on qty change ──
# Call displayPriceTiers with current qty when order modal qty changes
old_qty = "  info.style.display = 'block';\n  info.innerHTML = '💰 Нэгж үнэ: <b>' + tier.price.toLocaleString() + '₮</b> &nbsp;·&nbsp; Нийт: <b style=\"color:#15803d\">' + total.toLocaleString() + '₮</b>';"
new_qty = "  info.style.display = 'block';\n  info.innerHTML = '💰 Нэгж үнэ: <b>' + tier.price.toLocaleString() + '₮</b> &nbsp;·&nbsp; Нийт: <b style=\"color:#15803d\">' + total.toLocaleString() + '₮</b>';\n  displayPriceTiers(qty);"
if old_qty in content:
    content = content.replace(old_qty, new_qty)
    print("updateOrderPrice → displayPriceTiers call added ✓")
else:
    print("updateOrderPrice highlight NOT FOUND")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nAll done!")
