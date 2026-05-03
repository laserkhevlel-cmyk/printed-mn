import sys, base64, re
sys.stdout.reconfigure(encoding='utf-8')

LOGO = "C:/Users/dashp/OneDrive/Desktop/website/opload/logo_white.png"
HTML = "C:/Users/dashp/OneDrive/Desktop/website/opload/index.html"

with open(LOGO, 'rb') as f:
    logo_src = "data:image/png;base64," + base64.b64encode(f.read()).decode()

with open(HTML, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the nav logo img src and replace it
# Pattern: <img src="data:image/png;base64,..." ... class="nav-logo-img"
# or similar nav logo usage
replaced = False

# Try replacing nav-logo img
pattern = r'(<img[^>]*class=["\']nav-logo-img["\'][^>]*src=["\'])data:[^"\']+(["\'])'
if re.search(pattern, content):
    content = re.sub(pattern, r'\g<1>' + logo_src + r'\g<2>', content)
    print("Nav logo (class first) replaced ✓")
    replaced = True

pattern2 = r'(<img[^>]*src=["\'])data:[^"\']+(["\'][^>]*class=["\']nav-logo-img["\'])'
if not replaced and re.search(pattern2, content):
    content = re.sub(pattern2, r'\g<1>' + logo_src + r'\g<2>', content)
    print("Nav logo (src first) replaced ✓")
    replaced = True

# Fallback: find the nav-logo area and replace any img src inside it
if not replaced:
    nav_idx = content.find('class="nav-logo"')
    if nav_idx == -1:
        nav_idx = content.find("class='nav-logo'")
    if nav_idx != -1:
        # Find img src= within next 500 chars
        chunk_end = nav_idx + 600
        src_start = content.find('src="data:', nav_idx, chunk_end)
        if src_start == -1:
            src_start = content.find("src='data:", nav_idx, chunk_end)
        if src_start != -1:
            src_start += 5  # skip src="
            src_end = content.find('"', src_start)
            if src_end == -1:
                src_end = content.find("'", src_start)
            content = content[:src_start] + logo_src + content[src_end:]
            print("Nav logo (fallback nav-logo div) replaced ✓")
            replaced = True

if not replaced:
    print("Could not find nav logo — searching for logo_transparent reference...")
    # Maybe logo is referenced differently - search for any img with logo
    idx = content.find('logo_transparent')
    print("logo_transparent at:", idx)

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone!")
