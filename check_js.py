import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/dashp/OneDrive/Desktop/website/opload/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('<script type="module">')
module = parts[-1].split('</script>')[0]
lines = module.split('\n')
print('Module lines:', len(lines))

# Find lines with non-escaped '' adjacent to +
bad = []
for i, line in enumerate(lines):
    # Match '' that is not preceded by backslash
    for m in re.finditer(r"(?<!\\)''", line):
        ctx = line[max(0,m.start()-3):m.end()+3]
        if '+' in ctx:
            bad.append((i+1, line[:200]))
            break

if bad:
    print(f"\nFound {len(bad)} potentially broken lines:")
    for lineno, text in bad:
        print(f"  Line {lineno}: {repr(text)}")
else:
    print("\nNo broken '' patterns found!")
    print("Checking for other issues...")
    # Check for unclosed template literals or syntax errors
    for i, line in enumerate(lines):
        backticks = line.count('`')
        if backticks % 2 != 0:
            print(f"  Odd backtick count line {i+1}: {repr(line[:100])}")
