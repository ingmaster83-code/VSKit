(function() {
  let deferredPrompt = null;

  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferredPrompt = e;
    setTimeout(showPWABanner, 3000);
  });

  window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    closePWABanner();
    const heroBtn = document.getElementById('heroInstallBtn');
    if (heroBtn) heroBtn.style.display = 'none';
  });

  // hero 버튼 클릭
  document.addEventListener('DOMContentLoaded', () => {
    // 이미 설치된 경우 버튼 숨김
    if (window.matchMedia('(display-mode: standalone)').matches) {
      const heroBtn = document.getElementById('heroInstallBtn');
      if (heroBtn) heroBtn.style.display = 'none';
      return;
    }
    const heroBtn = document.getElementById('heroInstallBtn');
    if (heroBtn) {
      heroBtn.addEventListener('click', () => {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          deferredPrompt.userChoice.then(() => {
            deferredPrompt = null;
            heroBtn.style.display = 'none';
          });
        } else {
          alert('주소창 오른쪽의 설치 아이콘(⊕)을 클릭해 홈 화면에 추가하세요.');
        }
      });
    }
  });

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }

  window.showPWABanner = function() {
    if (sessionStorage.getItem('pwa_shown')) return;
    if (window.matchMedia('(display-mode: standalone)').matches) return;
    if (!deferredPrompt) return;

    sessionStorage.setItem('pwa_shown', '1');

    const style = document.createElement('style');
    style.textContent = `
      #pwa-install-banner {
        position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
        background: #1A1A2E; border-top: 3px solid #374151;
        padding: 14px 16px; display: flex; align-items: center; gap: 12px;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
        animation: slideUp 0.3s ease;
      }
      @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
      .pwa-banner-icon { font-size: 2rem; flex-shrink: 0; }
      .pwa-banner-text { flex: 1; }
      .pwa-banner-text strong { display: block; color: #fff; font-size: 0.95rem; }
      .pwa-banner-text span { color: rgba(255,255,255,0.7); font-size: 0.82rem; }
      .pwa-btn-install {
        background: #374151; color: #fff; border: none; border-radius: 8px;
        padding: 8px 18px; font-size: 0.88rem; font-weight: 700; cursor: pointer;
        white-space: nowrap; flex-shrink: 0;
      }
      .pwa-btn-install:hover { opacity: 0.85; }
      .pwa-btn-close {
        background: none; border: none; color: rgba(255,255,255,0.5);
        font-size: 1.2rem; cursor: pointer; padding: 4px; flex-shrink: 0;
      }
      .pwa-btn-close:hover { color: #fff; }
    `;
    document.head.appendChild(style);

    const banner = document.createElement('div');
    banner.id = 'pwa-install-banner';
    banner.innerHTML = `
      <div class="pwa-banner-icon">💻</div>
      <div class="pwa-banner-text">
        <strong>VSKit - VS Code 확장 프로그램 모음 바로가기 추가</strong>
        <span>앱처럼 설치해서 빠르게 접근하세요!</span>
      </div>
      <button class="pwa-btn-install" onclick="window.triggerPWAInstall()">설치하기</button>
      <button class="pwa-btn-close" onclick="window.closePWABanner()">✕</button>
    `;
    document.body.appendChild(banner);
    setTimeout(closePWABanner, 20000);
  };

  window.triggerPWAInstall = function() {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(() => {
      deferredPrompt = null;
      closePWABanner();
    });
  };

  window.closePWABanner = function() {
    const el = document.getElementById('pwa-install-banner');
    if (el) el.remove();
  };
})();
