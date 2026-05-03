

const firebaseConfig={apiKey:"AIzaSyADB2Te34_TR4oUHkz6fQi8guQ_j4GlxEs",authDomain:"printedmn.firebaseapp.com",projectId:"printedmn",storageBucket:"printedmn.firebasestorage.app",messagingSenderId:"538204036165",appId:"1:538204036165:web:c81cff434d4a191f8e972c",measurementId:"G-E8EE9ZD51S"};
const ADMIN_EMAIL="dashpurev.sh@gmail.com";
const app=initializeApp(firebaseConfig);
const auth=getAuth(app);
const db=getFirestore(app);
let currentUser=null;

onAuthStateChanged(auth,user=>{currentUser=user;updateNavUI(user);if(Object.keys(_stockMap).length)displayStockBadges({..._stockMap});});

function updateNavUI(user){
  const area=document.getElementById('navAuthArea');
  if(!area)return;
  if(user){
    const isAdmin=user.email===ADMIN_EMAIL;
    const name=user.displayName||user.email.split('@')[0];
    area.innerHTML='<button class="nav-user-btn" onclick="openOrdersModal()">\u{1F464} '+name+(isAdmin?' ⭐':'')+'</button>'+(isAdmin?'<button class="nav-user-btn" onclick="openStockModal()" style="font-size:12px;padding:6px 10px">📦 Үлдэгдэл</button>':'')+'<button class="nav-logout-btn" onclick="doLogout()">Гарах</button>';
  }else{
    area.innerHTML='<button class="nav-login-btn" onclick="openAuthModal()">Нэвтрэх</button>';
  }
}

window.openAuthModal=()=>{document.getElementById('authModal').style.display='flex';};
window.closeAuthModal=()=>{document.getElementById('authModal').style.display='none';clearErrors();};
window.openOrderModal=(btn)=>{
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
};
window.closeOrderModal=()=>{document.getElementById('orderModal').style.display='none';document.getElementById('orderProductGroup').style.display='';document.getElementById('orderProductDisplay').style.display='none';document.getElementById('orderProduct').value='';};
window.openOrdersModal=async()=>{
  if(!currentUser){openAuthModal();return;}
  const isAdmin=currentUser.email===ADMIN_EMAIL;
  document.getElementById('ordersModalTitle').textContent=isAdmin?'⭐ Бүх захиалгууд':'\u{1F4CB} Миний захиалгууд';
  document.getElementById('ordersModal').style.display='flex';
  await loadOrders();
};
window.closeOrdersModal=()=>{document.getElementById('ordersModal').style.display='none';};
window.switchAuthTab=(tab)=>{
  document.querySelectorAll('.auth-tab').forEach((t,i)=>t.classList.toggle('active',(tab==='login'&&i===0)||(tab==='register'&&i===1)));
  document.getElementById('loginTab').classList.toggle('active',tab==='login');
  document.getElementById('registerTab').classList.toggle('active',tab==='register');
  clearErrors();
};
window.toggleAddress=()=>{document.getElementById('addressGroup').style.display=document.getElementById('orderDelivery').value==='delivery'?'block':'none';};

function clearErrors(){['loginErr','regErr','orderErr'].forEach(id=>{const el=document.getElementById(id);if(el){el.style.display='none';el.textContent='';}});}
function showErr(id,msg){const el=document.getElementById(id);if(el){el.textContent=msg;el.style.display='block';}}
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3500);}
window.showToast=showToast;

window.doRegister=async()=>{
  const name=document.getElementById('regName').value.trim();
  const phone=document.getElementById('regPhone').value.trim();
  const email=document.getElementById('regEmail').value.trim();
  const pass=document.getElementById('regPassword').value;
  if(!name||!phone||!email||!pass)return showErr('regErr','Бүх талбарыг бөглөнө үү.');
  if(pass.length<6)return showErr('regErr','Нууц үг дор хаяж 6 тэмдэгт байна.');
  const btn=document.querySelector('#registerTab .btn-auth');
  try{
    btn.disabled=true;btn.textContent='Бүртгэж байна...';
    const cred=await createUserWithEmailAndPassword(auth,email,pass);
    await updateProfile(cred.user,{displayName:name,photoURL:phone});
    closeAuthModal();showToast('Бүртгэл амжилттай! Тавтай морилно үү \u{1F389}');
  }catch(e){
    const msgs={'auth/email-already-in-use':'Энэ имэйл бүртгэлтэй байна.','auth/invalid-email':'Имэйл буруу байна.','auth/weak-password':'Нууц үг хэтэрхий энгийн.'};
    showErr('regErr',msgs[e.code]||'Алдаа гарлаа. Дахин оролдоно үү.');
  }finally{btn.disabled=false;btn.textContent='Бүртгүүлэх';}
};

window.doLogin=async()=>{
  const email=document.getElementById('loginEmail').value.trim();
  const pass=document.getElementById('loginPassword').value;
  if(!email||!pass)return showErr('loginErr','Имэйл болон нууц үгийг бөглөнө үү.');
  const btn=document.querySelector('#loginTab .btn-auth');
  try{
    btn.disabled=true;btn.textContent='Нэвтэрч байна...';
    await signInWithEmailAndPassword(auth,email,pass);
    closeAuthModal();showToast('Амжилттай нэвтэрлээ!');
  }catch(e){
    const msgs={'auth/user-not-found':'Хэрэглэгч олдсонгүй.','auth/wrong-password':'Нууц үг буруу.','auth/invalid-credential':'Имэйл эсвэл нууц үг буруу.','auth/too-many-requests':'Хэт олон оролдлого. Түр хүлээнэ үү.'};
    showErr('loginErr',msgs[e.code]||'Нэвтрэх амжилтгүй боллоо.');
  }finally{btn.disabled=false;btn.textContent='Нэвтрэх';}
};

window.doLogout=async()=>{await signOut(auth);showToast('Гарлаа.');};

window.submitOrder=async()=>{
  if(!currentUser)return;
  const product=document.getElementById('orderProduct').value;
  const printType=document.getElementById('orderPrintType').value;
  const qty=document.getElementById('orderQty').value;
  const variant=document.getElementById('orderVariant').value;
  const design=document.getElementById('orderDesign').value.trim();
  const note=document.getElementById('orderNote').value.trim();
  const delivery=document.getElementById('orderDelivery').value;
  const address=document.getElementById('orderAddress').value.trim();
  const name=document.getElementById('orderName').value.trim();
  const phone=document.getElementById('orderPhone').value.trim();
  if(!product)return showErr('orderErr','Бүтээгдэхүүн сонгоно үү.');
  if(!printType)return showErr('orderErr','Хэвлэлийн төрөл сонгоно үү.');
  if(!qty||qty<1)return showErr('orderErr','Тоо ширхэг оруулна үү.');
  if(!name||!phone)return showErr('orderErr','Нэр болон утасны дугаар оруулна үү.');
  if(delivery==='delivery'&&!address)return showErr('orderErr','Хүргэлтийн хаяг оруулна үү.');
  const btn=document.querySelector('#orderModal .btn-auth');
  try{
    btn.disabled=true;btn.textContent='Илгээж байна...';
    await addDoc(collection(db,'orders'),{userId:currentUser.uid,userEmail:currentUser.email,userName:name,userPhone:phone,product,printType,qty:Number(qty),variant,design,note,delivery,address,status:'new',createdAt:serverTimestamp()});
    closeOrderModal();
    showToast('Захиалга амжилттай илгээгдлээ! Бид тантай холбогдоно \u{1F389}');
    ['orderProduct','orderPrintType','orderVariant','orderDesign','orderNote','orderAddress'].forEach(id=>{const el=document.getElementById(id);if(el)el.value='';});
    document.getElementById('orderQty').value=1;
  }catch(e){showErr('orderErr','Алдаа: '+e.message);}
  finally{btn.disabled=false;btn.textContent='✓ Захиалга илгээх';}
};

async function loadOrders(){
  const list=document.getElementById('ordersList');
  list.innerHTML='<div style="text-align:center;color:#94a3b8;padding:2rem">Уншиж байна...</div>';
  try{
    const isAdmin=currentUser.email===ADMIN_EMAIL;
    const q=isAdmin?query(collection(db,'orders'),orderBy('createdAt','desc')):query(collection(db,'orders'),where('userId','==',currentUser.uid),orderBy('createdAt','desc'));
    const snap=await getDocs(q);
    if(snap.empty){list.innerHTML='<div style="text-align:center;color:#94a3b8;padding:2rem">Захиалга байхгүй байна.</div>';return;}
    const sm={new:'Шинэ',pending:'Хүлээгдэж байна',progress:'Хийгдэж байна',ready:'Бэлэн',delivered:'Хүргэгдсэн'};
    const sc={new:'status-new',pending:'status-pending',progress:'status-progress',ready:'status-ready',delivered:'status-delivered'};
    list.innerHTML=snap.docs.map(d=>{
      const o=d.data();
      const date=o.createdAt?new Date(o.createdAt.toDate()).toLocaleDateString('mn-MN'):'--';
      const opts=Object.entries(sm).map(([k,v])=>'<option value="'+k+'"'+(o.status===k?' selected':'')+'>'+v+'</option>').join('');
      const adminCtrl=isAdmin?'<div style="margin-top:8px;display:flex;align-items:center;gap:8px"><select onchange="updateOrderStatus(\''+d.id+'\',this.value)" style="padding:4px 8px;border-radius:8px;border:1px solid #e2e8f0;font-size:12px">'+opts+'</select><span style="font-size:11px;color:#94a3b8">'+o.userEmail+'</span></div>':'';
      const delivText=o.delivery==='delivery'?'Хүргэлт: '+(o.address||''):'Очиж авна';
      return '<div class="order-card"><div class="order-card-header"><span class="order-product-name">'+o.product+'</span><span class="order-status '+(sc[o.status]||'status-new')+'">'+(sm[o.status]||'Шинэ')+'</span></div><div class="order-detail">🖨 '+o.printType+' · '+o.qty+' ширхэг'+(o.variant?' · '+o.variant:'')+'</div>'+(o.design?'<div class="order-detail">🎨 '+o.design+'</div>':'')+'<div class="order-detail">📅 '+date+' · '+delivText+' · 📞 '+(o.userPhone||'')+'</div>'+(o.note?'<div class="order-detail">📝 '+o.note+'</div>':'')+adminCtrl+'</div>';
    }).join('');
  }catch(e){list.innerHTML='<div style="color:#ef4444;padding:1rem">Алдаа: '+e.message+'</div>';}
}

window.updateOrderStatus=async(id,status)=>{
  try{await updateDoc(doc(db,'orders',id),{status});showToast('Төлөв шинэчлэгдлээ.');}
  catch(e){showToast('Алдаа: '+e.message);}
};

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
  const isAdm = currentUser && currentUser.email === ADMIN_EMAIL;
  // Card grid badges
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
  // Detail page stock displays
  Object.keys(PRODUCTS_MAP).forEach(id => {
    const el = document.getElementById('ds_' + id);
    if(!el) return;
    if(!(id in stockMap)) { el.innerHTML = ''; return; }
    const qty = stockMap[id];
    const cls = qty === 0 ? 'stock-out' : qty <= 5 ? 'stock-low' : 'stock-ok';
    const txt = qty === 0 ? '⛔ Дууссан' : qty <= 5 ? '⚠️ Үлдэгдэл: '+qty : '✅ Байна: '+qty;
    el.innerHTML = '<span class="detail-stock-info '+cls+'">'+txt+'</span>'
      +(isAdm ? '<button class="detail-stock-edit" data-sid="'+id+'" data-qty="'+qty+'" onclick="editDetailStock(this.dataset.sid,this.dataset.qty)">✎ Засах</button>' : '');
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
    const qty = (map[id] !== undefined) ? map[id] : '';
    return `<div class="stock-item"><span class="stock-item-name" title="${name}">${name}</span><input class="stock-input" type="number" min="0" id="sq_${id}" value="${qty}" placeholder="0"><button class="stock-save-btn" data-sid="${id}" onclick="saveStock(this.dataset.sid)">✓</button></div>`;
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
  await 
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
  showToast('Бүгд хадгалагдлаа ✓');
};

loadStockData();

