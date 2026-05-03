import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ── 1. Add ds_ div before each order-btns-wrap (line numbers, 1-based) ──
PRODUCTS = [
    (740,  'medallion'),
    (755,  'bottle580'),
    (770,  'bottle300'),
    (785,  'notebook'),
    (800,  'pen-luxury'),
    (815,  'pen-slim'),
    (830,  'cable-tag'),
    (851,  'stanley'),
    (872,  'notebook2'),
    (887,  'notebook3'),
    (902,  'coffee-cup'),
    (917,  'keychain-opener'),
    (932,  'keychain-plain'),
    (946,  'vacuum-bottle'),
    (961,  'dogtag'),
    (976,  'paper-bag'),
    (991,  'tor-bag'),
    (1006, 'name-necklace'),
]

old_btn_marker = '<div class="order-btns-wrap">'

for lineno, pid in PRODUCTS:
    idx = lineno - 1
    if old_btn_marker in lines[idx]:
        indent = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]
        ds_line = f'{indent}<div id="ds_{pid}" class="detail-stock-wrap"></div>\n'
        lines[idx] = ds_line + lines[idx]
        print(f"Line {lineno}: ds_{pid} added ✓")
    else:
        print(f"Line {lineno}: NOT FOUND")

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nStep 1 done.")

# ── 2. Add CSS + update JS ──
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS
detail_stock_css = """
.detail-stock-wrap{display:flex;align-items:center;gap:8px;margin-bottom:0.75rem;flex-wrap:wrap}
.detail-stock-info{display:inline-flex;align-items:center;padding:6px 14px;border-radius:10px;font-size:13px;font-weight:700}
.detail-stock-edit{background:none;border:1.5px solid #cbd5e1;border-radius:8px;padding:4px 10px;font-size:12px;font-weight:600;cursor:pointer;color:#64748b;transition:all 0.2s}
.detail-stock-edit:hover{background:#f1f5f9}
"""
content = content.replace('</style>', detail_stock_css + '</style>', 1)

# ── 3. Update displayStockBadges to also update detail pages ──
old_fn = """function displayStockBadges(stockMap) {
  _stockMap = stockMap;
  document.querySelectorAll('a.card[href^="#"]').forEach(card => {
    const id = card.getAttribute('href').slice(1);
    if(!(id in stockMap)) return;
    const qty = stockMap[id];
    const footer = card.querySelector('.card-footer');
    if(!footer) return;
    const old = footer.querySelector('.stock-badge');
    if(old) old.remove();
    const badge = document.createElement('span');
    const cls = qty === 0 ? 'stock-out' : qty <= 5 ? 'stock-low' : 'stock-ok';
    const txt = qty === 0 ? 'Дууссан' : qty <= 5 ? 'Үлдэгдэл: '+qty : 'Байна: '+qty;
    badge.className = 'stock-badge ' + cls;
    badge.textContent = txt;
    const arrow = footer.querySelector('.card-arrow');
    if(arrow) footer.insertBefore(badge, arrow); else footer.appendChild(badge);
  });
}"""

new_fn = """function displayStockBadges(stockMap) {
  _stockMap = stockMap;
  const isAdm = currentUser && currentUser.email === ADMIN_EMAIL;
  // Card grid badges
  document.querySelectorAll('a.card[href^="#"]').forEach(card => {
    const id = card.getAttribute('href').slice(1);
    if(!(id in stockMap)) return;
    const qty = stockMap[id];
    const footer = card.querySelector('.card-footer');
    if(!footer) return;
    const old = footer.querySelector('.stock-badge');
    if(old) old.remove();
    const badge = document.createElement('span');
    const cls = qty === 0 ? 'stock-out' : qty <= 5 ? 'stock-low' : 'stock-ok';
    const txt = qty === 0 ? 'Дууссан' : qty <= 5 ? 'Үлдэгдэл: '+qty : 'Байна: '+qty;
    badge.className = 'stock-badge ' + cls;
    badge.textContent = txt;
    const arrow = footer.querySelector('.card-arrow');
    if(arrow) footer.insertBefore(badge, arrow); else footer.appendChild(badge);
  });
  // Detail page stock displays
  Object.keys(PRODUCTS_MAP).forEach(id => {
    const el = document.getElementById('ds_' + id);
    if(!el) return;
    if(!(id in stockMap)) { el.innerHTML = ''; return; }
    const qty = stockMap[id];
    const cls = qty === 0 ? 'stock-out' : qty <= 5 ? 'stock-low' : 'stock-ok';
    const txt = qty === 0 ? '⛔ Дууссан' : qty <= 5 ? '⚠️ Үлдэгдэл: '+qty : '✅ Байна: '+qty;
    el.innerHTML = '<span class="detail-stock-info '+cls+'">'+txt+'</span>'
      +(isAdm ? '<button class="detail-stock-edit" data-sid="'+id+'" data-qty="'+qty+'" onclick="editDetailStock(this.dataset.sid,this.dataset.qty)">✎ Засах</button>' : '');
  });
}"""

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print("displayStockBadges updated ✓")
else:
    print("WARNING: displayStockBadges not found exactly")

# ── 4. Update onAuthStateChanged to re-render detail stock when admin logs in ──
old_auth = "onAuthStateChanged(auth,user=>{currentUser=user;updateNavUI(user);});"
new_auth = "onAuthStateChanged(auth,user=>{currentUser=user;updateNavUI(user);if(Object.keys(_stockMap).length)displayStockBadges({..._stockMap});});"
if old_auth in content:
    content = content.replace(old_auth, new_auth)
    print("onAuthStateChanged updated ✓")
else:
    print("WARNING: onAuthStateChanged not found")

# ── 5. Add editDetailStock and saveDetailStock functions before loadStockData(); ──
edit_fns = """
window.editDetailStock = (id, qty) => {
  const el = document.getElementById('ds_' + id);
  if(!el) return;
  el.innerHTML = '<input id="dse_'+id+'" class="stock-input" type="number" min="0" value="'+qty+'" style="width:80px">'
    +'<button class="stock-save-btn" onclick="saveDetailStock(\''+id+'\')">Хадгалах</button>'
    +'<button onclick="displayStockBadges({..._stockMap})" style="padding:5px 10px;background:#e2e8f0;border:none;border-radius:8px;cursor:pointer;font-size:13px">✕</button>';
};

window.saveDetailStock = async (id) => {
  const el = document.getElementById('dse_' + id);
  if(!el) return;
  const val = parseInt(el.value);
  if(isNaN(val) || val < 0) return showToast('Тоо оруулна уу');
  try {
    await setDoc(doc(db,'stock',id), {qty: val});
    _stockMap[id] = val;
    displayStockBadges({..._stockMap});
    showToast('Хадгалагдлаа ✓');
  } catch(e) { showToast('Алдаа: '+e.message); }
};
"""

content = content.replace('loadStockData();', edit_fns + '\nloadStockData();', 1)
print("editDetailStock/saveDetailStock added ✓")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll done!")
