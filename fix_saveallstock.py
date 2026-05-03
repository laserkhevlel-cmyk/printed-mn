import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Split off the last <script type="module"> block
split_tag = '<script type="module">'
parts = content.split(split_tag)
before_module = split_tag.join(parts[:-1]) + split_tag
module_and_after = parts[-1]

end_tag = '</script>'
module_end_idx = module_and_after.index(end_tag)
module_js = module_and_after[:module_end_idx]
after_module = module_and_after[module_end_idx:]

# Find where the broken saveAllStock begins
marker = 'window.saveAllStock = async () => {'
idx = module_js.find(marker)
if idx == -1:
    print("ERROR: saveAllStock not found!")
    sys.exit(1)

print(f"Found saveAllStock at module char {idx}")
print("Content BEFORE saveAllStock ends with:", repr(module_js[idx-30:idx]))

# Keep everything before saveAllStock
module_before_saveall = module_js[:idx]

# The clean replacement for everything from saveAllStock to end of module
clean_tail = r"""window.saveAllStock = async () => {
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

window.editDetailStock = (id, qty) => {
  const el = document.getElementById('ds_' + id);
  if(!el) return;
  el.innerHTML = `<input id="dse_${id}" class="stock-input" type="number" min="0" value="${qty}" style="width:80px"><button class="stock-save-btn" data-sid="${id}" onclick="saveDetailStock(this.dataset.sid)">Хадгалах</button><button onclick="displayStockBadges({..._stockMap})" style="padding:5px 10px;background:#e2e8f0;border:none;border-radius:8px;cursor:pointer;font-size:13px">✕</button>`;
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

loadStockData();
"""

new_module = module_before_saveall + clean_tail
new_content = before_module + new_module + after_module

# Verify: count loadStockData occurrences in module
lsd_count = new_module.count('loadStockData')
print(f"loadStockData occurrences in module: {lsd_count}")

# Verify: balanced braces/parens in clean_tail
print(f"clean_tail {{ count: {clean_tail.count('{')}, }} count: {clean_tail.count('}')}")

# Verify: saveAllStock is properly closed (no orphan await)
if 'await \nwindow' in new_module or 'await\nwindow' in new_module:
    print("WARNING: orphan await still present!")
else:
    print("No orphan await found ✓")

# Verify: editDetailStock is OUTSIDE saveAllStock
save_idx = new_module.find('window.saveAllStock')
edit_idx = new_module.find('window.editDetailStock')
print(f"saveAllStock at {save_idx}, editDetailStock at {edit_idx}")
if edit_idx > save_idx:
    # Check editDetailStock is after saveAllStock's closing brace
    saveall_close = new_module.find('\n};\n\nwindow.editDetailStock', save_idx)
    if saveall_close != -1:
        print("editDetailStock correctly placed AFTER saveAllStock ✓")
    else:
        print("WARNING: editDetailStock may be inside saveAllStock!")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\nFile written successfully!")
print(f"New content length: {len(new_content)}")
