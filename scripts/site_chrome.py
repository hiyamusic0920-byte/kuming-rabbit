#!/usr/bin/env python3
"""全站共用的 head / header / footer。

這個網站沒有 build step（GitHub Pages 直接吃靜態檔），所以「共用版面」只能靠
產生時注入。所有頁面的 header / footer 都由這裡產出，再用 apply_chrome.py 寫進
各頁的標記區塊之間，避免 26 頁各自手改而漂移。

頁面裡的標記長這樣，內容會被整段換掉：
    <!-- CHROME:HEADER -->  ...  <!-- /CHROME:HEADER -->
    <!-- CHROME:FOOTER -->  ...  <!-- /CHROME:FOOTER -->
    <!-- CHROME:NAVJS -->   ...  <!-- /CHROME:NAVJS -->
"""

SITE_NAME = "苦命兔 Kuming Rabbit — AI QA Lab"
BASE_URL = "https://hiyamusic0920-byte.github.io/kuming-rabbit/"

# 主導覽四項，加一項次要項（Things AI Got Wrong 不進主層級，靠 hero CTA 與 footer 到達）
NAV = [
    ("ai-qa", "ai-qa.html", "AI QA", False),
    ("case-studies", "case-studies.html", "Case Studies", False),
    ("diary", "diary.html", "QA Diary", False),
    ("about", "about.html", "About", False),
    ("lessons", "lessons.html", "Things AI Got Wrong", True),
]

FOOTER_LINKS = [
    ("ai-qa.html", "AI QA"),
    ("case-studies.html", "Case Studies"),
    ("diary.html", "QA Diary"),
    ("about.html", "About"),
    ("lessons.html", "Things AI Got Wrong"),
]


def _p(depth: int, href: str) -> str:
    """把站內連結補上回到根目錄的相對路徑（portfolio/ 在下一層）。"""
    if href.startswith(("http", "#", "mailto:")):
        return href
    return "../" * depth + href


def head(
    title: str,
    description: str,
    url_path: str,
    *,
    depth: int = 0,
    og_title: str | None = None,
    og_description: str | None = None,
    og_image: str = "assets/og-image.jpg",
    og_image_alt: str = "苦命兔睡著了，旁邊的終端機一直印 sleep()，估計還要跑 14 小時 23 分。",
    og_type: str = "website",
    extra: str = "",
) -> str:
    """<head> 內容。description 一定要傳——Phase 1 的 SEO 底線是每頁都有。"""
    fonts = (
        "https://fonts.googleapis.com/css2?"
        "family=Archivo:wght@400..800"
        "&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400"
        "&family=Noto+Serif+TC:wght@400;600;700"
        "&family=JetBrains+Mono:wght@400;500;700&display=swap"
    )
    return f"""  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>{title}</title>
  <meta name="description" content="{description}">

  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{og_title or title}">
  <meta property="og:description" content="{og_description or description}">
  <meta property="og:url" content="{BASE_URL}{url_path}">
  <meta property="og:image" content="{BASE_URL}{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{og_image_alt}">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{fonts}">
  <link rel="stylesheet" href="{_p(depth, 'styles.css')}">
{extra}"""


def skip_link() -> str:
    return '<a class="skip-link" href="#main">跳到主要內容</a>'


def header(active: str = "", depth: int = 0) -> str:
    items = []
    for key, href, label, secondary in NAV:
        cls = ' class="nav-secondary"' if secondary else ""
        cur = ' aria-current="page"' if key == active else ""
        items.append(f'        <li{cls}><a href="{_p(depth, href)}"{cur}>{label}</a></li>')
    nav_items = "\n".join(items)
    return f"""<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="{_p(depth, 'index.html')}">
      <span class="brand-mark" aria-hidden="true">🐰</span>
      <span class="brand-text">
        <span class="brand-name">苦命兔 Kuming Rabbit</span>
        <span class="brand-role">AI QA Lab</span>
      </span>
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="開啟主導覽">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M3 6h18M3 12h18M3 18h18"></path>
      </svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
        <path d="M5 5l14 14M19 5L5 19"></path>
      </svg>
    </button>

    <nav class="site-nav" id="site-nav" aria-label="主導覽">
      <ul>
{nav_items}
      </ul>
    </nav>
  </div>
</header>"""


def footer(depth: int = 0) -> str:
    links = "\n".join(
        f'      <li><a href="{_p(depth, href)}">{label}</a></li>'
        for href, label in FOOTER_LINKS
    )
    return f"""<footer class="site-footer">
  <div class="site-footer-inner">
    <div>
      <p class="footer-brand">苦命兔 Kuming Rabbit · AI QA Lab</p>
      <p class="footer-tagline">一個 QA 把兩個 AI agent 放進真實測試流程的實驗紀錄。</p>
    </div>
    <ul class="footer-links">
{links}
      <li><a href="https://github.com/hiyamusic0920-byte/kuming-rabbit">GitHub</a></li>
    </ul>
    <p class="footer-meta">Sunny · QA Engineer / AI Native QA Explorer</p>
  </div>
</footer>"""


def nav_js() -> str:
    return """<script>
  // 手機漢堡選單。展開後焦點進選單、Esc 關閉並把焦點還給觸發按鈕。
  (function () {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.getElementById('site-nav');
    if (!toggle || !nav) return;

    function setOpen(open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? '關閉主導覽' : '開啟主導覽');
      nav.setAttribute('data-open', String(open));
    }

    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      setOpen(!open);
      if (!open) {
        var first = nav.querySelector('a');
        if (first) first.focus();
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      if (toggle.getAttribute('aria-expanded') !== 'true') return;
      setOpen(false);
      toggle.focus();
    });

    // 從手機寬度放大到桌機時，把展開狀態收掉，避免桌機殘留 data-open
    var wide = window.matchMedia('(min-width: 900px)');
    wide.addEventListener('change', function (e) {
      if (e.matches) setOpen(false);
    });
  })();
</script>"""
