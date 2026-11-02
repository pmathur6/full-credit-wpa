/* Leaderboard: players (all / hitters / pitchers) and team coaching, wins or runs */
(async () => {
  const { fmt, esc, bar, BUCKETS, COLORS, LABEL } = FC;
  const app = document.getElementById('app');
  const PAGE = 50;
  const DEFAULTS = { board: 'all', unit: 'w', team: '', pos: '', min: '', q: '', sort: 'total', dir: 'desc' };

  let meta;
  try { meta = await FC.seasons(); } catch (e) {
    app.innerHTML = `<div class="empty">Couldn't load the data (${esc(e.message)}).</div>`; return;
  }
  const p = FC.params();
  const S = {
    season: p.get('season') || String(meta.seasons[0]),
    board: p.get('board') || DEFAULTS.board, unit: p.get('unit') || DEFAULTS.unit,
    team: p.get('team') || '', pos: p.get('pos') || '', min: p.get('min') ?? '', q: p.get('q') || '',
    sort: p.get('sort') || DEFAULTS.sort, dir: p.get('dir') || DEFAULTS.dir, shown: PAGE,
  };

  app.innerHTML = `
    ${FC.header('leaderboard', { title: 'Who actually won the games',
      lede: "Every play's change in win probability, split across everyone involved: the batter, the runners, the pitcher, the fielders and the coaching staff." })}
    <section class="filters" aria-label="Filters">
      <div class="field">Board<div class="seg" role="tablist" aria-label="Board" id="board"></div></div>
      <div class="field">Measure<div class="seg" role="radiogroup" aria-label="Measure" id="unit"></div></div>
      <label class="field">Season<select id="season"></select></label>
      <label class="field">Team<select id="team"></select></label>
      <label class="field" id="pos-wrap">Position<select id="pos">
        <option value="">All positions</option><option>P</option><option>C</option><option>1B</option><option>2B</option>
        <option>3B</option><option>SS</option><option value="OF">OF</option><option>DH</option></select></label>
      <label class="field" id="min-wrap"><span id="min-label">Min PA or BF</span><input type="number" id="min" min="0" step="50" inputmode="numeric"></label>
      <div class="field grow" id="q-wrap"><label for="q">Player</label>
        <div class="search"><input type="search" id="q" placeholder="Search players" autocomplete="off">
        <button type="button" id="q-clear" class="clear" aria-label="Clear search" hidden>×</button></div></div>
      <button type="button" class="btn" id="reset" hidden>Reset filters</button>
    </section>
    <p class="note" id="unit-note" hidden></p>
    <section id="body" aria-live="polite"></section>
    <footer class="site-foot">
      <p id="foot-note"></p>
      <p id="foot-src"></p>
    </footer>`;

  const $ = id => document.getElementById(id);
  $('season').innerHTML = meta.seasons.map(y => `<option${String(y) === S.season ? ' selected' : ''}>${y}</option>`).join('');
  $('pos').value = S.pos; $('min').value = S.min; $('q').value = S.q;

  function seg(el, items, key, role) {
    el.innerHTML = items.map(([v, l]) => `<button type="button" role="${role}" data-v="${v}" aria-${role === 'tab' ? 'selected' : 'checked'}="${S[key] === v}">${l}</button>`).join('');
    el.onclick = e => {
      const b = e.target.closest('button'); if (!b) return;
      S[key] = b.dataset.v; S.shown = PAGE;
      if (key === 'board') { S.sort = 'total'; S.dir = 'desc'; }
      render();
    };
  }

  let data = null;
  async function load() {
    $('body').innerHTML = '<div class="loading">Loading…</div>';
    data = await FC.getJSON(`data/${S.season}/leaderboard.json`);
    data.rows = FC.rowsToObjects(data.cols, data.players);
    const teams = [...new Set(data.rows.flatMap(r => r.team.split('/')))].filter(Boolean).sort();
    $('team').innerHTML = `<option value="">All teams</option>` + teams.map(t => `<option${t === S.team ? ' selected' : ''}>${t}</option>`).join('');
    if (S.team && !teams.includes(S.team)) S.team = '';
  }

  function val(r, b) {
    const u = S.unit;
    const k = { batting: 'bat', baserunning: 'br', fielding: 'fld', pitching: 'pit' }[b];
    return r[`${k}_${u}`] || 0;
  }
  // hitters board: batting side only; pitchers board: pitching side only; all: everything
  function boardBuckets() {
    return S.board === 'hitters' ? ['batting', 'baserunning', 'fielding']
      : S.board === 'pitchers' ? ['fielding', 'pitching'] : BUCKETS;
  }
  function derived(r) {
    const parts = boardBuckets().map(b => [b, val(r, b)]);
    const total = parts.reduce((s, x) => s + x[1], 0);
    const trad = (S.board !== 'pitchers' ? r[`tradbat_${S.unit}`] || 0 : 0) + (S.board !== 'hitters' ? r[`tradpit_${S.unit}`] || 0 : 0);
    return { parts, total, trad, diff: total - trad };
  }
  function posMatch(r) {
    if (!S.pos) return true;
    const ps = r.pos.split('/');
    return S.pos === 'OF' ? ps.some(x => ['LF', 'CF', 'RF'].includes(x)) : ps.includes(S.pos);
  }

  function playersView() {
    const minDefault = S.board === 'all' ? 0 : 100;
    const min = S.min === '' ? minDefault : Number(S.min);
    const q = S.q.trim().toLowerCase();
    let rows = data.rows.filter(r => {
      if (S.board === 'hitters' && r.pa === 0) return false;
      if (S.board === 'pitchers' && r.bf === 0) return false;
      if (S.team && !r.team.split('/').includes(S.team)) return false;
      if (!posMatch(r)) return false;
      const n = S.board === 'hitters' ? r.pa : S.board === 'pitchers' ? r.bf : Math.max(r.pa, r.bf);
      if (n < min) return false;
      if (q && !r.name.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').includes(q.normalize('NFD').replace(/[̀-ͯ]/g, ''))) return false;
      return true;
    }).map(r => ({ ...r, ...derived(r) }));
    const key = {
      total: r => r.total, pa: r => r.pa, bf: r => r.bf, trad: r => r.trad, diff: r => r.diff, name: r => r.name,
      batting: r => val(r, 'batting'), baserunning: r => val(r, 'baserunning'), fielding: r => val(r, 'fielding'), pitching: r => val(r, 'pitching'),
    }[S.sort] || (r => r.total);
    const sgn = S.dir === 'asc' ? 1 : -1;
    rows.sort((a, b) => {
      const x = key(a), y = key(b);
      return (typeof x === 'string' ? x.localeCompare(y) : x - y) * sgn || b.total - a.total;
    });
    // rank by the current sort over the filtered set
    const n = rows.length;
    // bar scale: fit the largest positive and negative stacks among the shown rows
    const shown = rows.slice(0, S.shown);
    let maxPos = 0.01, maxNeg = 0;
    for (const r of shown) {
      maxPos = Math.max(maxPos, r.parts.filter(x => x[1] > 0).reduce((s, x) => s + x[1], 0));
      maxNeg = Math.max(maxNeg, -r.parts.filter(x => x[1] < 0).reduce((s, x) => s + x[1], 0));
    }
    const W = 200, zero = Math.max(16, Math.min(80, Math.round(W * maxNeg / (maxPos + maxNeg)) + 4));
    const scale = (W - zero - 2) / maxPos;
    const isHit = S.board === 'hitters', isPit = S.board === 'pitchers';
    const tradName = S.unit === 'w' ? 'Trad. WPA' : 'RE24';
    const cols = [
      ['rank', '#', 'l rank', false], ['name', 'Player', 'l name', true],
      ...(!isPit ? [['pa', 'PA', '', true]] : []), ...(!isHit ? [['bf', 'BF', '', true]] : []),
      ['total', 'Total', '', true], ['bar', 'Breakdown', 'l', false],
      ...(!isPit ? [['batting', 'Batting', '', true], ['baserunning', 'Baserunning', '', true]] : []),
      ['fielding', 'Fielding', '', true], ...(!isHit ? [['pitching', 'Pitching', '', true]] : []),
      ['trad', tradName, '', true], ['diff', 'vs trad.', '', true],
    ];
    const th = cols.map(([k, l, cls, sortable]) => {
      const sorted = S.sort === k;
      const aria = sorted ? ` aria-sort="${S.dir === 'asc' ? 'ascending' : 'descending'}"` : '';
      const arrow = sorted ? (S.dir === 'asc' ? ' ▴' : ' ▾') : '';
      return `<th scope="col" class="${cls}"${aria}>${sortable ? `<button type="button" data-sort="${k}">${l}${arrow}</button>` : `<button type="button" tabindex="-1" style="cursor:default">${l}</button>`}</th>`;
    }).join('');
    const u = S.unit;
    const body = shown.map((r, i) => {
      const cells = {
        rank: `<td class="rank">${i + 1}</td>`,
        name: `<td class="name"><a href="player.html?id=${r.id}&season=${S.season}">${esc(r.name)}</a><div class="sub">${esc(r.pos)} · ${esc(r.team)}</div></td>`,
        pa: `<td class="dim">${r.pa || '–'}</td>`, bf: `<td class="dim">${r.bf || '–'}</td>`,
        total: `<td class="strong${r.total < 0 ? ' neg' : ''}">${fmt(r.total, u)}</td>`,
        bar: `<td class="l"><div role="img" aria-label="${r.parts.map(([b, v]) => `${LABEL[b]} ${fmt(v, u)}`).join(', ')}">${bar(r.parts, scale, zero, W)}</div></td>`,
        batting: `<td>${r.pa ? fmt(val(r, 'batting'), u) : '–'}</td>`,
        baserunning: `<td>${r.pa ? fmt(val(r, 'baserunning'), u) : '–'}</td>`,
        fielding: `<td>${fmt(val(r, 'fielding'), u)}</td>`,
        pitching: `<td>${r.bf ? fmt(val(r, 'pitching'), u) : '–'}</td>`,
        trad: `<td class="dim">${fmt(r.trad, u)}</td>`,
        diff: `<td class="strong" style="color:${r.diff >= 0 ? 'var(--link)' : 'var(--neg)'}">${fmt(r.diff, u)}</td>`,
      };
      return `<tr>${cols.map(c => cells[c[0]]).join('')}</tr>`;
    }).join('');
    const legend = `<div class="legend">${BUCKETS.filter(b => !(isHit && b === 'pitching') && !(isPit && (b === 'batting' || b === 'baserunning')))
      .map(b => `<span><span class="sw" style="background:${COLORS[b]}"></span>${LABEL[b]}</span>`).join('')}
      <span>Bars start at the black line; segments left of it are negative.</span></div>`;
    $('body').innerHTML = n === 0 ? `${legend}<div class="empty">No players match these filters.</div>` : `
      <div style="display:flex;flex-direction:column;gap:12px">${legend}
      <div class="table-wrap"><table class="board"><thead><tr>${th}</tr></thead><tbody>${body}</tbody></table></div>
      <div class="more">${n > S.shown ? `<button type="button" class="btn" id="more">Show ${Math.min(PAGE, n - S.shown)} more</button>` : ''}<span>${Math.min(S.shown, n)} of ${n} players</span></div></div>`;
    $('body').querySelector('thead').onclick = e => {
      const b = e.target.closest('button[data-sort]'); if (!b) return;
      const k = b.dataset.sort;
      if (S.sort === k) S.dir = S.dir === 'desc' ? 'asc' : 'desc';
      else { S.sort = k; S.dir = k === 'name' ? 'asc' : 'desc'; }
      render();
    };
    const more = $('more'); if (more) more.onclick = () => { S.shown += PAGE; render(); };
  }

  function coachingView() {
    const c = data.coaching, u = S.unit;
    const roles = ['positioning', 'bunt call', 'intentional walk', 'defensive indifference'].filter(r => c.roles.includes(r));
    const label = { positioning: 'Positioning', 'bunt call': 'Bunt calls', 'intentional walk': 'Intentional walks', 'defensive indifference': 'Def. indifference' };
    let rows = FC.rowsToObjects(c.cols, c.rows).map(r => ({ team: r.team, ...Object.fromEntries(roles.map(x => [x, r[`${x}_${u}`] || 0])) }));
    rows.forEach(r => { r.total = roles.reduce((s, x) => s + r[x], 0); });
    if (S.team) rows = rows.filter(r => r.team === S.team);
    const k = S.sort in rows[0] ? S.sort : 'total';
    rows.sort((a, b) => (k === 'team' ? a.team.localeCompare(b.team) : a[k] - b[k]) * (S.dir === 'asc' ? 1 : -1));
    const cols = [['team', 'Team', 'l name'], ['total', 'Total', ''], ...roles.map(x => [x, label[x], ''])];
    const th = `<th scope="col" class="l rank"><button type="button" tabindex="-1" style="cursor:default">#</button></th>` + cols.map(([key, l, cls]) => {
      const sorted = k === key;
      return `<th scope="col" class="${cls}"${sorted ? ` aria-sort="${S.dir === 'asc' ? 'ascending' : 'descending'}"` : ''}><button type="button" data-sort="${key}">${l}${sorted ? (S.dir === 'asc' ? ' ▴' : ' ▾') : ''}</button></th>`;
    }).join('');
    const body = rows.map((r, i) => `<tr><td class="rank">${i + 1}</td><td class="name"><strong>${r.team}</strong></td>
      <td class="strong${r.total < 0 ? ' neg' : ''}">${fmt(r.total, u)}</td>${roles.map(x => `<td>${fmt(r[x], u)}</td>`).join('')}</tr>`).join('');
    $('body').innerHTML = `<div style="display:flex;flex-direction:column;gap:12px">
      <p class="muted" style="margin:0;font-size:13px">Team decisions that changed games: defensive positioning, sacrifice bunt calls, intentional walks and defensive indifference.</p>
      <div class="table-wrap"><table class="board" style="min-width:640px"><thead><tr>${th}</tr></thead><tbody>${body}</tbody></table></div></div>`;
    $('body').querySelector('thead').onclick = e => {
      const b = e.target.closest('button[data-sort]'); if (!b) return;
      const key = b.dataset.sort;
      if (S.sort === key) S.dir = S.dir === 'desc' ? 'asc' : 'desc'; else { S.sort = key; S.dir = key === 'team' ? 'asc' : 'desc'; }
      render();
    };
  }

  function render() {
    seg($('board'), [['all', 'All players'], ['hitters', 'Hitters'], ['pitchers', 'Pitchers'], ['coaching', 'Coaching']], 'board', 'tab');
    seg($('unit'), [['w', 'Wins'], ['r', 'Runs (context-neutral)']], 'unit', 'radio');
    const coaching = S.board === 'coaching';
    $('pos-wrap').hidden = coaching; $('min-wrap').hidden = coaching; $('q-wrap').hidden = coaching;
    $('min-label').textContent = S.board === 'pitchers' ? 'Min BF' : S.board === 'hitters' ? 'Min PA' : 'Min PA or BF';
    $('min').placeholder = S.board === 'all' ? '0' : '100';
    const note = $('unit-note');
    note.hidden = S.unit !== 'r';
    note.textContent = 'Context-neutral view: the same split in runs (run expectancy), where every play counts the same no matter the score or inning.';
    $('foot-note').textContent = S.unit === 'w'
      ? 'Wins added, weighted by game situation. Traditional WPA gives the batter or pitcher the whole play; "vs trad." is the difference. Players with 10+ games; positions with 10+ appearances, most games first.'
      : 'Runs added, every play weighted equally. RE24 gives the batter or pitcher the whole play; "vs trad." is the difference. Players with 10+ games; positions with 10+ appearances, most games first.';
    $('foot-src').textContent = `Data: MLB Stats API, Baseball Savant · ${S.season} regular season${meta.updated ? ' · updated ' + meta.updated : ''}`;
    $('q-clear').hidden = !S.q;
    $('reset').hidden = !(S.team || S.pos || S.min !== '' || S.q || S.board !== DEFAULTS.board || S.unit !== DEFAULTS.unit || S.sort !== DEFAULTS.sort || S.dir !== DEFAULTS.dir);
    FC.setParams({ season: S.season, board: S.board, unit: S.unit, team: S.team, pos: S.pos, min: S.min, q: S.q, sort: S.sort, dir: S.dir },
      { ...DEFAULTS, season: String(meta.seasons[0]) });
    coaching ? coachingView() : playersView();
  }

  $('season').onchange = async e => { S.season = e.target.value; S.shown = PAGE; await load(); render(); };
  $('team').onchange = e => { S.team = e.target.value; S.shown = PAGE; render(); };
  $('pos').onchange = e => { S.pos = e.target.value; S.shown = PAGE; render(); };
  $('min').oninput = e => { S.min = e.target.value; S.shown = PAGE; render(); };
  $('q-clear').onclick = () => { $('q').value = ''; S.q = ''; S.shown = PAGE; render(); $('q').focus(); };
  $('reset').onclick = () => {
    Object.assign(S, { board: DEFAULTS.board, unit: DEFAULTS.unit, team: '', pos: '', min: '', q: '', sort: DEFAULTS.sort, dir: DEFAULTS.dir, shown: PAGE });
    $('team').value = ''; $('pos').value = ''; $('min').value = ''; $('q').value = '';
    render();
  };
  let t; $('q').oninput = e => { clearTimeout(t); t = setTimeout(() => { S.q = e.target.value; S.shown = PAGE; render(); }, 150); };

  try { await load(); render(); } catch (e) {
    $('body').innerHTML = `<div class="empty">Couldn't load ${esc(S.season)} (${esc(e.message)}).</div>`;
  }
})();
