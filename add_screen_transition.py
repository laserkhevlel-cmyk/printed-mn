import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Replace detail-section CSS + old animation ──
old_css = """.detail-section{display:none}
.detail-section.open{display:block;animation:detailSlideIn 0.5s cubic-bezier(0.22,1,0.36,1) both}
@keyframes detailSlideIn{from{opacity:0;transform:translateY(-24px)}to{opacity:1;transform:translateY(0)}}"""

new_css = """.detail-section{display:none}
#detail-screen{position:fixed;top:0;left:0;width:100%;height:100%;overflow-y:auto;-webkit-overflow-scrolling:touch;background:linear-gradient(180deg,rgba(240,247,255,0.97) 0%,rgba(235,244,255,0.99) 100%);z-index:200;transform:translateX(100%);transition:transform 0.35s cubic-bezier(0.22,1,0.36,1);will-change:transform}
#detail-screen.open{transform:translateX(0)}
#detail-screen .detail-section.active-detail{display:block}"""

if old_css in content:
    content = content.replace(old_css, new_css)
    print("1. Detail section CSS updated ✓")
else:
    print("1. Detail section CSS NOT FOUND")

# ── 2. Replace detail-close button CSS with back-bar style ──
old_close_css = """.detail-close{display:flex;align-items:center;gap:8px;background:none;border:none;font-family:'Inter',sans-serif;font-size:13px;font-weight:600;color:#1D4ED8;cursor:pointer;padding:0;margin-bottom:1.5rem;letter-spacing:0.02em;transition:opacity 0.2s}
.detail-close:hover{opacity:0.7}
.detail-close::before{content:'←'}"""

new_close_css = """.detail-back-bar{position:sticky;top:0;z-index:10;background:rgba(255,255,255,0.92);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);padding:12px 16px;border-bottom:1px solid rgba(37,99,235,0.1);margin:-1.5rem -1.5rem 1.5rem}
.detail-close{display:flex;align-items:center;gap:6px;background:none;border:none;font-family:'Inter',sans-serif;font-size:15px;font-weight:700;color:#1D4ED8;cursor:pointer;padding:4px 0;letter-spacing:0.01em;transition:opacity 0.2s}
.detail-close:hover{opacity:0.7}
.detail-close::before{content:'‹';font-size:24px;line-height:1;margin-right:2px}"""

if old_close_css in content:
    content = content.replace(old_close_css, new_close_css)
    print("2. Detail close CSS updated ✓")
else:
    print("2. Detail close CSS NOT FOUND")

# ── 3. Replace JS navigation IIFE ──
old_js = """(function() {
  let activeCard = null;
  let activeDetail = null;

  // Add close button to each detail section
  document.querySelectorAll('.detail-section').forEach(section => {
    const btn = document.createElement('button');
    btn.className = 'detail-close';
    btn.textContent = 'Буцах';
    btn.addEventListener('click', () => closeDetail());
    const inner = section.querySelector('.detail-inner');
    if (inner) inner.insertBefore(btn, inner.firstChild);
  });

  function closeDetail() {
    if (activeDetail) {
      activeDetail.classList.remove('open');
      activeDetail = null;
    }
    if (activeCard) {
      activeCard.classList.remove('active');
      activeCard = null;
    }
  }

  function openDetail(card, targetId) {
    const target = document.getElementById(targetId);
    if (!target) return;

    // Close previous
    if (activeDetail && activeDetail !== target) {
      activeDetail.classList.remove('open');
      if (activeCard) activeCard.classList.remove('active');
    }

    // Toggle: same card clicked again → close
    if (activeDetail === target) {
      closeDetail();
      return;
    }

    activeCard = card;
    activeDetail = target;
    card.classList.add('active');
    target.classList.add('open');

    // Scroll to detail section smoothly
    setTimeout(() => {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 60);
  }

  document.querySelectorAll('a.card[href^="#"]').forEach(card => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = card.getAttribute('href').slice(1);
      openDetail(card, targetId);
    });
  });
})();"""

new_js = """(function() {
  const screen = document.getElementById('detail-screen');

  // Move all detail-sections into the overlay and add back buttons
  document.querySelectorAll('.detail-section').forEach(section => {
    screen.appendChild(section);
    const bar = document.createElement('div');
    bar.className = 'detail-back-bar';
    const btn = document.createElement('button');
    btn.className = 'detail-close';
    btn.textContent = ' Буцах';
    btn.addEventListener('click', () => closeDetail());
    bar.appendChild(btn);
    const inner = section.querySelector('.detail-inner');
    if (inner) inner.insertBefore(bar, inner.firstChild);
  });

  let activeCard = null;
  let activeDetail = null;

  function closeDetail() {
    screen.classList.remove('open');
    screen.addEventListener('transitionend', function h() {
      screen.removeEventListener('transitionend', h);
      if (activeDetail) { activeDetail.classList.remove('active-detail'); activeDetail = null; }
    });
    if (activeCard) { activeCard.classList.remove('active'); activeCard = null; }
    screen.scrollTop = 0;
  }

  function openDetail(card, targetId) {
    const target = document.getElementById(targetId);
    if (!target) return;
    if (activeDetail) activeDetail.classList.remove('active-detail');
    if (activeCard) activeCard.classList.remove('active');
    activeCard = card;
    activeDetail = target;
    card.classList.add('active');
    target.classList.add('active-detail');
    screen.scrollTop = 0;
    screen.classList.add('open');
    history.pushState({ detail: targetId }, '');
  }

  // Android hardware back button + browser back
  window.addEventListener('popstate', () => {
    if (screen.classList.contains('open')) closeDetail();
  });

  document.querySelectorAll('a.card[href^="#"]').forEach(card => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = card.getAttribute('href').slice(1);
      openDetail(card, targetId);
    });
  });
})();"""

if old_js in content:
    content = content.replace(old_js, new_js)
    print("3. Navigation JS updated ✓")
else:
    print("3. Navigation JS NOT FOUND")

# ── 4. Add #detail-screen div before </body> ──
if '<div id="detail-screen">' not in content:
    content = content.replace('</body>', '<div id="detail-screen"></div>\n</body>', 1)
    print("4. #detail-screen div added ✓")
else:
    print("4. #detail-screen div already exists")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("\nDone!")
