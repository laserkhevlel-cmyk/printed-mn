import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Product mapping: line number (1-based) -> (product name in HTML, prints separated by |)
PRODUCTS = [
    (740,  'Дурсгалын медаллион',              'Лазер хэвлэл'),
    (755,  'Термо усны сав 580мл',              'Лазер хэвлэл'),
    (770,  'Термо сав 300мл — 4 өнгө',         'Лазер хэвлэл'),
    (785,  'Тэмдэглэлийн дэвтэр &amp; Бал сет','Лазер хэвлэл|UV хэвлэл|DTF хэвлэл'),
    (800,  'Тансаг үзэг хайрцагтай',           'Лазер хэвлэл'),
    (815,  'Нарийн металл үзэг',               'Лазер хэвлэл'),
    (830,  'Кабелийн SS тэмдэглэгээ',          'Лазер хэвлэл'),
    (851,  'Стейнли загвартай термо аяга',      'Лазер хэвлэл|UV хэвлэл|DTF хэвлэл'),
    (872,  'Арьсан тэмдэглэлийн дэвтэр',       'Лазер хэвлэл|UV хэвлэл|DTF хэвлэл'),
    (887,  'Арьсан хавтастай нимгэн дэвтэр',   'Лазер хэвлэл|UV хэвлэл|DTF хэвлэл'),
    (902,  'Аялалын кофены ган аяга',           'Лазер хэвлэл|UV хэвлэл'),
    (917,  'Олон үйлдэлт түлхүүрийн оосор',    'Лазер хэвлэл'),
    (932,  'Металл түлхүүрийн оосор',           'Лазер хэвлэл'),
    (946,  'Цайны шүүртэй ган усны сав',        'Лазер хэвлэл|UV хэвлэл|DTF хэвлэл'),
    (961,  'Зураг хэвлэх боломжтой ган зүүлт', 'Лазер хэвлэл'),
    (976,  'Цагаан цаасан уут',                 'UV хэвлэл|DTF хэвлэл'),
    (991,  'Хэвлэлтэй тор уут',                'UV хэвлэл|DTF хэвлэл'),
    (1006, 'Name necklace — нэрийн зүүлт',      'Лазер хэвлэл'),
]

old_btn = 'onclick="openOrderModal()">📦 Онлайн захиалга</button>'

for lineno, product, prints in PRODUCTS:
    idx = lineno - 1
    if old_btn in lines[idx]:
        new_btn = f'onclick="openOrderModal(this)" data-product="{product}" data-prints="{prints}">📦 Онлайн захиалга</button>'
        lines[idx] = lines[idx].replace(old_btn, new_btn)
        print(f"Line {lineno}: {product} ✓")
    else:
        print(f"Line {lineno}: NOT FOUND - {lines[idx][:80]}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nDone!")
