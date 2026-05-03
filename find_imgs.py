import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()
imgs = re.findall(r'src="((?!data:)[^"]+)"', content)
for img in sorted(set(imgs)):
    print(img)
