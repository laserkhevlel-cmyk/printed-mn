import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# The stock JS block to move
stock_start = '\nconst PRODUCTS_MAP = {'
stock_end = "document.addEventListener('DOMContentLoaded', loadStockData);\n"

idx_start = content.find(stock_start)
idx_end = content.find(stock_end) + len(stock_end)

if idx_start == -1 or idx_end == -1:
    print("ERROR: stock JS not found")
    exit(1)

stock_js_block = content[idx_start:idx_end]
print(f"Found stock JS: {len(stock_js_block)} chars")
print("Starts with:", repr(stock_js_block[:50]))
print("Ends with:", repr(stock_js_block[-50:]))

# Remove from wrong location
content = content[:idx_start] + content[idx_end:]

# Find the LAST </script> (Firebase module) and insert before it
# The Firebase module script closes last
last_script_idx = content.rfind('</script>')
if last_script_idx == -1:
    print("ERROR: no closing script tag")
    exit(1)

# Change DOMContentLoaded to direct call (modules defer, so DOMContentLoaded never fires)
stock_js_fixed = stock_js_block.replace(
    "document.addEventListener('DOMContentLoaded', loadStockData);",
    "loadStockData();"
)

content = content[:last_script_idx] + stock_js_fixed + '\n</script>' + content[last_script_idx+len('</script>'):]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    check = f.read()

# Find which script has PRODUCTS_MAP now
parts = check.split('</script>')
for i, part in enumerate(parts[:-1]):
    if 'PRODUCTS_MAP' in part:
        print(f"PRODUCTS_MAP is in script #{i+1}")
    if 'updateDoc' in part:
        print(f"Firebase module is script #{i+1}")

print("loadStockData() direct call:", 'loadStockData();' in check)
print("DOMContentLoaded removed:", "addEventListener('DOMContentLoaded'" not in check)
print("Done!")
