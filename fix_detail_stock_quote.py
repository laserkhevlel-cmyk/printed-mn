import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = """window.editDetailStock = (id, qty) => {
  const el = document.getElementById('ds_' + id);
  if(!el) return;
  el.innerHTML = '<input id="dse_'+id+'" class="stock-input" type="number" min="0" value="'+qty+'" style="width:80px">'
    +'<button class="stock-save-btn" onclick="saveDetailStock(''+id+'')">Хадгалах</button>'
    +'<button onclick="displayStockBadges({..._stockMap})" style="padding:5px 10px;background:#e2e8f0;border:none;border-radius:8px;cursor:pointer;font-size:13px">✕</button>';
};"""

new = """window.editDetailStock = (id, qty) => {
  const el = document.getElementById('ds_' + id);
  if(!el) return;
  el.innerHTML = `<input id="dse_${id}" class="stock-input" type="number" min="0" value="${qty}" style="width:80px"><button class="stock-save-btn" data-sid="${id}" onclick="saveDetailStock(this.dataset.sid)">Хадгалах</button><button onclick="displayStockBadges({..._stockMap})" style="padding:5px 10px;background:#e2e8f0;border:none;border-radius:8px;cursor:pointer;font-size:13px">✕</button>`;
};"""

if old in content:
    content = content.replace(old, new)
    print("Fixed editDetailStock ✓")
else:
    print("NOT FOUND - checking...")
    idx = content.find("saveDetailStock(''")
    if idx != -1:
        print("Found bad pattern at:", idx)
        print(repr(content[idx-50:idx+100]))

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Bad quote pattern gone:", "saveDetailStock(''+" not in content)
print("Template literal used:", 'dse_${id}' in content)
