import sys
filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. CSS ──
auth_css = """
/* == Auth & Order System == */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.72);z-index:1000;display:flex;align-items:center;justify-content:center;padding:1rem;backdrop-filter:blur(6px)}
.modal-box{background:#fff;border-radius:24px;padding:2rem;width:100%;max-width:440px;max-height:90vh;overflow-y:auto;position:relative;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
.modal-box.wide{max-width:600px}
.order-modal-box{background:#fff;border-radius:24px;padding:2rem;width:100%;max-width:540px;max-height:92vh;overflow-y:auto;position:relative;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
.modal-close{position:absolute;top:1rem;right:1rem;background:none;border:none;font-size:1.4rem;cursor:pointer;color:#94a3b8;line-height:1;transition:color 0.2s}
.modal-close:hover{color:#0f172a}
.modal-title{font-size:1.25rem;font-weight:800;color:#0f172a;margin-bottom:1.5rem}
.auth-tabs{display:flex;gap:0;margin-bottom:1.5rem;border-radius:12px;overflow:hidden;border:1.5px solid #e2e8f0}
.auth-tab{flex:1;padding:10px;border:none;background:none;font-weight:700;cursor:pointer;font-size:14px;color:#64748b;transition:all 0.2s}
.auth-tab.active{background:linear-gradient(135deg,#1D4ED8,#0EA5E9);color:#fff}
.form-group{margin-bottom:1rem}
.form-label{display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:5px}
.form-input{width:100%;padding:10px 14px;border:1.5px solid #e2e8f0;border-radius:10px;font-size:14px;transition:border 0.2s;font-family:'Inter',sans-serif;box-sizing:border-box}
.form-input:focus{outline:none;border-color:#3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,0.1)}
.form-select{width:100%;padding:10px 14px;border:1.5px solid #e2e8f0;border-radius:10px;font-size:14px;background:#fff;font-family:'Inter',sans-serif;box-sizing:border-box}
textarea.form-input{resize:vertical;min-height:70px}
.btn-auth{width:100%;padding:12px;background:linear-gradient(135deg,#1D4ED8,#0EA5E9);color:#fff;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;margin-top:0.5rem;transition:opacity 0.2s}
.btn-auth:hover{opacity:0.9}
.btn-auth:disabled{opacity:0.6;cursor:not-allowed}
.auth-err{color:#ef4444;font-size:13px;margin-top:0.5rem;display:none;background:#fef2f2;padding:8px 12px;border-radius:8px}
.nav-auth-area{display:flex;align-items:center;gap:6px}
.nav-login-btn{background:rgba(255,255,255,0.15);border:1.5px solid rgba(255,255,255,0.5);color:#fff;padding:6px 16px;border-radius:20px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.2s;font-family:'Inter',sans-serif}
.nav-login-btn:hover{background:rgba(255,255,255,0.28)}
.nav-user-btn{background:rgba(255,255,255,0.15);border:1.5px solid rgba(255,255,255,0.5);color:#fff;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:700;cursor:pointer;font-family:'Inter',sans-serif;transition:all 0.2s}
.nav-logout-btn{background:rgba(255,80,80,0.18);border:1.5px solid rgba(255,100,100,0.4);color:#fff;padding:5px 12px;border-radius:16px;font-size:12px;font-weight:600;cursor:pointer;font-family:'Inter',sans-serif}
.order-btn-main{display:block;width:100%;padding:11px 24px;background:linear-gradient(135deg,#1D4ED8,#0EA5E9);color:#fff;border:none;border-radius:12px;font-size:14px;font-weight:700;cursor:pointer;margin-top:0.75rem;transition:opacity 0.2s;font-family:'Inter',sans-serif}
.order-btn-main:hover{opacity:0.9}
.orders-list{display:flex;flex-direction:column;gap:10px;margin-top:0.5rem}
.order-card{background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:14px;padding:1rem}
.order-card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;gap:8px}
.order-status{padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;white-space:nowrap}
.status-new{background:#dbeafe;color:#1D4ED8}
.status-pending{background:#fef9c3;color:#a16207}
.status-progress{background:#fef3c7;color:#d97706}
.status-ready{background:#d1fae5;color:#065f46}
.status-delivered{background:#e0e7ff;color:#4338ca}
.order-product-name{font-weight:700;font-size:14px;color:#0f172a}
.order-detail{font-size:12px;color:#64748b;margin-top:3px;line-height:1.6}
.toast{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%);background:#0f172a;color:#fff;padding:12px 24px;border-radius:14px;font-size:14px;font-weight:600;z-index:9999;opacity:0;transition:opacity 0.3s;pointer-events:none;white-space:nowrap}
.toast.show{opacity:1}
.tab-content{display:none}
.tab-content.active{display:block}
@media(max-width:640px){.modal-box,.order-modal-box{padding:1.5rem;border-radius:16px}}
"""
content = content.replace('</style>', auth_css + '</style>', 1)

# ── 2. Nav auth button ──
nav_btn = '\n  <div class="nav-auth-area" id="navAuthArea"><button class="nav-login-btn" onclick="openAuthModal()">Нэвтрэх</button></div>\n'
content = content.replace('<div class="nav-phone">', nav_btn + '  <div class="nav-phone">', 1)

# ── 3. Order button before each Facebook button ──
fb_btn = '<a href="https://www.facebook.com/profile.php?id=100063665375091" target="_blank" class="btn-primary" style="background:#1877F2;">Facebook захиалга өгөх →</a>'
order_plus_fb = '<button class="order-btn-main" onclick="openOrderModal()">📦 Онлайн захиалга өгөх</button>\n        ' + fb_btn
content = content.replace(fb_btn, order_plus_fb)

# ── 4. Modals + Script before </body> ──
modals_script = open("c:/Users/dashp/OneDrive/Desktop/website/opload/firebase_modals.html", 'r', encoding='utf-8').read()
content = content.replace('</body>', modals_script + '\n</body>', 1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
