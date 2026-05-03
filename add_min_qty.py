import sys, re
sys.stdout.reconfigure(encoding='utf-8')

HTML = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Update _stockMap to store {qty, minQty} and loadStockData ──────────────
old_vars = "let _stockMap = {};"
new_vars = "let _stockMap = {};\nlet _minQtyMap = {};"

if '_minQtyMap' not in content:
    content = content.replace(old_vars, new_vars, 1)
    print("1a. _minQtyMap variable added ✓")
else:
    print("1a. _minQtyMap already exists")

old_load = """async function loadStockData() {
  try {
    const snap = await getDocs(collection(db, 'stock'));
    const map = {};
    snap.forEach(d => { map[d.id] = d.data().qty ?? 0; });
    displayStockBadges(map);
  } catch(e) { console.log('stock err', e.message); }
}"""

new_load = """async function loadStockData() {
  try {
    const snap = await getDocs(collection(db, 'stock'));
    const map = {};
    snap.forEach(d => {
      const data = d.data();
      map[d.id] = data.qty ?? 0;
      if (data.minQty !== undefined) _minQtyMap[d.id] = data.minQty;
    });
    displayStockBadges(map);
  } catch(e) { console.log('stock err', e.message); }
}"""

if 'data.minQty' not in content:
    if old_load in content:
        content = content.replace(old_load, new_load, 1)
        print("1b. loadStockData updated ✓")
    else:
        print("1b. loadStockData not found — trying partial match")
else:
    print("1b. loadStockData already updated")

# ── 2. Update displayStockBadges to use minQty ────────────────────────────────
old_badge_card = "    const cls = qty === 0 ? 'stock-out' : qty <= 5 ? 'stock-low' : 'stock-ok';\n    const txt = qty === 0 ? 'Дууссан' : qty <= 5 ? 'Үлдэгдэл: '+qty : 'Байна: '+qty;"
new_badge_card = """    const _min = _minQtyMap[id] ?? 0;
    const cls = qty <= _min ? 'stock-out' : qty <= _min + 5 ? 'stock-low' : 'stock-ok';
    const txt = qty <= _min ? 'Дууссан' : qty <= _min + 5 ? 'Үлдэгдэл: '+qty : 'Байна: '+qty;"""

if '_minQtyMap[id]' not in content:
    if old_badge_card in content:
        content = content.replace(old_badge_card, new_badge_card, 1)
        print("2a. Card badge updated ✓")
    else:
        print("2a. Card badge pattern not found")
else:
    print("2a. Card badge already updated")

old_badge_detail = "    const cls = qty === 0 ? 'stock-out' : qty <= 5 ? 'stock-low' : 'stock-ok';\n    const txt = qty === 0 ? '⛔ Дууссан' : qty <= 5 ? '⚠️ Үлдэгдэл: '+qty : '✅ Байна: '+qty;"
new_badge_detail = """    const _minD = _minQtyMap[id] ?? 0;
    const cls = qty <= _minD ? 'stock-out' : qty <= _minD + 5 ? 'stock-low' : 'stock-ok';
    const txt = qty <= _minD ? '⛔ Дууссан' : qty <= _minD + 5 ? '⚠️ Үлдэгдэл: '+qty : '✅ Байна: '+qty;"""

if '_minD' not in content:
    if old_badge_detail in content:
        content = content.replace(old_badge_detail, new_badge_detail, 1)
        print("2b. Detail badge updated ✓")
    else:
        print("2b. Detail badge pattern not found")
else:
    print("2b. Detail badge already updated")

# ── 3. Update submitOrder to respect minQty ───────────────────────────────────
old_order_check = "if(_pid&&_pid in _stockMap){const _avail=_stockMap[_pid];if(_avail===0)return showErr('orderErr','Уучлаарай, энэ бүтээгдэхүүн дууссан байна.');if(Number(qty)>_avail)return showErr('orderErr','Үлдэгдэл '+_avail+' ширхэг байна, тоогоо багасгана уу.');}"
new_order_check = "if(_pid&&_pid in _stockMap){const _avail=_stockMap[_pid];const _minOrd=_minQtyMap[_pid]??0;if(_avail<=_minOrd)return showErr('orderErr','Уучлаарай, энэ бүтээгдэхүүн дууссан байна.');if(Number(qty)>(_avail-_minOrd))return showErr('orderErr','Үлдэгдэл '+(_avail-_minOrd)+' ширхэг байна, тоогоо багасгана уу.');}"

if '_minOrd' not in content:
    if old_order_check in content:
        content = content.replace(old_order_check, new_order_check, 1)
        print("3. submitOrder check updated ✓")
    else:
        print("3. submitOrder check not found")
else:
    print("3. submitOrder already updated")

# ── 4. Update Stock Modal to show and edit minQty ────────────────────────────
# Find the openStockModal function and update the stock list to show minQty input
old_stock_item = "    return `<div class=\"stock-item\"><span class=\"stock-item-name\" title=\"${name}\">${name}</span><input class=\"stock-input\" type=\"number\" min=\"0\" id=\"sq_${id}\" value=\"${qty}\" placeholder=\"0\"><button class=\"stock-save-btn\" data-sid=\"${id}\" onclick=\"saveStock(this.dataset.sid)\">✓</button></div>`;"
new_stock_item = "    const mq = (map[id] !== undefined && map[id].minQty !== undefined) ? map[id].minQty : (_minQtyMap[id] ?? 0);\n    return `<div class=\"stock-item\"><span class=\"stock-item-name\" title=\"${name}\">${name}</span><input class=\"stock-input\" type=\"number\" min=\"0\" id=\"sq_${id}\" value=\"${qty}\" placeholder=\"0\" style=\"width:64px\"><span style=\"font-size:11px;color:#94a3b8;margin:0 4px\">доод:</span><input class=\"stock-input\" type=\"number\" min=\"0\" id=\"smq_${id}\" value=\"${mq}\" placeholder=\"0\" style=\"width:52px\"><button class=\"stock-save-btn\" data-sid=\"${id}\" onclick=\"saveStock(this.dataset.sid)\">✓</button></div>`;"

# The openStockModal reads stock and builds the map - need to update it to store minQty too
old_snap_map = "  snap.forEach(d => { map[d.id] = d.data().qty ?? 0; });\n  list.innerHTML = Object.entries(PRODUCTS_MAP).map(([id, name]) => {\n    const qty = (map[id] !== undefined) ? map[id] : '';"
new_snap_map = "  snap.forEach(d => { const dd = d.data(); map[d.id] = { qty: dd.qty ?? 0, minQty: dd.minQty ?? 0 }; });\n  list.innerHTML = Object.entries(PRODUCTS_MAP).map(([id, name]) => {\n    const qty = (map[id] !== undefined) ? map[id].qty : '';"

if 'smq_' not in content:
    if old_snap_map in content:
        content = content.replace(old_snap_map, new_snap_map, 1)
        print("4a. openStockModal map updated ✓")
    else:
        print("4a. openStockModal map pattern not found")
    if old_stock_item in content:
        content = content.replace(old_stock_item, new_stock_item, 1)
        print("4b. Stock list item updated ✓")
    else:
        print("4b. Stock list item pattern not found")
else:
    print("4. Stock modal already updated")

# ── 5. Update saveStock and saveAllStock to write minQty ─────────────────────
old_save_stock = """window.saveStock = async (id) => {
  const val = parseInt(document.getElementById('sq_'+id).value);
  if(isNaN(val) || val < 0) return showToast('Тоо оруулна уу');
  await setDoc(doc(db,'stock',id), {qty: val});
  _stockMap[id] = val;
  displayStockBadges({..._stockMap});
  showToast('Хадгалагдлаа ✓');
};"""
new_save_stock = """window.saveStock = async (id) => {
  const val = parseInt(document.getElementById('sq_'+id).value);
  if(isNaN(val) || val < 0) return showToast('Тоо оруулна уу');
  const mqEl = document.getElementById('smq_'+id);
  const mq = mqEl ? parseInt(mqEl.value)||0 : (_minQtyMap[id]??0);
  await setDoc(doc(db,'stock',id), {qty: val, minQty: mq}, {merge:true});
  _stockMap[id] = val;
  _minQtyMap[id] = mq;
  displayStockBadges({..._stockMap});
  showToast('Хадгалагдлаа ✓');
};"""

if 'smq_' not in content or 'minQty: mq' not in content:
    if old_save_stock in content:
        content = content.replace(old_save_stock, new_save_stock, 1)
        print("5a. saveStock updated ✓")
    else:
        print("5a. saveStock not found")
else:
    print("5a. saveStock already updated")

old_saveall = """window.saveAllStock = async () => {
  const updates = [];
  for(const id of Object.keys(PRODUCTS_MAP)) {
    const el = document.getElementById('sq_'+id);
    if(!el || el.value === '') continue;
    const val = parseInt(el.value);
    if(!isNaN(val) && val >= 0) updates.push(setDoc(doc(db,'stock',id), {qty: val}));
  }
  await Promise.all(updates);
  showToast('Бүгд хадгалагдлаа ✓');
};"""
new_saveall = """window.saveAllStock = async () => {
  const updates = [];
  for(const id of Object.keys(PRODUCTS_MAP)) {
    const el = document.getElementById('sq_'+id);
    if(!el || el.value === '') continue;
    const val = parseInt(el.value);
    const mqEl = document.getElementById('smq_'+id);
    const mq = mqEl ? parseInt(mqEl.value)||0 : (_minQtyMap[id]??0);
    if(!isNaN(val) && val >= 0) {
      updates.push(setDoc(doc(db,'stock',id), {qty: val, minQty: mq}, {merge:true}));
      _minQtyMap[id] = mq;
    }
  }
  await Promise.all(updates);
  displayStockBadges({..._stockMap});
  showToast('Бүгд хадгалагдлаа ✓');
};"""

if old_saveall in content:
    content = content.replace(old_saveall, new_saveall, 1)
    print("5b. saveAllStock updated ✓")
else:
    print("5b. saveAllStock not found")

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone!")
