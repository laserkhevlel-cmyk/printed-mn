import sys
sys.stdout.reconfigure(encoding='utf-8')

HTML = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Fix broken saveAllStock function ──────────────────────────────────────
# The JS was accidentally inserted inside saveAllStock, breaking:
#   await Promise.all(updates);
#   await            <-- broken (await with no expression)
#   // ── Product content editing ...
#   ...
#   loadStockData();
#     showToast('Бүгд хадгалагдлаа ✓');
# };
#
# Fix: restore saveAllStock ending correctly and remove the dangling loadStockData + showToast

broken_end = """  await Promise.all(updates);
  await \n// ── Product content editing"""
fixed_end = """  await Promise.all(updates);
// ── Product content editing"""

if broken_end in content:
    content = content.replace(broken_end, fixed_end, 1)
    print("1a. Broken 'await' fixed ✓")
else:
    print("1a. Broken await pattern not found — checking alternative...")
    # Try without \n
    alt = "  await Promise.all(updates);\n  await \n// ── Product content editing"
    if alt in content:
        content = content.replace(alt, "  await Promise.all(updates);\n// ── Product content editing", 1)
        print("1a. Broken 'await' fixed (alt) ✓")
    else:
        print("1a. Could not find broken pattern")

# Fix the dangling loadStockData(); showToast at end (after closing })
broken_tail = """\nloadStockData();\n  showToast('Бүгд хадгалагдлаа ✓');\n};"""
fixed_tail  = """\n};"""

if broken_tail in content:
    content = content.replace(broken_tail, fixed_tail, 1)
    print("1b. Dangling loadStockData/showToast removed ✓")
else:
    print("1b. Dangling tail not found")

# ── 2. Add missing prodEditModal HTML div ─────────────────────────────────────
modal_html = """
<div id="prodEditModal" onclick="if(event.target===this)closeProdEdit()">
  <div id="prodEditBox">
    <button class="modal-close" onclick="closeProdEdit()" style="position:absolute;top:1rem;right:1rem">&#x2715;</button>
    <h3>&#x270E; Бүтээгдэхүүний мэдээлэл засах</h3>
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

if 'id="prodEditModal"' not in content:
    # Insert before <!-- Auth Modal -->
    anchor = '<!-- Auth Modal -->'
    if anchor in content:
        content = content.replace(anchor, modal_html + '\n' + anchor, 1)
        print("2. prodEditModal HTML added ✓")
    else:
        print("2. Auth Modal anchor not found")
else:
    print("2. prodEditModal div already exists ✓")

# ── 3. Verify loadProductContent and addProdEditButtons are called after auth ──
old_auth = "if(Object.keys(_stockMap).length)displayStockBadges({..._stockMap});"
new_auth = "if(Object.keys(_stockMap).length)displayStockBadges({..._stockMap});\n  loadProductContent();\n  addProdEditButtons();"
if 'loadProductContent()' not in content:
    if old_auth in content:
        content = content.replace(old_auth, new_auth, 1)
        print("3. Auth hook added ✓")
    else:
        print("3. Auth hook anchor not found")
else:
    print("3. Auth hook already exists ✓")

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone!")
