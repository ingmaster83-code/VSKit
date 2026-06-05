"""
WooaVS(VSKit) KO 페이지 메타 디스크립션 CTR 최적화
- 키워드: "vs코드 확장"(5·20%) / "vs code 필수 확장"(6·0%) / "vs코드 테마"(5·0%)
          "playwright 설치"(3·0%) / "gitlens 로그인 필수?"(2·0%)
- 공통 변환: "VS Code 확장 프로그램 설치." → "vs코드 확장 설치 가이드 —"
             "WooaVS 엄선 필수 VS Code 확장." → "vs코드 필수 확장, 설치 방법 안내."
- 테마: suffix → "vs코드 테마 추천, 설치 방법 안내."
- 특별: playwright / gitlens 개별 최적화
"""
import re, os, glob

BASE = 'C:/개인/wooahouse/VSKit'

# ── 테마 파일 (suffix 별도 처리) ──────────────────────────────────────
THEME_FILES = {
    'dracula', 'tokyo-night', 'catppuccin', 'github-theme',
    'night-owl', 'one-dark-pro',
}

# ── 개별 완전 교체 (description 전체 지정) ───────────────────────────
INDIVIDUAL = {
    # playwright 설치(3) + vs code에 playwright 설치(2) = 5 노출
    'extensions/playwright.html': (
        'Playwright Test VS Code 확장 프로그램 설치.',
        'Playwright VS Code 확장 설치 가이드 — vs code에 playwright 설치, E2E 테스트를 에디터에서 직접 실행. vs코드 필수 확장, 설치·사용법 안내.'
    ),
    # gitlens 로그인 필수?(2) + vs code git lens(2) = 4 노출
    'extensions/gitlens.html': (
        'GitLens VS Code 확장 프로그램 설치.',
        'GitLens VS Code 확장 설치 가이드 — 인라인 blame·히스토리·브랜치 비교 등 Git 슈퍼파워. 무료 버전으로 로그인 불필요, vs코드 필수 Git 확장 설치 방법 안내.'
    ),
    # indent rainbow 100% CTR이지만 보강
    'extensions/indent-rainbow.html': (
        'indent-rainbow VS Code 확장 프로그램 설치.',
        'indent-rainbow VS Code 확장 설치 가이드 — 들여쓰기를 무지개 색상으로 구분해 가독성 향상. vs code indent rainbow 설치 방법, vs코드 필수 확장 안내.'
    ),
    # c# dev kit 설치 100% CTR이지만 보강
    'extensions/csharp.html': (
        'C# Dev Kit VS Code 확장 프로그램 설치.',
        'C# Dev Kit VS Code 확장 설치 가이드 — C# 및 .NET 개발을 위한 공식 확장. c# dev kit 설치 방법, vs코드 필수 확장 안내.'
    ),
    # index.html
    'index.html': (
        'VS Code에서 꼭 설치해야 할 필수 확장 프로그램 모음.',
        'VS Code 필수 확장 프로그램 모음 — vs코드 확장·vs코드 테마·AI 코딩·Git·디버깅·생산성 익스텐션을 카테고리별 큐레이션. GitHub Copilot·ESLint·Prettier·GitLens 포함.'
    ),
}


def sync_og_twitter(content, new_val):
    content = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_val + x.group(2), content
    )
    content = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        lambda x: x.group(1) + new_val + x.group(2), content
    )
    return content


ok = 0
miss = 0

# ── 1) 개별 처리 ──────────────────────────────────────────────────────
for rel_path, (match_prefix, new_desc) in INDIVIDUAL.items():
    fpath = os.path.join(BASE, rel_path)
    if not os.path.exists(fpath):
        print(f'  SKIP: {rel_path}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    pattern = r'(<meta name="description" content=")[^"]*(")'
    def replacer(m, mp=match_prefix, nd=new_desc):
        if mp in m.group(0):
            return m.group(1) + nd + m.group(2)
        return m.group(0)
    c2 = re.sub(pattern, replacer, c)
    if c2 == c:
        print(f'  MISS: {rel_path}')
        miss += 1
        continue
    c2 = sync_og_twitter(c2, new_desc)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c2)
    print(f'  OK (개별): {rel_path}')
    ok += 1

# ── 2) extensions/*.html 공통 처리 ────────────────────────────────────
ext_files = sorted(glob.glob(os.path.join(BASE, 'extensions', '*.html')))
individually_done = {
    os.path.normpath(os.path.join(BASE, p)) for p in INDIVIDUAL
}

for fpath in ext_files:
    if os.path.normpath(fpath) in individually_done:
        continue

    fname_stem = os.path.splitext(os.path.basename(fpath))[0]
    is_theme = fname_stem in THEME_FILES

    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    # meta description 값 추출
    m = re.search(r'<meta name="description" content="([^"]+)"', c)
    if not m:
        print(f'  SKIP (desc 없음): extensions/{os.path.basename(fpath)}')
        continue
    old_desc = m.group(1)

    # Step1: "VS Code 확장 프로그램 설치." → "vs코드 확장 설치 가이드 —"
    new_desc = old_desc.replace(
        'VS Code 확장 프로그램 설치.',
        'vs코드 확장 설치 가이드 —',
        1
    )

    # Step2: suffix 교체
    suffix_new = (
        'vs코드 테마 추천, 설치 방법 안내.'
        if is_theme
        else 'vs코드 필수 확장, 설치 방법 안내.'
    )
    new_desc = re.sub(
        r'\s*WooaVS 엄선 필수 VS Code 확장\.',
        ' ' + suffix_new,
        new_desc
    )

    if new_desc == old_desc:
        print(f'  MISS: extensions/{os.path.basename(fpath)}')
        miss += 1
        continue

    # 교체 적용
    c2 = c.replace(
        f'<meta name="description" content="{old_desc}"',
        f'<meta name="description" content="{new_desc}"',
        1
    )
    c2 = sync_og_twitter(c2, new_desc)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c2)
    theme_tag = ' [테마]' if is_theme else ''
    print(f'  OK{theme_tag}: extensions/{os.path.basename(fpath)}')
    ok += 1

print(f'\n완료: {ok}개 교체, {miss}개 실패')
