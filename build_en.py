"""
VSKit 영어 버전 자동 생성 스크립트
실행: python build_en.py
결과: en/ 폴더에 영어 버전 HTML 파일 생성
"""

import os, re, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
EN_DIR = os.path.join(BASE, 'en')
os.makedirs(EN_DIR, exist_ok=True)

SITE_URL = 'https://vskit.wooahouse.com'
SITE_NAME = 'WooaVS'

# ── 1. 페이지별 메타 번역 ──────────────────────────────────────────────────────
PAGE_META = {
    'index.html': {
        'title': 'Best VS Code Extensions — Curated List for Developers | WooaVS',
        'desc':  'A curated collection of essential VS Code extensions by category. GitHub Copilot, GitLens, Prettier, ESLint, Error Lens and more — AI assist, themes, Git, debugging, productivity.',
        'kw':    'VS Code extensions, VSCode plugins, best VS Code extensions, GitHub Copilot, GitLens, Prettier, ESLint, VS Code themes, developer tools, code extensions',
        'og_title': 'Best VS Code Extensions — Developer Curation | WooaVS',
        'og_desc':  'Essential VS Code extensions curated by category: AI Assist, Themes, Git, Debugging, Languages, Productivity, Formatters.',
        'h1': 'VS Code Extensions Collection',
        'app_name': 'WooaVS',
    },
}

# ── 2. 공통 한국어→영어 치환 ──────────────────────────────────────────────────
COMMON = [
    # ── 내비게이션 ──
    ('>코드지원<', '>AI Assist<'),
    ('>테마<', '>Themes<'),
    ('>디버깅<', '>Debug<'),
    ('>언어팩<', '>Languages<'),
    ('>생산성<', '>Productivity<'),
    ('>포매터<', '>Formatter<'),

    # ── 히어로 ──
    ('<h1>VS Code 확장 프로그램 모음</h1>', '<h1>VS Code Extensions Collection</h1>'),
    ('개발 생산성을 극대화하는 VS Code 필수 확장만 엄선했습니다.<br>코드 지원부터 테마, Git, 디버깅까지 바로 설치하세요.',
     'Hand-picked essential VS Code extensions to maximize your productivity.<br>From AI code assist and themes to Git and debugging — install now.'),
    ('<a href="#ai-assist" class="hero-tag">🤖 코드 지원</a>', '<a href="#ai-assist" class="hero-tag">🤖 AI Assist</a>'),
    ('<a href="#themes" class="hero-tag">🎨 테마/UI</a>', '<a href="#themes" class="hero-tag">🎨 Themes/UI</a>'),
    ('<a href="#git" class="hero-tag">🌿 Git/협업</a>', '<a href="#git" class="hero-tag">🌿 Git</a>'),
    ('<a href="#debug" class="hero-tag">🐛 디버깅</a>', '<a href="#debug" class="hero-tag">🐛 Debug</a>'),
    ('<a href="#languages" class="hero-tag">💬 언어팩</a>', '<a href="#languages" class="hero-tag">💬 Languages</a>'),
    ('<a href="#productivity" class="hero-tag">⚡ 생산성</a>', '<a href="#productivity" class="hero-tag">⚡ Productivity</a>'),
    ('<a href="#formatter" class="hero-tag">✨ 포매터</a>', '<a href="#formatter" class="hero-tag">✨ Formatter</a>'),
    ('>📌 홈 화면에 추가<', '>📌 Add to Home Screen<'),

    # ── 카테고리 제목/설명 ──
    ('<h2 class="category-title">코드 지원 / AI</h2>', '<h2 class="category-title">Code Assist / AI</h2>'),
    ('<p class="category-desc">AI 자동완성, 코드 추천으로 개발 속도 향상</p>',
     '<p class="category-desc">Speed up development with AI autocomplete and code suggestions</p>'),
    ('<h2 class="category-title">테마 / UI</h2>', '<h2 class="category-title">Themes / UI</h2>'),
    ('<p class="category-desc">눈이 편한 다크테마와 아이콘 테마</p>',
     '<p class="category-desc">Dark themes and icon themes for comfortable coding</p>'),
    ('<h2 class="category-title">Git / 협업</h2>', '<h2 class="category-title">Git / Collaboration</h2>'),
    ('<p class="category-desc">Git 히스토리 시각화와 팀 협업 도구</p>',
     '<p class="category-desc">Git history visualization and team collaboration tools</p>'),
    ('<h2 class="category-title">디버깅 / 테스트</h2>', '<h2 class="category-title">Debugging / Testing</h2>'),
    ('<p class="category-desc">버그 추적과 API 테스트, 오류 시각화 도구</p>',
     '<p class="category-desc">Bug tracking, API testing, and error visualization tools</p>'),
    ('<h2 class="category-title">언어 지원</h2>', '<h2 class="category-title">Language Support</h2>'),
    ('<p class="category-desc">각 프로그래밍 언어별 문법 지원 및 LSP</p>',
     '<p class="category-desc">Syntax support and LSP for each programming language</p>'),
    ('<h2 class="category-title">생산성</h2>', '<h2 class="category-title">Productivity</h2>'),
    ('<p class="category-desc">코딩 효율을 높이는 유틸리티 확장</p>',
     '<p class="category-desc">Utility extensions to boost coding efficiency</p>'),
    ('<h2 class="category-title">포매터 / 린터</h2>', '<h2 class="category-title">Formatter / Linter</h2>'),
    ('<p class="category-desc">코드 스타일 통일과 품질 검사 도구</p>',
     '<p class="category-desc">Code style consistency and quality checking tools</p>'),

    # ── 확장 설명 (AI/코드지원) ──
    ('<div class="link-desc">AI 기반 코드 자동완성 및 코드 생성. 개발자 필수</div>',
     '<div class="link-desc">AI-powered code autocomplete and generation. A must-have for developers</div>'),
    ('<div class="link-desc">AI 코드 자동완성. 로컬 AI 모델 지원</div>',
     '<div class="link-desc">AI code autocomplete. Supports local AI models</div>'),
    ('<div class="link-desc">Microsoft AI 기반 코드 완성 및 추천</div>',
     '<div class="link-desc">Microsoft AI-powered code completion and suggestions</div>'),
    ('<div class="link-desc">파일 경로 자동완성으로 import 오류 방지</div>',
     '<div class="link-desc">File path autocomplete to prevent import errors</div>'),
    ('<div class="link-desc">TypeScript/JavaScript import 구문 자동 추가</div>',
     '<div class="link-desc">Auto-add TypeScript/JavaScript import statements</div>'),
    ('<div class="link-desc">AI와 대화하며 코드 작성·설명·디버깅</div>',
     '<div class="link-desc">Chat with AI to write, explain, and debug code</div>'),

    # ── 확장 설명 (테마) ──
    ('<div class="link-desc">VS Code 최고 인기 다크 테마. Atom 스타일</div>',
     '<div class="link-desc">The most popular VS Code dark theme. Atom style</div>'),
    ('<div class="link-desc">모든 에디터에서 인기 있는 다크 테마</div>',
     '<div class="link-desc">Popular dark theme across all editors</div>'),
    ('<div class="link-desc">파일·폴더를 직관적인 아이콘으로 표시</div>',
     '<div class="link-desc">Display files and folders with intuitive icons</div>'),
    ('<div class="link-desc">파스텔 톤의 따뜻하고 부드러운 컬러 테마</div>',
     '<div class="link-desc">Warm, soft pastel color theme</div>'),
    ('<div class="link-desc">도쿄 야경에서 영감 받은 차분한 다크 테마</div>',
     '<div class="link-desc">Calm dark theme inspired by the Tokyo night skyline</div>'),
    ('<div class="link-desc">GitHub 공식 다크/라이트 테마</div>',
     '<div class="link-desc">Official GitHub dark and light theme</div>'),

    # ── 확장 설명 (Git) ──
    ('<div class="link-desc">인라인 blame, 히스토리, 브랜치 비교 등 Git 슈퍼파워</div>',
     '<div class="link-desc">Inline blame, history, branch compare — Git supercharged</div>'),
    ('<div class="link-desc">Git 브랜치와 커밋 히스토리를 그래프로 시각화</div>',
     '<div class="link-desc">Visualize Git branches and commit history as a graph</div>'),
    ('<div class="link-desc">VS Code 내에서 PR 생성·리뷰·머지 처리</div>',
     '<div class="link-desc">Create, review, and merge PRs inside VS Code</div>'),
    ('<div class="link-desc">파일·줄 단위 Git 히스토리 탐색</div>',
     '<div class="link-desc">Browse Git history by file or line</div>'),
    ('<div class="link-desc">SSH로 원격 서버에 직접 접속해 개발</div>',
     '<div class="link-desc">Develop directly on remote servers via SSH</div>'),
    ('<div class="link-desc">실시간 코드 공유 및 페어 프로그래밍</div>',
     '<div class="link-desc">Real-time code sharing and pair programming</div>'),

    # ── 확장 설명 (디버깅) ──
    ('<div class="link-desc">오류·경고를 해당 줄 옆에 인라인으로 즉시 표시</div>',
     '<div class="link-desc">Instantly display errors and warnings inline next to the relevant line</div>'),
    ('<div class="link-desc">.http 파일로 VS Code 내에서 직접 API 테스트</div>',
     '<div class="link-desc">Test APIs directly in VS Code using .http files</div>'),
    ('<div class="link-desc">Postman 대체. VS Code 내 경량 REST API 클라이언트</div>',
     '<div class="link-desc">Postman alternative. Lightweight REST API client inside VS Code</div>'),
    ('<div class="link-desc">40+ 언어 코드를 에디터에서 바로 실행</div>',
     '<div class="link-desc">Run code in 40+ languages directly from the editor</div>'),
    ('<div class="link-desc">사이드바에서 테스트 실행·결과 확인</div>',
     '<div class="link-desc">Run tests and view results in the sidebar</div>'),
    ('<div class="link-desc">Playwright E2E 테스트를 VS Code에서 직접 실행</div>',
     '<div class="link-desc">Run Playwright E2E tests directly in VS Code</div>'),

    # ── 확장 설명 (언어) ──
    ('<div class="link-desc">Python 공식 지원. IntelliSense·디버깅·Jupyter</div>',
     '<div class="link-desc">Official Python support. IntelliSense, debugging, and Jupyter</div>'),
    ('<div class="link-desc">Go 공식 확장. 자동완성·디버깅·포매팅 지원</div>',
     '<div class="link-desc">Official Go extension. Autocomplete, debugging, and formatting</div>'),
    ('<div class="link-desc">Rust 최고의 LSP. 코드 완성·인레이 힌트·오류 표시</div>',
     '<div class="link-desc">The best Rust LSP. Code completion, inlay hints, and error display</div>'),
    ('<div class="link-desc">Microsoft C/C++ 공식 지원. IntelliSense·디버깅</div>',
     '<div class="link-desc">Official Microsoft C/C++ support. IntelliSense and debugging</div>'),
    ('<div class="link-desc">Java 개발을 위한 공식 확장 패키지</div>',
     '<div class="link-desc">Official extension pack for Java development</div>'),
    ('<div class="link-desc">C# 및 .NET 개발을 위한 공식 확장</div>',
     '<div class="link-desc">Official extension for C# and .NET development</div>'),

    # ── 확장 설명 (생산성) ──
    ('<div class="link-desc">코드 내 TODO·FIXME 주석 강조 표시</div>',
     '<div class="link-desc">Highlight TODO and FIXME comments in your code</div>'),
    ('<div class="link-desc">코드 줄에 북마크 추가 후 빠른 이동</div>',
     '<div class="link-desc">Add bookmarks to code lines and jump to them quickly</div>'),
    ('<div class="link-desc">여러 프로젝트를 쉽게 저장·전환·관리</div>',
     '<div class="link-desc">Save, switch, and manage multiple projects with ease</div>'),
    ('<div class="link-desc">주석 유형별 색상 구분으로 가독성 향상</div>',
     '<div class="link-desc">Color-coded comment types for improved readability</div>'),
    ('<div class="link-desc">코드 내 영어 철자 오류 실시간 감지</div>',
     '<div class="link-desc">Real-time English spell checking in your code</div>'),
    ('<div class="link-desc">HTML/JSX 태그 이름 변경 시 닫는 태그 자동 동기화</div>',
     '<div class="link-desc">Auto-sync closing tag when renaming HTML/JSX tags</div>'),

    # ── 확장 설명 (포매터) ──
    ('<div class="link-desc">JS·TS·CSS·HTML 등 코드 자동 포매팅. 팀 표준 필수</div>',
     '<div class="link-desc">Auto-format JS, TS, CSS, HTML and more. Essential for team standards</div>'),
    ('<div class="link-desc">JavaScript·TypeScript 코드 품질 및 스타일 검사</div>',
     '<div class="link-desc">Code quality and style checking for JavaScript and TypeScript</div>'),
    ('<div class="link-desc">CSS·SCSS·Less 스타일 코드 품질 검사</div>',
     '<div class="link-desc">Style code quality checking for CSS, SCSS, and Less</div>'),
    ('<div class="link-desc">.editorconfig 파일로 팀 간 들여쓰기·줄바꿈 통일</div>',
     '<div class="link-desc">Unify indentation and line endings across teams with .editorconfig</div>'),
    ('<div class="link-desc">Python 표준 코드 포매터 Black 공식 확장</div>',
     '<div class="link-desc">Official extension for the Black Python code formatter</div>'),
    ('<div class="link-desc">Rust로 만든 초고속 Python 린터·포매터</div>',
     '<div class="link-desc">Ultra-fast Python linter and formatter built with Rust</div>'),

    # ── 설치하기 버튼 ──
    ('<span class="link-hint">설치하기 →</span>', '<span class="link-hint">Install →</span>'),

    # ── cross-link tip ──
    ('💡 개발 리소스 링크 모음이 필요하다면? → <a href="https://wooahouse.com/#dev" target="_blank" rel="noopener">WooaHouse 개발 도구 모음 보기</a>',
     '💡 Need a developer resource hub? → <a href="https://wooahouse.com/#dev" target="_blank" rel="noopener">Explore WooaHouse Developer Tools</a>'),

    # ── SEO intro ──
    ('<h2>WooaVS — VS Code 확장 프로그램 큐레이션</h2>',
     '<h2>WooaVS — VS Code Extensions Curation</h2>'),

    # ── footer ──
    ('<p>VS Code 확장 프로그램 큐레이션 서비스.<br>직접 사용하고 검증한 확장만 수록합니다.</p>',
     '<p>A curated collection of VS Code extensions.<br>Only extensions we\'ve personally tested and verified.</p>'),
    ('<h4>WooaHouse 서비스</h4>', '<h4>WooaHouse Services</h4>'),
    ('>서비스 소개<', '>About<'),
    ('>개인정보처리방침<', '>Privacy Policy<'),
    ('>홈<', '>Home<'),
    ('© 2026 WooaVS by WooaHouse. 모든 권리 보유.',
     '© 2026 WooaVS by WooaHouse. All rights reserved.'),
    ('<p class="coupang-notice">이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>', ''),

    # ── our-sites-bar active link (en/ 기준) ──
    ('href="https://vskit.wooahouse.com/" target="_blank" rel="noopener" class="active"',
     'href="https://vskit.wooahouse.com/en/" target="_blank" rel="noopener" class="active"'),

    # ── 상대 경로 수정 (en/ 서브디렉토리) ──
    ('href="manifest.json"', 'href="../manifest.json"'),
    ('href="css/style.css"', 'href="../css/style.css"'),
    ('src="js/pwa-install.js"', 'src="../js/pwa-install.js"'),
    ('href="index.html"', 'href="../index.html"'),
    ('href="about.html"', 'href="../about.html"'),
    ('href="privacy.html"', 'href="../privacy.html"'),
]

# ── 3. 언어 선택기 CSS ────────────────────────────────────────────────────────
LANG_SWITCHER_CSS = """    .lang-switcher { display:flex; align-items:center; gap:4px; }
    .lang-switcher a { color:rgba(255,255,255,0.7); text-decoration:none; font-size:0.8rem; font-weight:600; padding:3px 8px; border-radius:12px; transition:background 0.15s; }
    .lang-switcher a.active { color:white; background:rgba(255,255,255,0.25); }
    .lang-switcher a:hover { color:white; background:rgba(255,255,255,0.18); }
    .lang-switcher span { color:rgba(255,255,255,0.3); font-size:0.75rem; }
"""

def build_page(filename, meta):
    ko_path = os.path.join(BASE, filename)
    en_path = os.path.join(EN_DIR, filename)

    with open(ko_path, encoding='utf-8') as f:
        html = f.read()

    # ── 메타 태그 교체 ──
    html = re.sub(r'<title>[^<]+</title>', f'<title>{meta["title"]}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]*"',
                  f'<meta name="description" content="{meta["desc"]}"', html)
    html = re.sub(r'<meta name="keywords" content="[^"]*"',
                  f'<meta name="keywords" content="{meta["kw"]}"', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*"',
                  f'<meta property="og:title" content="{meta["og_title"]}"', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*"',
                  f'<meta property="og:description" content="{meta["og_desc"]}"', html)
    html = re.sub(r'<meta property="og:url" content="[^"]*"',
                  f'<meta property="og:url" content="{SITE_URL}/en/{filename}"', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*"',
                  f'<link rel="canonical" href="{SITE_URL}/en/{filename}"', html)

    # ── hreflang 추가 ──
    hreflang = (f'\n  <link rel="alternate" hreflang="ko" href="{SITE_URL}/{filename}">'
                f'\n  <link rel="alternate" hreflang="en" href="{SITE_URL}/en/{filename}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/{filename}">')
    html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + hreflang, html)

    # ── ld+json 업데이트 ──
    html = re.sub(r'"name": "([^"]*[가-힣][^"]*)"', f'"name": "{meta["app_name"]}"', html)
    html = re.sub(r'"description": "([^"]*[가-힣][^"]*)"', f'"description": "{meta["desc"]}"', html)
    html = re.sub(r'"url": "' + re.escape(SITE_URL) + r'/"',
                  f'"url": "{SITE_URL}/en/{filename}"', html)
    html = re.sub(r'"inLanguage": "ko"', '"inLanguage": "en"', html)

    # ── h1 교체 ──
    if meta.get('h1'):
        replaced = re.sub(r'<h1>([^<]*)</h1>', f'<h1>{meta["h1"]}</h1>', html, count=1)
        html = replaced

    # ── 공통 문자열 치환 ──
    for ko, en in COMMON:
        html = html.replace(ko, en)

    # ── 언어 선택기 CSS 삽입 ──
    if 'lang-switcher' not in html:
        html = html.replace('  </style>', LANG_SWITCHER_CSS + '  </style>', 1)
        if 'lang-switcher' not in html:
            html = html.replace('</style>', LANG_SWITCHER_CSS + '</style>', 1)

    # ── 헤더에 언어 선택기 삽입 ──
    html = re.sub(
        r'(\s*</div>\s*</header>)',
        f'\n    <div class="header-right">\n'
        f'      <div class="lang-switcher">\n'
        f'        <a href="../{filename}">KO</a>\n'
        f'        <span>|</span>\n'
        f'        <a href="{filename}" class="active">EN</a>\n'
        f'      </div>\n'
        f'      <a href="../about.html" style="color:rgba(255,255,255,0.85); font-size:0.85rem; text-decoration:none; margin-left:8px;">About</a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</header>',
        html, count=1
    )

    # ── 쿠팡 제거 / og:locale 교체 ──
    html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
    html = re.sub(r'<script>\s*new PartnersCoupang\.G\([^)]*\);?\s*</script>', '', html)
    html = html.replace('content="ko_KR"', 'content="en_US"')

    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'  ✅ en/{filename}')


# ── 4. 실행 ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Building English pages for VSKit...')

    for filename, meta in PAGE_META.items():
        ko_path = os.path.join(BASE, filename)
        if os.path.exists(ko_path):
            build_page(filename, meta)
        else:
            print(f'  ⚠️  {filename} not found, skipping')

    # ── about.html 처리 ──
    about_src = os.path.join(BASE, 'about.html')
    about_dst = os.path.join(EN_DIR, 'about.html')
    if os.path.exists(about_src):
        with open(about_src, encoding='utf-8') as f:
            html = f.read()

        ABOUT_EXTRA = [
            (r'<title>[^<]+</title>', '<title>About WooaVS – VS Code Extensions Curation</title>'),
            (r'<meta name="description" content="[^"]*"',
             '<meta name="description" content="WooaVS is a curated collection of essential VS Code extensions. Discover the best extensions for AI assist, themes, Git, debugging, and more."'),
            (r'<link rel="canonical" href="[^"]*"',
             f'<link rel="canonical" href="{SITE_URL}/en/about.html"'),
        ]
        for pattern, repl in ABOUT_EXTRA:
            html = re.sub(pattern, repl, html)

        hreflang = (f'\n  <link rel="alternate" hreflang="ko" href="{SITE_URL}/about.html">'
                    f'\n  <link rel="alternate" hreflang="en" href="{SITE_URL}/en/about.html">'
                    f'\n  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/about.html">')
        html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + hreflang, html)

        for ko, en in COMMON:
            html = html.replace(ko, en)

        html = re.sub(
            r'(\s*</div>\s*</header>)',
            f'\n    <div class="header-right">\n'
            f'      <div class="lang-switcher">\n'
            f'        <a href="../about.html">KO</a>\n'
            f'        <span>|</span>\n'
            f'        <a href="about.html" class="active">EN</a>\n'
            f'      </div>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</header>',
            html, count=1
        )
        if 'lang-switcher' not in html:
            html = html.replace('</style>', LANG_SWITCHER_CSS + '</style>', 1)

        html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
        html = re.sub(r'<script>\s*new PartnersCoupang\.G\([^)]*\);?\s*</script>', '', html)
        html = html.replace('content="ko_KR"', 'content="en_US"')

        with open(about_dst, 'w', encoding='utf-8') as f:
            f.write(html)
        print('  ✅ en/about.html')

    # ── privacy.html 처리 ──
    privacy_src = os.path.join(BASE, 'privacy.html')
    privacy_dst = os.path.join(EN_DIR, 'privacy.html')
    if os.path.exists(privacy_src):
        with open(privacy_src, encoding='utf-8') as f:
            html = f.read()

        html = re.sub(r'<title>[^<]+</title>',
                      '<title>Privacy Policy – WooaVS</title>', html)
        html = re.sub(r'<link rel="canonical" href="[^"]*"',
                      f'<link rel="canonical" href="{SITE_URL}/en/privacy.html"', html)

        hreflang = (f'\n  <link rel="alternate" hreflang="ko" href="{SITE_URL}/privacy.html">'
                    f'\n  <link rel="alternate" hreflang="en" href="{SITE_URL}/en/privacy.html">'
                    f'\n  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/privacy.html">')
        html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + hreflang, html)

        for ko, en in COMMON:
            html = html.replace(ko, en)

        html = re.sub(
            r'(\s*</div>\s*</header>)',
            f'\n    <div class="header-right">\n'
            f'      <div class="lang-switcher">\n'
            f'        <a href="../privacy.html">KO</a>\n'
            f'        <span>|</span>\n'
            f'        <a href="privacy.html" class="active">EN</a>\n'
            f'      </div>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'</header>',
            html, count=1
        )
        if 'lang-switcher' not in html:
            html = html.replace('</style>', LANG_SWITCHER_CSS + '</style>', 1)

        html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
        html = html.replace('content="ko_KR"', 'content="en_US"')

        with open(privacy_dst, 'w', encoding='utf-8') as f:
            f.write(html)
        print('  ✅ en/privacy.html')

    print('\nDone! Check en/ folder.')
