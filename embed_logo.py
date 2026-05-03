import sys, base64, re
sys.stdout.reconfigure(encoding='utf-8')

LOGO = "C:/Users/dashp/OneDrive/Desktop/website/opload/logo.png"
HTML = "C:/Users/dashp/OneDrive/Desktop/website/opload/index.html"

with open(LOGO, 'rb') as f:
    logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode()

with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the nav logo img src (currently references logo_transparent.png file)
old = 'src="logo_transparent.png"'
new = f'src="{logo_b64}"'

if old in content:
    content = content.replace(old, new, 1)
    print("Logo embedded as base64 ✓")
else:
    print("logo_transparent.png reference not found")

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
