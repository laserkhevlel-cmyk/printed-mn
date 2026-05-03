import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Map data-product value -> product ID
PRODUCT_MAP = {
    'Дурсгалын медаллион':              'medallion',
    'Термо усны сав 580мл':              'bottle580',
    'Термо сав 300мл — 4 өнгө':         'bottle300',
    'Тэмдэглэлийн дэвтэр &amp; Бал сет':'notebook',
    'Тансаг үзэг хайрцагтай':           'pen-luxury',
    'Нарийн металл үзэг':               'pen-slim',
    'Кабелийн SS тэмдэглэгээ':          'cable-tag',
    'Стейнли загвартай термо аяга':      'stanley',
    'Арьсан тэмдэглэлийн дэвтэр':       'notebook2',
    'Арьсан хавтастай нимгэн дэвтэр':   'notebook3',
    'Аялалын кофены ган аяга':           'coffee-cup',
    'Олон үйлдэлт түлхүүрийн оосор':    'keychain-opener',
    'Металл түлхүүрийн оосор':           'keychain-plain',
    'Цайны шүүртэй ган усны сав':        'vacuum-bottle',
    'Зураг хэвлэх боломжтой ган зүүлт': 'dogtag',
    'Цагаан цаасан уут':                 'paper-bag',
    'Хэвлэлтэй тор уут':                'tor-bag',
    'Name necklace — нэрийн зүүлт':      'name-necklace',
}

inserted = 0
i = 0
while i < len(lines):
    line = lines[i]
    if 'order-btns-wrap' in line and 'data-product=' in line:
        # Extract product name from data-product="..."
        pid = None
        for pname, pid_val in PRODUCT_MAP.items():
            if f'data-product="{pname}"' in line:
                pid = pid_val
                break
        if pid:
            # Check if ds_ div not already added on previous line
            prev = lines[i-1] if i > 0 else ''
            if f'id="ds_{pid}"' not in prev:
                indent = line[:len(line) - len(line.lstrip())]
                ds_line = f'{indent}<div id="ds_{pid}" class="detail-stock-wrap"></div>\n'
                lines.insert(i, ds_line)
                print(f"Added ds_{pid} before line {i+2}")
                inserted += 1
                i += 1  # skip inserted line
    i += 1

print(f"\nTotal inserted: {inserted}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Done!")
