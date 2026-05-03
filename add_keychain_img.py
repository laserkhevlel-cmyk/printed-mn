import sys, base64, re
sys.stdout.reconfigure(encoding='utf-8')

with open("C:/Users/dashp/OneDrive/Desktop/website/deploy/keychain.jpg", "rb") as f:
    new_b64 = base64.b64encode(f.read()).decode('ascii')
new_src = f'data:image/jpeg;base64,{new_b64}'

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find keychain-opener section
idx = content.find('id="keychain-opener"')
if idx == -1:
    print("NOT FOUND"); exit()

# Find gallery-one div inside this section
g_start = content.find('<div class="gallery gallery-one">', idx)
g_end = content.find('</div>', g_start) + 6  # closes gallery-img div
g_end2 = content.find('</div>', g_end) + 6    # closes gallery-one div

old_gallery = content[g_start:g_end2]
print("Old block found:", old_gallery[:100].replace('\n','\\n'))

# Build new block with two images
new_gallery = old_gallery.replace(
    '<div class="gallery gallery-one">',
    '<div class="gallery gallery-two">'
)
# Insert second image before closing </div> of gallery
insert_pos = new_gallery.rfind('</div>')
new_gallery = (new_gallery[:insert_pos]
    + f'\n        <div class="gallery-img"><img src="{new_src}" style="width:100%;height:100%;object-fit:contain;padding:8px"></div>\n      '
    + new_gallery[insert_pos:])

content = content[:g_start] + new_gallery + content[g_end2:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done! gallery-two + new image added ✓")
