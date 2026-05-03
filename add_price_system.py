import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

# ── 1. Add oninput to orderQty ──
old = '<input class="form-input" type="number" id="orderQty" min="1" value="1">'
new = '<input class="form-input" type="number" id="orderQty" min="1" value="1" oninput="updateOrderPrice()">'
if old in content:
    content = content.replace(old, new)
    print("1. orderQty oninput added ✓")
else:
    errors.append("1. orderQty not found")

# ── 2. Add price info div after qty/variant grid ──
old = ('    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">\n'
       '      <div class="form-group"><label class="form-label">Тоо ширхэг</label>'
       '<input class="form-input" type="number" id="orderQty" min="1" value="1" oninput="updateOrderPrice()"></div>\n'
       '      <div class="form-group"><label class="form-label">Өнгө / Хэмжээ</label>'
       '<input class="form-input" type="text" id="orderVariant" placeholder="Хар, A5..."></div>\n'
       '    </div>')
new = (old + '\n'
       '    <div id="orderPriceInfo" style="display:none;background:#f0fdf4;border:1.5px solid #bbf7d0;'
       'border-radius:12px;padding:10px 16px;margin-bottom:0.5rem;font-size:14px;color:#15803d"></div>')
if old in content:
    content = content.replace(old, new)
    print("2. orderPriceInfo div added ✓")
else:
    errors.append("2. orderQty grid not found")

# ── 3. Add price modal HTML before stockModal ──
stock_modal_start = '<div id="stockModal"'
price_modal_html = (
    '<div id="priceModal" class="modal-overlay" style="display:none" onclick="if(event.target===this)closePriceModal()">\n'
    '  <div class="modal-box wide">\n'
    '    <button class="modal-close" onclick="closePriceModal()">&#x2715;</button>\n'
    '    <div class="modal-title">&#x1F4B0; &#x04AE;&#x043D;&#x044D; &#x0442;&#x043E;&#x0445;&#x0438;&#x0440;&#x0443;&#x0443;&#x043B;&#x0430;&#x0445;</div>\n'
    '    <div style="font-size:12px;color:#94a3b8;margin-bottom:0.5rem">&#x0424;&#x043E;&#x0440;&#x043C;&#x0430;&#x0442;: 1-10:5000,11-50:4000,51+:3000 &nbsp;(&#x0448;&#x0438;&#x0440;&#x0445;&#x044D;&#x0433;:&#x0442;&#x04E9;&#x0433;&#x0440;&#x04E9;&#x0433;)</div>\n'
    '    <div id="priceList" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:0.5rem"></div>\n'
    '    <button class="btn-auth" style="margin-top:1rem" onclick="saveAllPrices()">&#x2713; &#x0411;&#x04AF;&#x0433;&#x0434;&#x0438;&#x0439;&#x0433; &#x0445;&#x0430;&#x0434;&#x0433;&#x0430;&#x043B;&#x0430;&#x0445;</button>\n'
    '  </div>\n'
    '</div>\n\n'
)
if stock_modal_start in content:
    content = content.replace(stock_modal_start, price_modal_html + stock_modal_start, 1)
    print("3. priceModal HTML added ✓")
else:
    errors.append("3. stockModal not found for priceModal insertion")

# ── 4. JS module changes ──
split_tag = '<script type="module">'
parts = content.split(split_tag)
before_module = split_tag.join(parts[:-1]) + split_tag
module_and_after = parts[-1]
end_tag = '</script>'
module_end_idx = module_and_after.index(end_tag)
module_js = module_and_after[:module_end_idx]
after_module = module_and_after[module_end_idx:]

# 4a. Add _priceMap after _stockMap
old_js = 'let _stockMap = {};'
new_js = 'let _stockMap = {};\nlet _priceMap = {};'
if old_js in module_js:
    module_js = module_js.replace(old_js, new_js)
    print("4a. _priceMap variable added ✓")
else:
    errors.append("4a. _stockMap not found")

# 4b. Add loadPriceData function before openStockModal
old_js = 'window.openStockModal = async () => {'
new_js = ('async function loadPriceData(){\n'
          '  try{\n'
          '    const snap=await getDocs(collection(db,\'prices\'));\n'
          '    snap.forEach(d=>{_priceMap[d.id]=d.data().tiers||[];});\n'
          '  }catch(e){console.log(\'price err\',e.message);}\n'
          '}\n\n'
          'window.openStockModal = async () => {')
if old_js in module_js:
    module_js = module_js.replace(old_js, new_js)
    print("4b. loadPriceData function added ✓")
else:
    errors.append("4b. openStockModal not found for loadPriceData insertion")

# 4c. Add 💰 Үнэ button next to 📦 Үлдэгдэл in nav
old_js = '+(isAdmin?\'<button class="nav-user-btn" onclick="openStockModal()" style="font-size:12px;padding:6px 10px">📦 Үлдэгдэл</button>\':\'\')'
new_js = ('+(isAdmin?\'<button class="nav-user-btn" onclick="openStockModal()" style="font-size:12px;padding:6px 10px">📦 Үлдэгдэл</button>'
          '<button class="nav-user-btn" onclick="openPriceModal()" style="font-size:12px;padding:6px 10px">💰 Үнэ</button>\':\'\')')
if old_js in module_js:
    module_js = module_js.replace(old_js, new_js)
    print("4c. 💰 Үнэ nav button added ✓")
else:
    errors.append("4c. nav stock button not found")
    # show what's there
    idx = module_js.find('openStockModal()')
    if idx != -1:
        print("  found openStockModal at:", repr(module_js[idx-50:idx+80]))

# 4d. Call updateOrderPrice() when order modal opens (after setting display to flex)
old_js = "  document.getElementById('orderModal').style.display='flex';"
new_js = ("  document.getElementById('orderQty').value=1;updateOrderPrice();\n"
          "  document.getElementById('orderModal').style.display='flex';")
if old_js in module_js:
    module_js = module_js.replace(old_js, new_js)
    print("4d. updateOrderPrice call on open added ✓")
else:
    errors.append("4d. orderModal display=flex not found")

# 4e. Hide price info on closeOrderModal
old_js = "window.closeOrderModal=()=>{document.getElementById('orderModal').style.display='none';"
new_js = ("window.closeOrderModal=()=>{"
          "const _pi=document.getElementById('orderPriceInfo');if(_pi)_pi.style.display='none';"
          "document.getElementById('orderModal').style.display='none';")
if old_js in module_js:
    module_js = module_js.replace(old_js, new_js)
    print("4e. closeOrderModal price hide added ✓")
else:
    errors.append("4e. closeOrderModal not found")

# 4f. Replace final standalone loadStockData(); with price functions + both data loads
# Find last occurrence of bare loadStockData();
last_idx = module_js.rfind('\nloadStockData();\n')
if last_idx != -1:
    price_functions = """
window.updateOrderPrice = () => {
  const product = document.getElementById('orderProduct').value;
  const qty = parseInt(document.getElementById('orderQty').value) || 0;
  const info = document.getElementById('orderPriceInfo');
  if(!product || !qty || qty < 1) { info.style.display='none'; return; }
  const pid = Object.keys(PRODUCTS_MAP).find(k => PRODUCTS_MAP[k] === product);
  if(!pid || !_priceMap[pid] || !_priceMap[pid].length) { info.style.display='none'; return; }
  const tier = _priceMap[pid].find(t => qty >= t.min && (t.max === null || qty <= t.max));
  if(!tier) { info.style.display='none'; return; }
  const total = tier.price * qty;
  info.style.display = 'block';
  info.innerHTML = '💰 Нэгж үнэ: <b>' + tier.price.toLocaleString() + '₮</b> &nbsp;·&nbsp; Нийт: <b>' + total.toLocaleString() + '₮</b>';
};

window.openPriceModal = async () => {
  document.getElementById('priceModal').style.display = 'flex';
  const list = document.getElementById('priceList');
  list.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:#94a3b8;padding:1rem">Уншиж байна...</div>';
  const snap = await getDocs(collection(db, 'prices'));
  const map = {};
  snap.forEach(d => { map[d.id] = d.data().tiers || []; });
  list.innerHTML = Object.entries(PRODUCTS_MAP).map(([id, name]) => {
    const tiers = map[id] || [];
    const str = tiers.map(t => t.max === null ? t.min+'+:'+t.price : t.min+'-'+t.max+':'+t.price).join(',');
    return '<div class="stock-item"><span class="stock-item-name" title="'+name+'">'+name+'</span>'
      +'<input class="stock-input" type="text" id="pq_'+id+'" value="'+str+'" placeholder="1-10:5000,11+:4000" style="width:145px">'
      +'<button class="stock-save-btn" data-sid="'+id+'" onclick="savePriceItem(this.dataset.sid)">✓</button></div>';
  }).join('');
};

window.closePriceModal = () => { document.getElementById('priceModal').style.display = 'none'; };

window.savePriceItem = async (id) => {
  const el = document.getElementById('pq_'+id);
  if(!el) return;
  const tiers = el.value.trim().split(',').map(s => {
    s = s.trim();
    const parts = s.split(':');
    if(parts.length < 2) return null;
    const range = parts[0].trim();
    const price = parseInt(parts[1]);
    if(isNaN(price)) return null;
    if(range.endsWith('+')) return {min: parseInt(range), max: null, price};
    const rng = range.split('-').map(Number);
    return {min: rng[0], max: rng[1], price};
  }).filter(t => t && !isNaN(t.min));
  await setDoc(doc(db,'prices',id), {tiers});
  _priceMap[id] = tiers;
  showToast('Хадгалагдлаа ✓');
};

window.saveAllPrices = async () => {
  const updates = [];
  for(const id of Object.keys(PRODUCTS_MAP)) {
    const el = document.getElementById('pq_'+id);
    if(!el || !el.value.trim()) continue;
    const tiers = el.value.trim().split(',').map(s => {
      s = s.trim();
      const parts = s.split(':');
      if(parts.length < 2) return null;
      const range = parts[0].trim();
      const price = parseInt(parts[1]);
      if(isNaN(price)) return null;
      if(range.endsWith('+')) return {min: parseInt(range), max: null, price};
      const rng = range.split('-').map(Number);
      return {min: rng[0], max: rng[1], price};
    }).filter(t => t && !isNaN(t.min));
    updates.push(setDoc(doc(db,'prices',id), {tiers}));
    _priceMap[id] = tiers;
  }
  await Promise.all(updates);
  showToast('Бүгд хадгалагдлаа ✓');
};

loadStockData();
loadPriceData();
"""
    module_js = module_js[:last_idx] + '\n' + price_functions
    print("4f. price functions + loadPriceData() added ✓")
else:
    errors.append("4f. standalone loadStockData(); not found")

content = before_module + module_js + after_module

# ── Report ──
if errors:
    print("\nERRORS:")
    for e in errors:
        print(" !", e)
else:
    print("\nAll changes applied successfully!")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"File written. Size: {len(content)} bytes")
