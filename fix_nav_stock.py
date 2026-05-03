import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'area.innerHTML=\'<button class="nav-user-btn" onclick="openOrdersModal()">\\u{1F464} \'+name+(isAdmin?\' ⭐\':\'\')+\'</button><button class="nav-logout-btn" onclick="doLogout()">Гарах</button>\';'

new = 'area.innerHTML=\'<button class="nav-user-btn" onclick="openOrdersModal()">\\u{1F464} \'+name+(isAdmin?\' ⭐\':\'\')+\'</button>\'+(isAdmin?\'<button class="nav-user-btn" onclick="openStockModal()" style="font-size:12px;padding:6px 10px">📦 Үлдэгдэл</button>\':\'\')+\'<button class="nav-logout-btn" onclick="doLogout()">Гарах</button>\';'

if old in content:
    content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Nav updated!")
else:
    print("NOT FOUND, searching...")
    idx = content.find('openOrdersModal()')
    print(repr(content[idx-20:idx+200]))
