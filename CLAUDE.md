# VSKit 프로젝트 지침

## 프로젝트 개요
- **사이트명:** VSKit
- **URL:** https://vskit.wooahouse.com
- **GitHub:** https://github.com/ingmaster83-code/VSKit
- **배포:** GitHub Pages (main 브랜치 → root)
- **도메인 관리:** 호스팅케이알
- **DNS:** vskit CNAME → ingmaster83-code.github.io

## 기술 스택
- 순수 HTML / CSS / JS (프레임워크 없음)
- Google AdSense 수익화

## 서비스 목적
VS Code에서 꼭 설치해야 할 필수 확장 프로그램을 카테고리별로 큐레이션한 사이트.
코드 지원 · 테마 · Git · 디버깅 · 생산성 확장 분류 제공.
GitHub Copilot, ESLint, Prettier, GitLens 등 검증된 확장만 엄선.

## 파일 구조
```
VSKit/
├── index.html       # 메인 (확장 프로그램 목록)
├── about.html       # 서비스 소개
├── privacy.html     # 개인정보처리방침
├── robots.txt
├── sitemap.xml
├── CNAME            # vskit.wooahouse.com
└── css/
    └── style.css
```

## 작업 규칙
- 확장 프로그램 추가 시 공식 VS Code Marketplace 링크만 사용
- 카테고리 추가 시 sitemap.xml 업데이트
- SEO 키워드: VS Code 확장, VSCode 익스텐션, 비주얼스튜디오코드 플러그인, 필수 VSCode 확장
