import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Add _currentProductId variable after _priceMap ──
old = 'let _priceMap = {};'
new = 'let _priceMap = {};\nlet _currentProductId = null;'
if old in content:
    content = content.replace(old, new)
    print("1. _currentProductId added ✓")
else:
    print("1. _priceMap not found!")

# ── 2. Set _currentProductId in openOrderModal when product is known ──
old = ("  const pg=document.getElementById('orderProductGroup');\n"
       "  const pd=document.getElementById('orderProductDisplay');\n"
       "  const ps=document.getElementById('orderProduct');\n"
       "  const pt=document.getElementById('orderPrintType');\n"
       "  if(product){")
new = ("  const pg=document.getElementById('orderProductGroup');\n"
       "  const pd=document.getElementById('orderProductDisplay');\n"
       "  const ps=document.getElementById('orderProduct');\n"
       "  const pt=document.getElementById('orderPrintType');\n"
       "  _currentProductId=product?Object.keys(PRODUCTS_MAP).find(k=>PRODUCTS_MAP[k]===product)||null:null;\n"
       "  if(product){")
if old in content:
    content = content.replace(old, new)
    print("2. _currentProductId set in openOrderModal ✓")
else:
    print("2. openOrderModal block not found!")

# ── 3. Rewrite updateOrderPrice to use _currentProductId directly ──
old = """window.updateOrderPrice = () => {
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
};"""

new = """window.updateOrderPrice = () => {
  const qty = parseInt(document.getElementById('orderQty').value) || 0;
  const info = document.getElementById('orderPriceInfo');
  if(!_currentProductId || qty < 1) { info.style.display='none'; return; }
  const tiers = _priceMap[_currentProductId];
  if(!tiers || !tiers.length) { info.style.display='none'; return; }
  const tier = tiers.find(t => qty >= t.min && (t.max === null || qty <= t.max));
  if(!tier) { info.style.display='none'; return; }
  const total = tier.price * qty;
  info.style.display = 'block';
  info.innerHTML = '💰 Нэгж үнэ: <b>' + tier.price.toLocaleString() + '₮</b> &nbsp;·&nbsp; Нийт: <b style="color:#15803d">' + total.toLocaleString() + '₮</b>';
};"""

if old in content:
    content = content.replace(old, new)
    print("3. updateOrderPrice rewritten ✓")
else:
    print("3. updateOrderPrice not found!")

# ── 4. Reset _currentProductId on closeOrderModal ──
old = ("window.closeOrderModal=()=>{"
       "const _pi=document.getElementById('orderPriceInfo');if(_pi)_pi.style.display='none';"
       "document.getElementById('orderModal').style.display='none';")
new = ("window.closeOrderModal=()=>{"
       "_currentProductId=null;"
       "const _pi=document.getElementById('orderPriceInfo');if(_pi)_pi.style.display='none';"
       "document.getElementById('orderModal').style.display='none';")
if old in content:
    content = content.replace(old, new)
    print("4. closeOrderModal reset ✓")
else:
    print("4. closeOrderModal not found!")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone!")
