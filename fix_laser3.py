filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the laser panel start and UV panel start to extract the exact block
laser_start = content.index('    <!-- Лазер panel -->')
uv_start = content.index('\n<!-- UV panel -->')

old_laser_block = content[laser_start:uv_start]

new_laser_block = '''    <!-- Лазер panel -->
    <div class="svc-panel active" id="svc-laser">
      <div>
        <p class="svc-panel-desc">Лазер туяагаар материалын гадаргуу дээр лого, текст, дизайн сийлдэг аргачлал. Маш нарийн, удаан эдэлгээтэй, өнгө хэзээ ч бүдгэрдэггүй.</p>
        <ul class="svc-features">
          <li>Маш нарийн, өндөр нарийвчлалтай хэвлэл</li>
          <li>Өнгө бүдгэрэх, арилах явдалгүй — насан туршийн чанар</li>
          <li>Химийн бодис ашиглахгүй — гадаргуу гэмтдэггүй</li>
          <li>Нэг нэгжээс олон ширхэг хүртэл захиалах боломжтой</li>
          <li>Металл, шил, мод зэрэг хатуу материалд тохиромжтой</li>
        </ul>
        <button class="svc-view-btn" data-pfilter="laser">Лазер бүтээгдэхүүн харах →</button>
      </div>
      <div class="svc-panel-right">
        <div class="svc-panel-icon">🔆</div>
        <div class="svc-panel-title">Лазер хэвлэл</div>
        <div class="svc-panel-sub">Бүтээгдэхүүн сонговол үнэгүй хэвлэл · Өндөр нарийвчлал</div>
        <div class="svc-mat-label">Тохирох материал</div>
        <div class="svc-panel-mats">
          <span class="svc-mat">Металл</span>
          <span class="svc-mat">Шил</span>
          <span class="svc-mat">Мод</span>
          <span class="svc-mat">Арьс</span>
          <span class="svc-mat">Акрил</span>
          <span class="svc-mat">Керамик</span>
        </div>
      </div>
      <div style="grid-column:1/-1;margin-top:1.5rem;display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
        <div style="border-radius:16px;overflow:hidden;border:2px solid rgba(37,99,235,0.35);box-shadow:0 4px 20px rgba(37,99,235,0.10)">
          <img src="Laserzurag.png" alt="Лазер хэвлэлийн хэрэглээ" class="lb-img" style="width:100%;height:auto;display:block;">
        </div>
        <div style="border-radius:16px;overflow:hidden;border:2px solid rgba(37,99,235,0.35);box-shadow:0 4px 20px rgba(37,99,235,0.10)">
          <img src="laser_new.png" alt="Лазер хэвлэлийн жишээ" class="lb-img" style="width:100%;height:auto;display:block;">
        </div>
      </div>
    </div>
'''

content = content.replace(old_laser_block, new_laser_block)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("Laser panel rewritten to match UV structure.")
