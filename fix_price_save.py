import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix savePriceItem - add try/catch
old = """window.savePriceItem = async (id) => {
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
};"""

new = """window.savePriceItem = async (id) => {
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
  try {
    await setDoc(doc(db,'prices',id), {tiers});
    _priceMap[id] = tiers;
    showToast('Хадгалагдлаа ✓');
  } catch(e) { showToast('Алдаа: ' + e.message); }
};"""

if old in content:
    content = content.replace(old, new)
    print("savePriceItem fixed ✓")
else:
    print("savePriceItem NOT FOUND")

# Fix saveAllPrices - add try/catch
old2 = """window.saveAllPrices = async () => {
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
};"""

new2 = """window.saveAllPrices = async () => {
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
  try {
    await Promise.all(updates);
    showToast('Бүгд хадгалагдлаа ✓');
  } catch(e) { showToast('Алдаа: ' + e.message); }
};"""

if old2 in content:
    content = content.replace(old2, new2)
    print("saveAllPrices fixed ✓")
else:
    print("saveAllPrices NOT FOUND")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
