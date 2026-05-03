import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken onclick in openStockModal - replace with data attribute approach
old_map = """  list.innerHTML = Object.entries(PRODUCTS_MAP).map(([id, name]) => {
    const qty = map[id] ?? '';
    return '<div class="stock-item"><span class="stock-item-name" title="'+name+'">'+name+'</span><input class="stock-input" type="number" min="0" id="sq_'+id+'" value="'+qty+'" placeholder="0"><button class="stock-save-btn" onclick="saveStock(''+id+'')">✓</button></div>';
  }).join('');"""

new_map = """  list.innerHTML = Object.entries(PRODUCTS_MAP).map(([id, name]) => {
    const qty = (map[id] !== undefined) ? map[id] : '';
    return `<div class="stock-item"><span class="stock-item-name" title="${name}">${name}</span><input class="stock-input" type="number" min="0" id="sq_${id}" value="${qty}" placeholder="0"><button class="stock-save-btn" data-sid="${id}" onclick="saveStock(this.dataset.sid)">✓</button></div>`;
  }).join('');"""

if old_map in content:
    content = content.replace(old_map, new_map)
    print("Fixed openStockModal innerHTML!")
else:
    print("NOT FOUND - searching...")
    idx = content.find("saveStock(''")
    print(repr(content[idx-100:idx+100]))

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    check = f.read()
print("Syntax error gone:", "saveStock(''+" not in check)
print("Template literal used:", "dataset.sid" in check)
