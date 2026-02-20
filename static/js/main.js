/**
 * OsloBørsen — Global JavaScript
 * Handles: mobile nav, watchlist (localStorage), tooltips, market status
 */

'use strict';

// ════════════════════════════════════════════════════════
// Mobile nav toggle
// ════════════════════════════════════════════════════════
(function setupMobileMenu() {
  const btn  = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', () => {
    const isOpen = !menu.classList.contains('hidden');
    menu.classList.toggle('hidden', isOpen);
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.add('hidden');
    }
  });
})();


// ════════════════════════════════════════════════════════
// Watchlist  (localStorage-backed Set)
// ════════════════════════════════════════════════════════
const watchlist = (function() {
  const STORE_KEY = 'oslo_watchlist_v1';

  function load() {
    try { return new Set(JSON.parse(localStorage.getItem(STORE_KEY) || '[]')); }
    catch { return new Set(); }
  }
  function save(set) {
    localStorage.setItem(STORE_KEY, JSON.stringify([...set]));
  }

  let items = load();

  function has(ticker) { return items.has(ticker); }

  function add(ticker) {
    items.add(ticker);
    save(items);
    _updateCountBadge();
    _renderPanel();
  }

  function remove(ticker) {
    items.delete(ticker);
    save(items);
    _updateCountBadge();
    _renderPanel();
  }

  function toggle(ticker) {
    if (has(ticker)) remove(ticker);
    else add(ticker);
  }

  function all() { return [...items]; }

  function _updateCountBadge() {
    const badge = document.getElementById('watchlist-count');
    if (!badge) return;
    const count = items.size;
    badge.textContent = count;
    badge.classList.toggle('hidden', count === 0);
  }

  function _renderPanel() {
    const container = document.getElementById('watchlist-items');
    if (!container) return;

    if (!items.size) {
      container.innerHTML = '<p class="text-gray-500 text-sm text-center py-8">Your watchlist is empty.<br>Bookmark stocks from the screener.</p>';
      return;
    }

    container.innerHTML = [...items].map(ticker => `
      <div class="flex items-center gap-3 p-3 rounded-xl bg-surface-700 border border-surface-500 hover:border-brand-500/50 transition-colors">
        <a href="/stock/${ticker}" class="flex-1 min-w-0">
          <div class="text-sm font-medium text-white font-mono">${ticker}</div>
        </a>
        <button onclick="watchlist.remove('${ticker}')"
                class="p-1 rounded hover:bg-surface-500 text-gray-500 hover:text-red-400 transition-colors flex-shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    `).join('');
  }

  // Init
  _updateCountBadge();
  _renderPanel();

  return { has, add, remove, toggle, all };
})();


// ════════════════════════════════════════════════════════
// Watchlist side panel
// ════════════════════════════════════════════════════════
const watchlistPanel = (function() {
  const panel   = document.getElementById('watchlist-panel');
  const overlay = document.getElementById('watchlist-overlay');

  function open() {
    panel?.classList.add('open');
    overlay?.classList.add('open');
  }
  function close() {
    panel?.classList.remove('open');
    overlay?.classList.remove('open');
  }
  function toggle() {
    panel?.classList.contains('open') ? close() : open();
  }

  return { open, close, toggle };
})();


// ════════════════════════════════════════════════════════
// Metric tooltip system
// ════════════════════════════════════════════════════════
const TOOLTIPS = {
  dividend_yield: {
    title: 'Dividend Yield',
    body:  'Annual dividend per share ÷ current share price. Higher = more income relative to price. E.g. 5% means you earn 5 NOK for every 100 NOK invested.',
  },
  pe_ratio: {
    title: 'P/E Ratio (Price-to-Earnings)',
    body:  'How much you pay for each krone of profit. P/E 10 = cheap, P/E 30+ = expensive. Lower P/E can indicate undervaluation, but also slow growth expectations.',
  },
  pb_ratio: {
    title: 'P/B Ratio (Price-to-Book)',
    body:  'Share price compared to the company\'s book value per share. P/B < 1 means you\'re buying assets below their accounting value.',
  },
  eps: {
    title: 'EPS (Earnings Per Share)',
    body:  'Net profit divided by the number of shares outstanding. Higher EPS generally means a more profitable company.',
  },
  score: {
    title: 'Composite Score (0–100)',
    body:  'A simple score combining dividend yield (40 pts), P/E ratio (30 pts), and P/B ratio (30 pts). Designed to surface attractive dividend-value stocks. Not financial advice.',
  },
  change_pct: {
    title: 'Daily Change %',
    body:  'Percentage price change versus yesterday\'s closing price. Positive = stock is up today.',
  },
  roe: {
    title: 'Return on Equity (ROE)',
    body:  'Net income ÷ shareholders\' equity. Measures how efficiently a company uses investor money. Higher is generally better.',
  },
  payout_ratio: {
    title: 'Payout Ratio',
    body:  'What percentage of earnings is paid out as dividends. 50–70% is often considered sustainable. Very high (>100%) may mean dividends are being funded by debt.',
  },
  beta: {
    title: 'Beta',
    body:  'Measures how much the stock moves relative to the overall market. Beta > 1 = more volatile than market. Beta < 1 = less volatile. Beta ~0 = uncorrelated.',
  },
};

(function setupTooltips() {
  const popup    = document.getElementById('tooltip-popup');
  const titleEl  = document.getElementById('tooltip-title');
  const bodyEl   = document.getElementById('tooltip-body');
  let hideTimer  = null;

  function showTooltip(btn) {
    const key  = btn.dataset.tip;
    const data = TOOLTIPS[key];
    if (!data || !popup) return;

    clearTimeout(hideTimer);
    titleEl.textContent = data.title;
    bodyEl.textContent  = data.body;

    // Position near button
    const rect = btn.getBoundingClientRect();
    const pw   = 320; // max-w-xs ≈ 320px
    let left   = rect.left + window.scrollX;
    let top    = rect.bottom + window.scrollY + 8;

    if (left + pw > window.innerWidth - 16) left = window.innerWidth - pw - 16;
    if (left < 16) left = 16;

    popup.style.left    = `${left}px`;
    popup.style.top     = `${top}px`;
    popup.style.opacity = '1';
    popup.style.pointerEvents = 'auto';
  }

  function hideTooltip() {
    if (!popup) return;
    hideTimer = setTimeout(() => {
      popup.style.opacity = '0';
      popup.style.pointerEvents = 'none';
    }, 150);
  }

  // Delegate events on document for dynamically added buttons
  document.addEventListener('mouseover', (e) => {
    const btn = e.target.closest('.tooltip-btn');
    if (btn) showTooltip(btn);
  });
  document.addEventListener('mouseout', (e) => {
    if (e.target.classList.contains('tooltip-btn')) hideTooltip();
  });
  popup?.addEventListener('mouseenter', () => clearTimeout(hideTimer));
  popup?.addEventListener('mouseleave', hideTooltip);
})();


// ════════════════════════════════════════════════════════
// Market status indicator (Oslo Børs hours: 09:00–16:30 CET)
// ════════════════════════════════════════════════════════
(function setMarketStatus() {
  const dot   = document.getElementById('market-status-dot');
  const label = document.getElementById('market-status-label');
  if (!dot || !label) return;

  const now  = new Date();
  // Convert to Oslo time (CET = UTC+1, CEST = UTC+2)
  const oslo = new Date(now.toLocaleString('en-US', { timeZone: 'Europe/Oslo' }));
  const day  = oslo.getDay(); // 0=Sun, 6=Sat
  const hour = oslo.getHours();
  const min  = oslo.getMinutes();
  const mins = hour * 60 + min;

  const OPEN  = 9 * 60;       // 09:00
  const CLOSE = 16 * 60 + 30; // 16:30

  const isWeekday = day >= 1 && day <= 5;
  const isOpen    = isWeekday && mins >= OPEN && mins < CLOSE;

  if (isOpen) {
    dot.style.background = '#22c55e';
    label.textContent    = 'Market Open';
    label.style.color    = '#22c55e';
  } else {
    dot.style.background = '#6b7280';
    dot.classList.remove('animate-pulse-slow');
    label.textContent    = 'Market Closed';
    label.style.color    = '#6b7280';
  }
})();


// ════════════════════════════════════════════════════════
// Utility: format large numbers
// ════════════════════════════════════════════════════════
function fmtLarge(num) {
  if (num == null) return '—';
  if (num >= 1e12) return (num/1e12).toFixed(2)+'T';
  if (num >= 1e9)  return (num/1e9).toFixed(2)+'B';
  if (num >= 1e6)  return (num/1e6).toFixed(2)+'M';
  if (num >= 1e3)  return (num/1e3).toFixed(1)+'K';
  return num.toFixed(2);
}
