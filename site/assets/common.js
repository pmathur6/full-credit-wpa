/* Full-Credit WPA — shared helpers (no build step, plain JS) */
const FC = (() => {
  const COLORS = { batting: '#1E3A8A', baserunning: '#0E9F8E', fielding: '#E08A00', pitching: '#BE185D', behind: '#5B6472' };
  const BUCKETS = ['batting', 'baserunning', 'fielding', 'pitching'];
  const LABEL = { batting: 'Batting', baserunning: 'Baserunning', fielding: 'Fielding', pitching: 'Pitching' };
  const cache = new Map();
  const TEAMS = { ATH: 'Athletics', ATL: 'Atlanta Braves', AZ: 'Arizona Diamondbacks', BAL: 'Baltimore Orioles', BOS: 'Boston Red Sox',
    CHC: 'Chicago Cubs', CIN: 'Cincinnati Reds', CLE: 'Cleveland Guardians', COL: 'Colorado Rockies', CWS: 'Chicago White Sox',
    DET: 'Detroit Tigers', HOU: 'Houston Astros', KC: 'Kansas City Royals', LAA: 'Los Angeles Angels', LAD: 'Los Angeles Dodgers',
    MIA: 'Miami Marlins', MIL: 'Milwaukee Brewers', MIN: 'Minnesota Twins', NYM: 'New York Mets', NYY: 'New York Yankees',
    OAK: 'Oakland Athletics', PHI: 'Philadelphia Phillies', PIT: 'Pittsburgh Pirates', SD: 'San Diego Padres', SEA: 'Seattle Mariners',
    SF: 'San Francisco Giants', STL: 'St. Louis Cardinals', TB: 'Tampa Bay Rays', TEX: 'Texas Rangers', TOR: 'Toronto Blue Jays',
    WSH: 'Washington Nationals' };
  const NICK = { ATH: 'Athletics', ATL: 'Braves', AZ: 'Diamondbacks', BAL: 'Orioles', BOS: 'Red Sox', CHC: 'Cubs', CIN: 'Reds',
    CLE: 'Guardians', COL: 'Rockies', CWS: 'White Sox', DET: 'Tigers', HOU: 'Astros', KC: 'Royals', LAA: 'Angels', LAD: 'Dodgers',
    MIA: 'Marlins', MIL: 'Brewers', MIN: 'Twins', NYM: 'Mets', NYY: 'Yankees', OAK: 'Athletics', PHI: 'Phillies', PIT: 'Pirates',
    SD: 'Padres', SEA: 'Mariners', SF: 'Giants', STL: 'Cardinals', TB: 'Rays', TEX: 'Rangers', TOR: 'Blue Jays', WSH: 'Nationals' };
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  // '2026-05-22' -> 'May 22'
  function shortDate(d) { const [, m, day] = d.split('-'); return `${MONTHS[+m - 1]} ${+day}`; }
  function ordinal(n) { const s = ['th', 'st', 'nd', 'rd'], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); }
  const BASES = ['bases empty', 'runner on 1st', 'runner on 2nd', '1st & 2nd', 'runner on 3rd', '1st & 3rd', '2nd & 3rd', 'bases loaded'];

  async function getJSON(path) {
    if (!cache.has(path)) {
      cache.set(path, fetch(path).then(r => {
        if (!r.ok) throw new Error(`${path}: ${r.status}`);
        return r.json();
      }));
    }
    return cache.get(path);
  }

  // signed number with a real minus sign; digits by unit (wins 2, runs 1)
  function fmt(v, unit = 'w', digits) {
    if (v === null || v === undefined || Number.isNaN(v)) return '–';
    const d = digits ?? (unit === 'r' ? 1 : 2);
    const r = Number(v.toFixed(d));
    if (r === 0) return (0).toFixed(d);
    return (r > 0 ? '+' : '−') + Math.abs(r).toFixed(d);
  }

  function rowsToObjects(cols, rows) {
    return rows.map(r => Object.fromEntries(cols.map((c, i) => [c, r[i]])));
  }

  function params() { return new URLSearchParams(location.search); }
  function setParams(obj, defaults = {}) {
    const p = new URLSearchParams();
    for (const [k, v] of Object.entries(obj)) {
      if (v === undefined || v === null || v === '' || String(v) === String(defaults[k])) continue;
      p.set(k, v);
    }
    const q = p.toString();
    history.replaceState(null, '', q ? `?${q}` : location.pathname);
  }

  function esc(s) {
    return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  async function seasons() {
    const s = await getJSON('data/seasons.json');
    return s;
  }

  function header(active, { title, eyebrow, lede } = {}) {
    const link = (href, label, key) => `<a href="${href}"${active === key ? ' aria-current="page"' : ''}>${label}</a>`;
    return `<header class="site-head">
      <div class="intro">
        <p class="eyebrow">${eyebrow ?? '<a href="./">Full-Credit WPA</a>'}</p>
        <h1>${title ?? ''}</h1>
        ${lede ? `<p class="lede">${lede}</p>` : ''}
      </div>
      <nav class="nav" aria-label="Sections">
        ${link('./', 'Leaderboard', 'leaderboard')}
        ${link('games.html', 'Games', 'games')}
        ${link('about.html', 'How it works', 'about')}
      </nav>
    </header>`;
  }

  // stacked bar of signed parts from a zero line; scale = px per unit
  function bar(parts, scale, zero, width = 200) {
    let pos = zero, neg = zero, html = '';
    for (const [k, v] of parts) {
      if (!v) continue;
      const w = Math.min(Math.abs(v) * scale, width);
      let left;
      if (v > 0) { left = pos; pos += w; } else { neg -= w; left = neg; }
      html += `<span style="left:${left.toFixed(1)}px;width:${w.toFixed(1)}px;background:${COLORS[k]}"></span>`;
    }
    return `<div class="bar" style="width:${width}px">${html}<span class="zero" style="left:${zero - 1}px"></span></div>`;
  }

  return { COLORS, BUCKETS, LABEL, TEAMS, NICK, MONTHS, BASES, shortDate, ordinal, getJSON, fmt, rowsToObjects, params, setParams, esc, seasons, header, bar };
})();
