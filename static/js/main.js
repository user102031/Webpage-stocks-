/**
 * Nordic Stock Analyzer — Global JavaScript
 * Handles: market switching, mobile nav, watchlist (localStorage), tooltips, market status
 */

'use strict';

// ════════════════════════════════════════════════════════
// Market switcher (localStorage-backed)
// ════════════════════════════════════════════════════════
const marketSwitcher = (function() {
  const STORE_KEY = 'nordic_market_v1';
  const MARKET_NAMES = {
    NO: { short: 'OsloBørsen',         full: 'Oslo Børs',           exchange: 'Oslo Børs / Euronext',    currency: 'NOK', tz: 'Europe/Oslo',       open: 540, close: 990 },
    SE: { short: 'Stockholmsbörsen',   full: 'Nasdaq Stockholm',    exchange: 'Nasdaq Stockholm',        currency: 'SEK', tz: 'Europe/Stockholm',  open: 540, close: 1050 },
    DK: { short: 'Københavnsbørsen',   full: 'Nasdaq Copenhagen',   exchange: 'Nasdaq Copenhagen',       currency: 'DKK', tz: 'Europe/Copenhagen', open: 540, close: 1020 },
    FI: { short: 'Helsinkibörsen',     full: 'Nasdaq Helsinki',     exchange: 'Nasdaq Helsinki',         currency: 'EUR', tz: 'Europe/Helsinki',   open: 600, close: 1110 },
  };

  function get() {
    const m = localStorage.getItem(STORE_KEY);
    return (m && MARKET_NAMES[m]) ? m : 'NO';
  }

  function set(market) {
    if (!MARKET_NAMES[market]) return;
    localStorage.setItem(STORE_KEY, market);
    _updateUI(market);
    // Reload page so all data refreshes with new market
    window.location.reload();
  }

  function getConfig() {
    return MARKET_NAMES[get()];
  }

  function _updateUI(market) {
    const cfg = MARKET_NAMES[market];
    if (!cfg) return;

    // Update brand name
    const brandEl = document.getElementById('brand-name');
    if (brandEl) brandEl.textContent = cfg.short;

    // Update footer
    const footerBrand = document.getElementById('footer-brand');
    if (footerBrand) footerBrand.textContent = cfg.short;
    const footerExchange = document.getElementById('footer-exchange');
    if (footerExchange) footerExchange.textContent = cfg.exchange;
    const footerCurrency = document.getElementById('footer-currency');
    if (footerCurrency) footerCurrency.textContent = cfg.currency;

    // Highlight active flag
    document.querySelectorAll('.market-flag-btn').forEach(btn => {
      const isActive = btn.dataset.market === market;
      btn.classList.toggle('market-flag-active', isActive);
    });

    // Update market status
    _setMarketStatus(cfg);
  }

  function _setMarketStatus(cfg) {
    const dot   = document.getElementById('market-status-dot');
    const label = document.getElementById('market-status-label');
    if (!dot || !label) return;

    const now = new Date();
    const local = new Date(now.toLocaleString('en-US', { timeZone: cfg.tz }));
    const day  = local.getDay();
    const mins = local.getHours() * 60 + local.getMinutes();

    const isWeekday = day >= 1 && day <= 5;
    const isOpen    = isWeekday && mins >= cfg.open && mins < cfg.close;

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
  }

  // Init: set up flag buttons & update UI
  document.querySelectorAll('.market-flag-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const m = btn.dataset.market;
      if (m !== get()) set(m);
    });
  });

  // Apply current market on load (no reload)
  _updateUI(get());

  return { get, set, getConfig };
})();


// ════════════════════════════════════════════════════════
// API fetch helper — auto-appends ?market=XX
// ════════════════════════════════════════════════════════
function apiFetch(url, options) {
  const market = marketSwitcher.get();
  const sep = url.includes('?') ? '&' : '?';
  return fetch(`${url}${sep}market=${market}`, options);
}


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
  const STORE_KEY = 'nordic_watchlist_v2';

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
    body:  'Annual dividend per share \u00f7 current share price. Higher = more income relative to price. E.g. 5% means you earn 5 NOK for every 100 NOK invested.',
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
    title: 'Composite Score (0\u2013100)',
    body:  'A simple score combining dividend yield (40 pts), P/E ratio (30 pts), and P/B ratio (30 pts). Designed to surface attractive dividend-value stocks. Not financial advice.',
  },
  change_pct: {
    title: 'Daily Change %',
    body:  'Percentage price change versus yesterday\'s closing price. Positive = stock is up today.',
  },
  roe: {
    title: 'Return on Equity (ROE)',
    body:  'Net income \u00f7 shareholders\' equity. Measures how efficiently a company uses investor money. Higher is generally better.',
  },
  payout_ratio: {
    title: 'Payout Ratio',
    body:  'What percentage of earnings is paid out as dividends. 50\u201370% is often considered sustainable. Very high (>100%) may mean dividends are being funded by debt.',
  },
  beta: {
    title: 'Beta',
    body:  'Measures how much the stock moves relative to the overall market. Beta > 1 = more volatile than market. Beta < 1 = less volatile. Beta ~0 = uncorrelated.',
  },
  recommendation: {
    title: 'Analyst Recommendation',
    body:  'Based on consensus from professional analysts covering this stock. They set price targets and rate stocks as Buy, Hold, or Sell. "Strong Buy" means most analysts expect significant upside. This is not financial advice \u2014 analyst targets can be wrong.',
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

    const rect = btn.getBoundingClientRect();
    const pw   = 320;
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
// Utility: format large numbers
// ════════════════════════════════════════════════════════
function fmtLarge(num) {
  if (num == null) return '\u2014';
  if (num >= 1e12) return (num/1e12).toFixed(2)+'T';
  if (num >= 1e9)  return (num/1e9).toFixed(2)+'B';
  if (num >= 1e6)  return (num/1e6).toFixed(2)+'M';
  if (num >= 1e3)  return (num/1e3).toFixed(1)+'K';
  return num.toFixed(2);
}
