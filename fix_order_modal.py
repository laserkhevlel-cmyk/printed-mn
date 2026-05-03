import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/firebase_modals.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add id to product group div
content = content.replace(
    '<div class="form-group"><label class="form-label">Бүтээгдэхүүн</label>',
    '<div class="form-group" id="orderProductGroup"><label class="form-label">Бүтээгдэхүүн</label>'
)

# 2. Add product display div after product group closing </div>
# The product group ends with </select>\n    </div>
content = content.replace(
    '      </select>\n    </div>\n    <div class="form-group"><label class="form-label">Хэвлэлийн төрөл</label>',
    '      </select>\n    </div>\n    <div class="form-group" id="orderProductDisplay" style="display:none"><label class="form-label">Бүтээгдэхүүн</label><div style="padding:10px 14px;border:1.5px solid #e2e8f0;border-radius:10px;font-size:14px;background:#f8fafc;font-weight:600;color:#0f172a" id="orderProductName"></div></div>\n    <div class="form-group"><label class="form-label">Хэвлэлийн төрөл</label>'
)

# 3. Update openOrderModal function
old_open = '''window.openOrderModal=(product)=>{
  if(!currentUser){openAuthModal();return;}
  if(product)document.getElementById('orderProduct').value=product;
  document.getElementById('orderName').value=currentUser.displayName||'';
  document.getElementById('orderPhone').value=currentUser.photoURL||'';
  document.getElementById('orderModal').style.display='flex';
};'''

new_open = '''window.openOrderModal=(btn)=>{
  if(!currentUser){openAuthModal();return;}
  const product=btn&&btn.dataset?btn.dataset.product:null;
  const printTypes=btn&&btn.dataset&&btn.dataset.prints?btn.dataset.prints.split('|'):null;
  const pg=document.getElementById('orderProductGroup');
  const pd=document.getElementById('orderProductDisplay');
  const ps=document.getElementById('orderProduct');
  const pt=document.getElementById('orderPrintType');
  if(product){
    pg.style.display='none';pd.style.display='block';
    document.getElementById('orderProductName').textContent=product;
    ps.value=product;
    pt.innerHTML='<option value="">— Сонгох —</option>';
    (printTypes||['Лазер хэвлэл','UV хэвлэл','DTF хэвлэл','Сублимац хэвлэл','Бизнес хэвлэл']).forEach(t=>{const o=document.createElement('option');o.value=t;o.textContent=t;pt.appendChild(o);});
    if(printTypes&&printTypes.length===1)pt.value=printTypes[0];
  }else{
    pg.style.display='';pd.style.display='none';
    pt.innerHTML='<option value="">— Сонгох —</option><option>Лазер хэвлэл</option><option>UV хэвлэл</option><option>DTF хэвлэл</option><option>Сублимац хэвлэл</option><option>Бизнес хэвлэл</option>';
  }
  document.getElementById('orderName').value=currentUser.displayName||'';
  document.getElementById('orderPhone').value=currentUser.photoURL||'';
  document.getElementById('orderModal').style.display='flex';
};'''

content = content.replace(old_open, new_open)

# 4. Update closeOrderModal to reset state
content = content.replace(
    "window.closeOrderModal=()=>{document.getElementById('orderModal').style.display='none';};",
    "window.closeOrderModal=()=>{document.getElementById('orderModal').style.display='none';document.getElementById('orderProductGroup').style.display='';document.getElementById('orderProductDisplay').style.display='none';document.getElementById('orderProduct').value='';};"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("firebase_modals.html updated!")
print("orderProductGroup id:", 'id="orderProductGroup"' in content)
print("orderProductDisplay:", 'id="orderProductDisplay"' in content)
print("new openOrderModal:", 'btn.dataset.product' in content)
print("updated closeOrderModal:", 'orderProductGroup' in content.split('closeOrderModal')[1][:200])
