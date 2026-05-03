import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = "  if(!qty||qty<1)return showErr('orderErr','Тоо ширхэг оруулна үү.');\n  if(!name||!phone)return showErr('orderErr','Нэр болон утасны дугаар оруулна үү.');"

new = "  if(!qty||qty<1)return showErr('orderErr','Тоо ширхэг оруулна үү.');\n  const _pid=Object.keys(PRODUCTS_MAP).find(k=>PRODUCTS_MAP[k]===product);\n  if(_pid&&_pid in _stockMap){const _avail=_stockMap[_pid];if(_avail===0)return showErr('orderErr','Уучлаарай, энэ бүтээгдэхүүн дууссан байна.');if(Number(qty)>_avail)return showErr('orderErr','Үлдэгдэл '+_avail+' ширхэг байна, тоогоо багасгана уу.');}\n  if(!name||!phone)return showErr('orderErr','Нэр болон утасны дугаар оруулна үү.');"

if old in content:
    content = content.replace(old, new)
    print("Stock check added to submitOrder ✓")
else:
    print("NOT FOUND — searching for nearby text...")
    idx = content.find("Тоо ширхэг оруулна үү.")
    if idx != -1:
        print(repr(content[idx-20:idx+120]))
    sys.exit(1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
