import sys
sys.stdout.reconfigure(encoding='utf-8')

HTML = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add CSS ─────────────────────────────────────────────────────────────────
css = """
#prodEditModal{position:fixed;inset:0;z-index:1500;background:rgba(0,0,0,0.55);display:none;align-items:center;justify-content:center;padding:16px}
#prodEditModal.open{display:flex}
#prodEditBox{background:#fff;border-radius:20px;padding:1.75rem;width:100%;max-width:480px;max-height:90vh;overflow-y:auto;box-shadow:0 24px 80px rgba(0,0,0,0.25);position:relative}
#prodEditBox h3{font-family:'Inter',sans-serif;font-size:16px;font-weight:800;color:#0f172a;margin-bottom:1.25rem}
.pedit-label{font-size:12px;font-weight:700;color:#64748b;margin-bottom:4px;margin-top:12px;letter-spacing:.05em;text-transform:uppercase}
.pedit-input{width:100%;padding:9px 12px;border:1.5px solid #e2e8f0;border-radius:10px;font-size:14px;font-family:'Inter',sans-serif;box-sizing:border-box;resize:vertical}
.pedit-input:focus{outline:none;border-color:#1D4ED8}
.pedit-hint{font-size:11px;color:#94a3b8;margin-top:3px}
.prod-edit-btn{display:inline-flex;align-items:center;gap:5px;background:rgba(37,99,235,0.08);border:1.5px solid rgba(37,99,235,0.2);border-radius:8px;padding:5px 12px;font-size:12px;font-weight:700;color:#1D4ED8;cursor:pointer;transition:all 0.2s;font-family:'Inter',sans-serif;margin-top:0.75rem}
.prod-edit-btn:hover{background:rgba(37,99,235,0.15)}
"""
if '#prodEditModal' not in content:
    content = content.replace('</style>', css + '</style>', 1)
    print("1. CSS added ✓")
else:
    print("1. CSS already exists")

# ── 2. Add modal HTML ──────────────────────────────────────────────────────────
modal_html = """
<div id="prodEditModal" onclick="if(event.target===this)closeProdEdit()">
  <div id="prodEditBox">
    <button class="modal-close" onclick="closeProdEdit()" style="position:absolute;top:1rem;right:1rem">&#x2715;</button>
    <h3>✎ Бүтээгдэхүүний мэдээлэл засах</h3>
    <input type="hidden" id="pedit_pid">
    <div class="pedit-label">Бүтээгдэхүүний нэр</div>
    <input class="pedit-input" id="pedit_name" type="text" placeholder="Нэр">
    <div class="pedit-label">Тайлбар</div>
    <textarea class="pedit-input" id="pedit_desc" rows="3" placeholder="Тайлбар текст"></textarea>
    <div class="pedit-label">Онцлогууд <span class="pedit-hint">(мөр бүрт нэг онцлог)</span></div>
    <textarea class="pedit-input" id="pedit_features" rows="6" placeholder="Онцлог 1&#10;Онцлог 2&#10;Онцлог 3"></textarea>
    <button class="btn-auth" style="margin-top:1.25rem" onclick="saveProdEdit()">&#x2713; Хадгалах</button>
  </div>
</div>
"""
if 'prodEditModal' not in content:
    content = content.replace('<div id="detail-screen"></div>', modal_html + '\n<div id="detail-screen"></div>')
    print("2. Modal HTML added ✓")
else:
    print("2. Modal already exists")

# ── 3. Add JS functions ────────────────────────────────────────────────────────
js = """
// ── Product content editing ──────────────────────────────────────────────────
let _prodContent = {};

async function loadProductContent() {
  try {
    const snap = await getDocs(collection(db, 'products'));
    snap.forEach(d => { _prodContent[d.id] = d.data(); });
    applyProductContent();
  } catch(e) { console.log('prodContent err', e.message); }
}

function applyProductContent() {
  Object.entries(_prodContent).forEach(([pid, data]) => {
    const sec = document.getElementById(pid);
    if (!sec) return;
    if (data.name) {
      const h2 = sec.querySelector('h2');
      if (h2) h2.textContent = data.name;
      const lbl = sec.querySelector('.section-label');
      if (lbl) lbl.textContent = '✦ ' + data.name;
    }
    if (data.desc) {
      const p = sec.querySelector('.detail-content > p');
      if (p) p.textContent = data.desc;
    }
    if (data.features && data.features.length) {
      const ul = sec.querySelector('ul.features');
      if (ul) ul.innerHTML = data.features.map(f => '<li>' + f + '</li>').join('');
    }
  });
}

window.openProdEdit = (pid) => {
  const data = _prodContent[pid] || {};
  const sec = document.getElementById(pid);
  document.getElementById('pedit_pid').value = pid;
  // Prefill from Firestore data or from current DOM
  const h2 = sec ? sec.querySelector('h2') : null;
  const p  = sec ? sec.querySelector('.detail-content > p') : null;
  const ul = sec ? sec.querySelector('ul.features') : null;
  document.getElementById('pedit_name').value = data.name || (h2 ? h2.textContent : '');
  document.getElementById('pedit_desc').value = data.desc || (p ? p.textContent : '');
  const feats = data.features || (ul ? Array.from(ul.querySelectorAll('li')).map(li => li.textContent) : []);
  document.getElementById('pedit_features').value = feats.join('\\n');
  document.getElementById('prodEditModal').classList.add('open');
};

window.closeProdEdit = () => {
  document.getElementById('prodEditModal').classList.remove('open');
};

window.saveProdEdit = async () => {
  const pid = document.getElementById('pedit_pid').value;
  if (!pid) return;
  const name     = document.getElementById('pedit_name').value.trim();
  const desc     = document.getElementById('pedit_desc').value.trim();
  const features = document.getElementById('pedit_features').value.split('\\n').map(s=>s.trim()).filter(Boolean);
  try {
    await setDoc(doc(db, 'products', pid), { name, desc, features }, { merge: true });
    _prodContent[pid] = { ...(_prodContent[pid]||{}), name, desc, features };
    applyProductContent();
    closeProdEdit();
    showToast('Мэдээлэл хадгалагдлаа ✓');
  } catch(e) { showToast('Алдаа: ' + e.message); }
};

function addProdEditButtons() {
  const isAdmin = currentUser && ADMIN_EMAILS.includes(currentUser.email);
  if (!isAdmin) return;
  document.querySelectorAll('.detail-section').forEach(sec => {
    const pid = sec.id;
    if (!pid || sec.querySelector('.prod-edit-btn')) return;
    const content = sec.querySelector('.detail-content');
    if (!content) return;
    const btn = document.createElement('button');
    btn.className = 'prod-edit-btn';
    btn.innerHTML = '✎ Мэдээлэл засах';
    btn.onclick = () => openProdEdit(pid);
    content.appendChild(btn);
  });
}
"""

# Insert JS before loadStockData() call at bottom
old_load = 'loadStockData();'
if 'loadProductContent' not in content:
    new_load = js + '\nloadStockData();'
    content = content.replace(old_load, new_load, 1)
    print("3. JS functions added ✓")
else:
    print("3. JS already exists")

# ── 4. Call loadProductContent and addProdEditButtons after auth ──────────────
old_auth = "if(Object.keys(_stockMap).length)displayStockBadges({..._stockMap});"
new_auth = "if(Object.keys(_stockMap).length)displayStockBadges({..._stockMap});\n  loadProductContent();\n  addProdEditButtons();"
if 'addProdEditButtons' not in content:
    if old_auth in content:
        content = content.replace(old_auth, new_auth)
        print("4. Auth hook added ✓")
    else:
        print("4. Auth hook NOT FOUND")
else:
    print("4. Auth hook already exists")

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone!")
