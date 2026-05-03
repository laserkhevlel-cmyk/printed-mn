import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add setDoc to Firestore imports ──
content = content.replace(
    'import{getFirestore,collection,addDoc,getDocs,query,where,orderBy,serverTimestamp,doc,updateDoc}',
    'import{getFirestore,collection,addDoc,getDocs,query,where,orderBy,serverTimestamp,doc,updateDoc,setDoc}'
)

# ── 2. Add stock CSS ──
stock_css = """
/* == Stock badges == */
.stock-badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:700;white-space:nowrap}
.stock-ok{background:#d1fae5;color:#065f46}
.stock-low{background:#fef3c7;color:#d97706}
.stock-out{background:#fee2e2;color:#b91c1c}
.stock-input{width:70px;padding:5px 8px;border:1.5px solid #e2e8f0;border-radius:8px;font-size:13px;text-align:center}
.stock-item{background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:12px;padding:10px 14px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.stock-item-name{font-size:13px;font-weight:600;color:#0f172a;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stock-save-btn{padding:5px 12px;background:linear-gradient(135deg,#1D4ED8,#0EA5E9);color:#fff;border:none;border-radius:8px;font-size:12px;font-weight:700;cursor:pointer}
"""
content = content.replace('</style>', stock_css + '</style>', 1)

# ── 3. Add stock modal HTML before </body> ──
stock_modal = """
<!-- Stock Modal -->
<div id="stockModal" class="modal-overlay" style="display:none" onclick="if(event.target===this)closeStockModal()">
  <div class="modal-box wide">
    <button class="modal-close" onclick="closeStockModal()">&#x2715;</button>
    <div class="modal-title">&#x1F4E6; Үлдэгдэл тохируулах</div>
    <div id="stockList" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:1rem"></div>
    <button class="btn-auth" style="margin-top:1rem" onclick="saveAllStock()">&#x2713; Бүгдийг хадгалах</button>
  </div>
</div>
"""
content = content.replace('</body>', stock_modal + '\n</body>', 1)

# ── 4. Add stock JS before closing </script> ──
stock_js = """
const PRODUCTS_MAP = {
  'medallion':      'Дурсгалын медаллион',
  'bottle580':      'Термо усны сав 580мл',
  'bottle300':      'Термо сав 300мл — 4 өнгө',
  'notebook':       'Тэмдэглэлийн дэвтэр & Бал сет',
  'pen-luxury':     'Тансаг үзэг хайрцагтай',
  'pen-slim':       'Нарийн металл үзэг',
  'cable-tag':      'Кабелийн SS тэмдэглэгээ',
  'stanley':        'Стейнли загвартай термо аяга',
  'notebook2':      'Арьсан тэмдэглэлийн дэвтэр',
  'notebook3':      'Арьсан хавтастай нимгэн дэвтэр',
  'coffee-cup':     'Аялалын кофены ган аяга',
  'keychain-opener':'Олон үйлдэлт түлхүүрийн оосор',
  'keychain-plain': 'Металл түлхүүрийн оосор',
  'vacuum-bottle':  'Цайны шүүртэй ган усны сав',
  'dogtag':         'Зураг хэвлэх боломжтой ган зүүлт',
  'paper-bag':      'Цагаан цаасан уут',
  'tor-bag':        'Хэвлэлтэй тор уут',
  'name-necklace':  'Name necklace — нэрийн зүүлт',
};

let _stockMap = {};

function displayStockBadges(stockMap) {
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
}

async function loadStockData() {
  try {
    const snap = await getDocs(collection(db, 'stock'));
    const map = {};
    snap.forEach(d => { map[d.id] = d.data().qty ?? 0; });
    displayStockBadges(map);
  } catch(e) { console.log('stock err', e.message); }
}

window.openStockModal = async () => {
  document.getElementById('stockModal').style.display = 'flex';
  const list = document.getElementById('stockList');
  list.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:#94a3b8;padding:1rem">Уншиж байна...</div>';
  const snap = await getDocs(collection(db, 'stock'));
  const map = {};
  snap.forEach(d => { map[d.id] = d.data().qty ?? 0; });
  list.innerHTML = Object.entries(PRODUCTS_MAP).map(([id, name]) => {
    const qty = map[id] ?? '';
    return '<div class="stock-item"><span class="stock-item-name" title="'+name+'">'+name+'</span><input class="stock-input" type="number" min="0" id="sq_'+id+'" value="'+qty+'" placeholder="0"><button class="stock-save-btn" onclick="saveStock(\''+id+'\')">✓</button></div>';
  }).join('');
};

window.closeStockModal = () => { document.getElementById('stockModal').style.display = 'none'; };

window.saveStock = async (id) => {
  const val = parseInt(document.getElementById('sq_'+id).value);
  if(isNaN(val) || val < 0) return showToast('Тоо оруулна уу');
  await setDoc(doc(db,'stock',id), {qty: val});
  _stockMap[id] = val;
  displayStockBadges({..._stockMap});
  showToast('Хадгалагдлаа ✓');
};

window.saveAllStock = async () => {
  const updates = [];
  for(const id of Object.keys(PRODUCTS_MAP)) {
    const el = document.getElementById('sq_'+id);
    if(!el || el.value === '') continue;
    const val = parseInt(el.value);
    if(!isNaN(val) && val >= 0) updates.push(setDoc(doc(db,'stock',id), {qty: val}));
  }
  await Promise.all(updates);
  await loadStockData();
  showToast('Бүгд хадгалагдлаа ✓');
};

document.addEventListener('DOMContentLoaded', loadStockData);
"""
content = content.replace('</script>', stock_js + '\n</script>', 1)

# ── 5. Update admin nav UI to add 📦 stock button ──
old_nav = "area.innerHTML='<button class=\"nav-user-btn\" onclick=\"openOrdersModal()\">\\u{1F464} '+name+(isAdmin?' ⭐':'')+\\'</button><button class=\"nav-logout-btn\" onclick=\"doLogout()\">Гарах</button>';"
new_nav = "area.innerHTML='<button class=\"nav-user-btn\" onclick=\"openOrdersModal()\">\\u{1F464} '+name+(isAdmin?' ⭐':'')+\\'</button>'+(isAdmin?'<button class=\"nav-user-btn\" onclick=\"openStockModal()\" style=\"font-size:12px;padding:6px 10px\">📦 Үлдэгдэл</button>':'')+\\'<button class=\"nav-logout-btn\" onclick=\"doLogout()\">Гарах</button>';"
content = content.replace(old_nav, new_nav)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("setDoc import:", 'setDoc' in content[:2000])
print("stock CSS:", 'stock-badge' in content)
print("stock modal:", 'stockModal' in content)
print("stock JS:", 'PRODUCTS_MAP' in content)
print("stock btn in nav:", 'openStockModal' in content)
