/* Player page: season summary, cumulative chart, fielding by position, game log with every play */
(async () => {
  const { fmt, esc, COLORS, LABEL, TEAMS, BASES, shortDate, ordinal } = FC;
  const app = document.getElementById('app');
  const p = FC.params();
  const id = p.get('id');
  let meta;
  try { meta = await FC.seasons(); } catch (e) { app.innerHTML = `<div class="empty">Couldn't load the data.</div>`; return; }
  const S = {
    season: p.get('season') || String(meta.seasons[0]), unit: p.get('unit') || 'w', role: p.get('role') || '',
    order: 'impact', open: p.get('game') ? Number(p.get('game')) : null, pinned: p.get('game') ? Number(p.get('game')) : null,
    sel: null, shown: 30,
  };
  let P, LB, log;
  const $ = x => document.getElementById(x);

  async function load() {
    app.innerHTML = '<div class="loading">Loading…</div>';
    try { P = await FC.getJSON(`data/${S.season}/players/${id}.json`); }
    catch (e) {
      app.innerHTML = `<a class="back" href="./">← Leaderboard</a><div class="empty">No ${esc(S.season)} data for this player.
        ${meta.seasons.filter(y => String(y) !== S.season).map(y => `<a href="?id=${esc(id)}&season=${y}">${y}</a>`).join(' · ')}</div>`;
      return false;
    }
    LB = await FC.getJSON(`data/${S.season}/leaderboard.json`);
    if (!LB.rows) LB.rows = FC.rowsToObjects(LB.cols, LB.players);
    log = FC.rowsToObjects(P.log.cols, P.log.rows);
    const hit = P.pa > 0, pit = P.bf > 0;
    const two = P.pa >= 50 && P.bf >= 50;
    if (!two) S.role = pit && !hit ? 'pitching' : 'hitting';
    else if (!['hitting', 'pitching'].includes(S.role)) S.role = P.pa >= P.bf ? 'hitting' : 'pitching';
    P.two = two;
    if (S.sel === null) S.sel = null;
    document.title = `${P.name} ${S.season} — Full-Credit WPA`;
    return true;
  }

  const u = () => S.unit;
  const unitWord = () => (S.unit === 'w' ? 'Wins' : 'Runs');
  const k = (b) => ({ batting: 'bat', baserunning: 'br', fielding: 'fld', pitching: 'pit', behind: 'behind', trad: 'trad' }[b]);
  const g_ = (r, b) => r[`${k(b)}_${S.unit}`] || 0;
  const roleBuckets = () => (S.role === 'pitching' ? ['pitching', 'fielding'] : ['batting', 'baserunning', 'fielding']);
  // games for this role (two-way players split by whether he pitched)
  function roleGames() {
    if (!P.two) return log;
    return S.role === 'pitching' ? log.filter(r => r.bf > 0) : log.filter(r => r.bf === 0 || r.pa > 0);
  }
  function gameTotal(r) { return roleBuckets().reduce((s, b) => s + g_(r, b), 0); }

  function ranks() {
    const rows = LB.rows, U = S.unit;
    const tot = r => r[`bat_${U}`] + r[`br_${U}`] + r[`fld_${U}`] + r[`pit_${U}`];
    const by = (arr, f) => { const s = [...arr].sort((a, b) => f(b) - f(a)); return [s.findIndex(r => r.id === P.id) + 1, s.length]; };
    return {
      overall: by(rows, tot),
      batting: by(rows.filter(r => r.pa > 0), r => r[`bat_${U}`]),
      baserunning: by(rows.filter(r => r.pa > 0), r => r[`br_${U}`]),
      fielding: by(rows.filter(r => !/^P$/.test(r.pos)), r => r[`fld_${U}`]),
      pitching: by(rows.filter(r => r.bf >= (P.bf >= 300 ? 300 : 1)), r => r[`pit_${U}`]),
      pitchingAll: by(rows.filter(r => r.bf > 0), r => r[`pit_${U}`]),
    };
  }

  function tilesHTML() {
    const T = P.totals[S.unit], U = S.unit, R = ranks();
    const rk = ([n, of]) => (n > 0 ? `${ordinal(n)} of ${of}` : 'not ranked (under 10 games)');
    const tile = (label, v, sub, color, key) => `<div class="tile${key ? ' key' : ''}"><span class="lab">${color ? `<span class="dot" style="background:${color}"></span>` : ''}${label}</span>
      <span class="val"${v < 0 ? ' style="color:var(--neg)"' : ''}>${fmt(v, U)}</span><span class="sub">${sub}</span></div>`;
    const all = T.batting + T.baserunning + T.fielding + T.pitching;
    const tradName = U === 'w' ? 'Traditional WPA' : 'RE24';
    if (S.role === 'pitching') {
      const tot = T.pitching + T.fielding;
      return [
        P.two ? tile('Total (hitting + pitching)', all, rk(R.overall) + ' players', null, true) : tile('Total', tot, rk(R.overall) + ' players', null, true),
        tile('Pitching', T.pitching, `${rk(R.pitching)} pitchers${P.bf >= 300 ? ' with 300+ BF' : ''}`, COLORS.pitching),
        tile('Fielding', T.fielding, 'his own plays in the field', COLORS.fielding),
        tile(tradName, T.trad_pit, 'pitcher gets the whole play'),
        tile('Defense behind him', T.behind, 'fielders and coaching on his plays', COLORS.behind),
        tile('vs traditional', tot - T.trad_pit, 'pitching + fielding minus traditional'),
      ].join('');
    }
    const tot = T.batting + T.baserunning + T.fielding;
    return [
      P.two ? tile('Total (hitting + pitching)', all, rk(R.overall) + ' players', null, true) : tile('Total', tot, rk(R.overall) + ' players', null, true),
      tile('Batting', T.batting, `${P.pa} plate appearances`, COLORS.batting),
      tile('Baserunning', T.baserunning, rk(R.baserunning) + ' hitters', COLORS.baserunning),
      tile('Fielding', T.fielding, P.pos.replace('/DH', '').replace(/^DH$/, 'DH, no fielding'), COLORS.fielding),
      tile(tradName, T.trad_bat, 'batter gets the whole play'),
      tile('vs traditional', tot - T.trad_bat, U === 'w' ? 'value WPA leaves out' : 'value RE24 leaves out'),
    ].join('');
  }

  function headline() {
    const T = P.totals[S.unit], R = ranks();
    const parts = [];
    if (R.overall[0] > 0) parts.push(`${ordinal(R.overall[0])} of ${R.overall[1]} players in ${S.season}`);
    else parts.push(`${P.g} games in ${S.season} (under the 10-game minimum for the leaderboard)`);
    if (S.role === 'hitting') {
      const tot = T.batting + T.baserunning + T.fielding, other = T.baserunning + T.fielding;
      if (tot > 0 && other / tot >= 0.5) parts.push(`${other / tot >= 0.66 ? 'about two-thirds' : 'over half'} of his value came from baserunning and fielding`);
      if (T.batting > 0 && other < 0 && -other / T.batting > 0.25) parts.push('his baserunning and fielding gave back some of his bat');
    } else {
      const diff = T.pitching - T.trad_pit;
      if (Math.abs(diff) > (S.unit === 'w' ? 0.2 : 2)) parts.push(diff > 0 ? 'his defense cost him; his pitching was better than traditional numbers show' : 'his defense helped him; traditional numbers flatter his pitching');
    }
    return parts.join(' · ');
  }

  function splitPanel() {
    if (S.role !== 'pitching') return '';
    const T = P.totals[S.unit], U = S.unit, name = U === 'w' ? 'traditional WPA' : 'RE24';
    return `<section class="block panel" aria-label="How traditional value splits">
      <h2 style="font-size:16px">How ${name} splits for him</h2>
      <p class="small" style="font-size:14px">${U === 'w' ? 'Traditional WPA' : 'RE24'} gives a pitcher everything the defense did on his plays. Here's where his ${fmt(T.trad_pit, U)} actually went:</p>
      <div class="splitrow">
        <span><span class="dot" style="background:${COLORS.pitching}"></span>His pitching <b class="mono">${fmt(T.pitching, U)}</b></span>
        <span><span class="dot" style="background:${COLORS.fielding}"></span>His own fielding <b class="mono">${fmt(T.fielding, U)}</b></span>
        <span><span class="dot" style="background:${COLORS.behind}"></span>Defense and coaching behind him <b class="mono"${T.behind < 0 ? ' style="color:var(--neg)"' : ''}>${fmt(T.behind, U)}</b></span>
      </div>
      <p class="small">The three add up to his ${fmt(T.trad_pit, U)}${Math.abs(T.pitching + T.fielding + T.behind - T.trad_pit) > 0.02 ? ' (within rounding)' : ''}.</p>
    </section>`;
  }

  // ---- chart
  function niceTicks(lo, hi) {
    const span = hi - lo || 1, raw = span / 4, mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map(m => m * mag).find(s => s >= raw);
    const t = []; for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) t.push(+v.toFixed(6));
    return t;
  }
  function chartHTML() {
    const G = roleGames();
    if (!G.length) return '';
    let run = 0; const cum = G.map(r => (run += gameTotal(r)));
    let lo = Math.min(0, ...cum), hi = Math.max(0, ...cum);
    const pad = (hi - lo) * 0.08 || 0.5; lo -= pad; hi += pad;
    const n = G.length, H = 240;
    const X = i => (n === 1 ? 500 : i / (n - 1) * 1000), Y = v => H - (v - lo) / (hi - lo) * H;
    const pct = v => ((hi - v) / (hi - lo) * 100).toFixed(2);
    const ticks = niceTicks(lo, hi);
    if (S.sel === null || S.sel >= n) {
      const tt = G.map(gameTotal), pi = S.pinned != null ? G.findIndex(x => x.game === S.pinned) : -1;
      S.sel = pi >= 0 ? pi : tt.indexOf(Math.max(...tt));
    }
    const s = S.sel, left = (n === 1 ? 50 : s / (n - 1) * 100).toFixed(2);
    // month labels at each month's first game; skip one that would crowd the next
    let months = []; let last = '';
    G.forEach((r, i) => { const m = r.date.slice(5, 7); if (m !== last) { months.push([i, FC.MONTHS[+m - 1]]); last = m; } });
    const gap = n > 1 ? 0.07 * (n - 1) : 1;
    months = months.filter((m, j) => j === months.length - 1 || months[j + 1][0] - m[0] >= gap);
    const color = S.role === 'pitching' ? COLORS.pitching : COLORS.batting;
    const r = G[s], t = gameTotal(r);
    return `<section class="block" aria-label="${unitWord()} added through the season">
      <h2>${unitWord()} added through the season</h2>
      <p class="small">${S.role === 'pitching' ? 'Pitching plus his own fielding, game by game.' : 'Batting, baserunning and fielding, game by game.'} Tap any point to see that game.</p>
      <div class="panel" style="padding:16px 16px 8px">
        <div class="chart">
          <div class="yaxis"><span class="ytitle">${unitWord()} added (cumulative)</span>
            ${ticks.map(v => `<span class="ytick" style="top:${pct(v)}%">${v > 0 ? '+' : v < 0 ? '−' : ''}${Math.abs(v)}</span>`).join('')}</div>
          <div class="plot">
            <svg aria-hidden="true" viewBox="0 0 1000 240" preserveAspectRatio="none">
              ${ticks.filter(v => v !== 0).map(v => `<line x1="0" x2="1000" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}" stroke="#E3E6EA" vector-effect="non-scaling-stroke"/>`).join('')}
              <line x1="0" x2="1000" y1="${Y(0).toFixed(1)}" y2="${Y(0).toFixed(1)}" stroke="#12161C" vector-effect="non-scaling-stroke"/>
              <polyline points="${cum.map((v, i) => `${X(i).toFixed(1)},${Y(v).toFixed(1)}`).join(' ')}" fill="none" stroke="${color}" stroke-width="2.5" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
            </svg>
            <span class="guide" style="left:${left}%"></span><span class="mark" style="left:${left}%;top:${pct(cum[s])}%"></span>
            <div class="hits" id="hits">${G.map((g, i) => `<button type="button" data-i="${i}" aria-pressed="${i === s}" aria-label="${shortDate(g.date)} ${esc(g.opp)}, ${fmt(gameTotal(g), u())}"></button>`).join('')}</div>
          </div>
        </div>
        <div class="xaxis">${months.map(([i, m]) => { const x = n === 1 ? 0 : i / (n - 1) * 100; return `<span style="left:${x.toFixed(1)}%${x > 92 ? ';transform:translateX(-100%)' : ''}">${m}</span>`; }).join('')}</div>
        <div class="selbox" role="status">
          <div style="flex:1 1 180px;min-width:0"><div style="font-weight:600">${shortDate(r.date)} · ${esc(r.opp)}</div>
            <div class="small" style="font-size:13px">${esc(r.res.replace('-', '–'))}${S.role === 'pitching' ? ` · ${r.bf} batters faced` : r.pa ? ` · ${r.pa} PA` : ''}</div></div>
          <div style="display:flex;gap:20px">
            <div><div class="small" style="font-size:12px">This game</div><div class="big" style="color:${t >= 0 ? 'var(--link)' : 'var(--neg)'}">${fmt(t, u(), u() === 'w' ? 3 : 2)}</div></div>
            <div><div class="small" style="font-size:12px">Season to date</div><div class="big">${fmt(cum[s], u())}</div></div>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:8px">
            <button type="button" class="icon-btn" id="prev" aria-label="Previous game">‹</button>
            <button type="button" class="icon-btn" id="next" aria-label="Next game">›</button>
            <a href="#game-log" class="dark-btn" id="open-sel">Open in game log ↓</a>
          </div>
        </div>
      </div>
    </section>`;
  }

  function fieldingHTML() {
    const fp = Object.entries(P.fielding_by_pos || {}).sort((a, b) => b[1].g - a[1].g);
    if (!fp.length || (S.role === 'hitting' && fp.every(([pos]) => pos === 'P'))) return '';
    const rows = fp.filter(([pos]) => (S.role === 'pitching' ? pos === 'P' : pos !== 'P' || !P.two));
    if (!rows.length || S.role === 'pitching') return '';
    return `<section class="block" aria-label="Fielding by position"><h2>Fielding by position</h2>
      ${rows.map(([pos, v]) => `<div class="fieldpos"><span class="p">${pos}</span>
        <span class="small" style="font-size:14px">${v.g} games</span>
        <span class="small" style="font-size:14px">${unitWord()} <b class="mono" style="color:var(--ink);font-weight:500">${fmt(v[S.unit], u())}</b></span></div>`).join('')}
    </section>`;
  }

  // ---- game log
  function logHTML() {
    const G = roleGames();
    const idx = G.map((_, i) => i);
    const lists = {
      impact: idx.slice().sort((a, b) => gameTotal(G[b]) - gameTotal(G[a])).slice(0, 5),
      worst: idx.slice().sort((a, b) => gameTotal(G[a]) - gameTotal(G[b])).slice(0, 5),
      recent: idx.slice(-6).reverse(),
      all: idx.slice().reverse().slice(0, S.shown),
    };
    const pinnedI = S.pinned != null ? G.findIndex(r => r.game === S.pinned) : -1;
    const list = pinnedI >= 0 ? [pinnedI] : lists[S.order];
    const orders = [['impact', S.role === 'pitching' ? 'Best games' : 'Biggest games'], ['worst', 'Worst games'], ['recent', 'Most recent'], ['all', 'All games']];
    const pill = (label, v, color, unit = u()) => `<span class="pill">${color ? `<span class="dot" style="background:${color}"></span>` : '<span class="dot" style="border:1px solid var(--ink)"></span>'}${label} <b>${fmt(v, unit)}</b></span>`;
    const tradName = S.unit === 'w' ? 'Traditional' : 'RE24';
    const rows = list.map(i => {
      const r = G[i], t = gameTotal(r), open = S.open === r.game;
      const pills = S.role === 'pitching'
        ? [pill('Pitching', g_(r, 'pitching'), COLORS.pitching), pill('Fielding', g_(r, 'fielding'), COLORS.fielding), pill('Defense behind', g_(r, 'behind'), COLORS.behind), pill(tradName, g_(r, 'trad'), null)]
        : [pill('Batting', g_(r, 'batting'), COLORS.batting), pill('Baserunning', g_(r, 'baserunning'), COLORS.baserunning), pill('Fielding', g_(r, 'fielding'), COLORS.fielding)];
      return `<article data-game="${r.game}">
        <div class="row">
          <div class="when"><div style="font-weight:600">${shortDate(r.date)} · ${esc(r.opp)}</div>
            <div class="small" style="font-size:13px">${esc(r.res.replace('-', '–'))}${S.role === 'pitching' ? ` · ${r.bf} BF` : r.pa ? ` · ${r.pa} PA` : ''}</div></div>
          <div class="tot"><div class="big" style="color:${t >= 0 ? 'var(--link)' : 'var(--neg)'}">${fmt(t, u())}</div><div class="cap">${S.role === 'pitching' ? 'his total' : 'game total'}</div></div>
          <div class="pills">${pills.join('')}</div>
          <button type="button" class="btn" data-toggle="${r.game}" aria-expanded="${open}">${open ? 'Hide plays' : (S.role === 'pitching' ? 'Show batters' : 'Show plays')}</button>
        </div>
        ${open ? `<div class="plays" id="plays-${r.game}"><div class="loading" style="padding:16px">Loading plays…</div></div>` : ''}
      </article>`;
    }).join('');
    const moreBtn = pinnedI < 0 && S.order === 'all' && G.length > S.shown ? `<div class="more" style="margin-top:8px"><button type="button" class="btn" id="log-more">Show ${Math.min(30, G.length - S.shown)} more</button><span>${S.shown} of ${G.length} games</span></div>` : '';
    return `<section id="game-log" class="block" aria-label="Game log" style="scroll-margin-top:16px">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px">
        <h2>Game log</h2>
        <div class="seg" role="tablist" aria-label="Order" id="orders">${orders.map(([v, l]) => `<button type="button" role="tab" data-v="${v}" aria-selected="${pinnedI < 0 && S.order === v}">${l}</button>`).join('')}</div>
      </div>
      ${pinnedI >= 0 ? `<div class="banner"><span>Showing the game picked on the chart.</span><button type="button" class="linkbtn" id="unpin">Show all games</button></div>` : ''}
      <div class="log">${rows || '<div class="empty">No games.</div>'}</div>${moreBtn}
    </section>`;
  }

  // plays for one game, from the game file
  async function fillPlays(gid) {
    const box = $(`plays-${gid}`); if (!box) return;
    let G;
    try { G = await FC.getJSON(`data/${S.season}/games/${gid}.json`); }
    catch (e) { box.innerHTML = '<p class="small" style="padding:12px 0">Couldn\'t load this game.</p>'; return; }
    const C = G.cols, ci = Object.fromEntries(C.map((c, i) => [c, i]));
    const pid = P.id, U = S.unit, ui = U === 'w' ? 4 : 5;
    const myTeam = (() => {
      for (const e of G.events) for (const c of e[ci.credits]) if (c[0] === pid) return c[1];
      const r = log.find(x => x.game === gid); return r && r.opp.startsWith('@') ? G.away : G.home;
    })();
    const opp = myTeam === G.home ? G.away : G.home;
    const neg = U === 'w' ? 0.001 : 0.005;
    const nm = x => { const n = G.names[String(x)] || ''; return n.split(' ').slice(1).join(' ') || n; };
    const items = [];
    for (const e of G.events) {
      const cr = e[ci.credits];
      const mine = cr.filter(c => c[0] === pid);
      const isPitcher = e[ci.pitcher] === pid, isBatter = e[ci.batter] === pid;
      if (S.role === 'pitching' ? !isPitcher : !(isBatter || (mine.length && !isPitcher))) continue;
      const by = {};
      for (const c of mine) {
        if (S.role === 'hitting' && c[2] === 'pitching') continue;
        by[c[2]] = (by[c[2]] || 0) + c[ui];
      }
      if (!isBatter && !isPitcher && !Object.keys(by).length) continue;
      if (e[ci.kind] === 'mid' && !Object.keys(by).length && S.role === 'hitting') continue;
      const chips = FC.BUCKETS.filter(b => b in by).map(b => [b, by[b]]).map(([b, v]) => `<span class="chip" style="background:${v >= 0 || Math.abs(v) < neg ? COLORS[b] : 'var(--neg)'}">${LABEL[b]} ${Math.abs(v) < neg ? 'negligible' : fmt(v, U, U === 'w' ? 3 : 2)}</span>`);
      if (S.role === 'pitching') {
        const others = {};
        for (const c of cr) {
          if (c[0] === pid || c[1] !== myTeam) continue;
          const key = c[0] ? nm(c[0]) : 'Coaching';
          others[key] = (others[key] || 0) + c[ui];
        }
        for (const [n, v] of Object.entries(others)) if (!(n === 'Coaching' && Math.abs(v) < neg)) chips.push(`<span class="chip ghost">${esc(n)} ${Math.abs(v) < neg ? 'negligible' : fmt(v, U, U === 'w' ? 3 : 2)}</span>`);
      }
      const batting = e[ci.half] === 'bottom' ? G.home : G.away;
      const d = e[U === 'w' ? ci.d_w : ci.d_r] * (batting === myTeam ? 1 : -1);
      const usScore = myTeam === G.home ? e[ci.home] : e[ci.away], themScore = myTeam === G.home ? e[ci.away] : e[ci.home];
      const big = Math.abs(d) >= (U === 'w' ? 0.1 : 0.75);
      items.push(`<div class="play${big ? ' bigplay' : ''}">
        <div class="sit"><b>${e[ci.half] === 'top' ? 'T' : 'B'}${e[ci.inning]}</b><span>${e[ci.outs]} out · ${BASES[e[ci.bases]]} · ${myTeam} ${usScore}–${themScore} ${opp}</span>${e[ci.kind] === 'mid' ? '<span>between pitches</span>' : ''}</div>
        <div class="desc">${esc(e[ci.desc] || e[ci.type])}</div>
        <div class="foot"><div class="chips">${chips.join('') || '<span class="small">no credit on this play</span>'}</div><span class="whole">Whole play ${fmt(d, U, U === 'w' ? 3 : 2)}</span></div>
      </div>`);
    }
    box.innerHTML = (items.join('') || '<p class="small" style="padding:12px 0">No plays.</p>') +
      `<p class="small" style="margin-top:12px">"Whole play" is the swing in ${myTeam}'s ${U === 'w' ? 'win probability' : 'expected runs'}${S.role === 'pitching' ? ", what traditional numbers would give him. The coloured chips are his share; the grey chips are the fielders and coaching behind him. \"Negligible\" means a fielder was involved but moved the play by almost nothing." : `. The chips are ${esc(P.name.split(' ').slice(-1)[0])}'s share; the rest went to teammates, the pitcher, the fielders or coaching.`}</p>
      <a href="game.html?id=${gid}&season=${S.season}&player=${pid}" style="display:inline-flex;align-items:center;min-height:44px;margin-top:8px;font-size:14px;font-weight:600">Open the full game →</a>`;
  }

  function render() {
    const U = S.unit;
    const team = P.team.split('/').map(t => TEAMS[t] || t).join(' / ');
    const count = S.role === 'pitching' ? `${P.bf} batters faced` : `${P.pa} PA`;
    app.innerHTML = `
      <a class="back" href="./?season=${S.season}">← Leaderboard</a>
      <header class="site-head">
        <div class="intro">
          <p class="eyebrow">${esc(P.pos)} · ${esc(team)} · ${P.two ? `${P.pa} PA · ${P.bf} BF` : count}</p>
          <h1>${esc(P.name)}</h1>
          <p class="lede">${headline()}</p>
        </div>
        <div class="controls">
          ${P.two ? `<div class="field">Role<div class="seg" role="tablist" aria-label="Role" id="role">${[['hitting', 'Hitting'], ['pitching', 'Pitching']].map(([v, l]) => `<button type="button" role="tab" data-v="${v}" aria-selected="${S.role === v}">${l}</button>`).join('')}</div></div>` : ''}
          <label class="field">Season<select id="season">${meta.seasons.map(y => `<option${String(y) === S.season ? ' selected' : ''}>${y}</option>`).join('')}</select></label>
          <div class="field">Measure<div class="seg" role="radiogroup" aria-label="Measure" id="unit">${[['w', 'Wins'], ['r', 'Runs (context-neutral)']].map(([v, l]) => `<button type="button" role="radio" data-v="${v}" aria-checked="${S.unit === v}">${l}</button>`).join('')}</div></div>
        </div>
      </header>
      ${U === 'r' ? '<p class="note">Context-neutral view: the same split in runs (run expectancy), every play weighted equally.</p>' : ''}
      <section class="tiles" aria-label="Season summary">${tilesHTML()}</section>
      ${splitPanel()}
      ${chartHTML()}
      ${fieldingHTML()}
      ${logHTML()}
      <footer class="site-foot"><p>${U === 'w' ? 'Wins added, weighted by game situation.' : 'Runs added, every play weighted equally.'} Data: MLB Stats API, Baseball Savant · ${S.season} regular season</p>
        <p><a href="about.html">How it works</a></p></footer>`;
    FC.setParams({ id, season: S.season, unit: S.unit, role: P.two ? S.role : '', game: S.pinned ?? '' }, { unit: 'w', season: String(meta.seasons[0]) });
    wire();
    if (S.open != null) fillPlays(S.open);
  }

  function wire() {
    $('season').onchange = async e => { S.season = e.target.value; S.sel = null; S.open = S.pinned = null; if (await load()) render(); };
    $('unit').onclick = e => { const b = e.target.closest('button'); if (!b) return; S.unit = b.dataset.v; render(); };
    if ($('role')) $('role').onclick = e => { const b = e.target.closest('button'); if (!b) return; S.role = b.dataset.v; S.sel = null; S.open = S.pinned = null; render(); };
    const G = roleGames();
    if ($('hits')) {
      $('hits').onclick = e => { const b = e.target.closest('button'); if (!b) return; S.sel = +b.dataset.i; render(); };
      $('prev').onclick = () => { S.sel = Math.max(0, S.sel - 1); render(); };
      $('next').onclick = () => { S.sel = Math.min(G.length - 1, S.sel + 1); render(); };
      $('open-sel').onclick = e => { e.preventDefault(); const gid = G[S.sel].game; S.pinned = gid; S.open = gid; render(); $('game-log').scrollIntoView({ behavior: 'smooth' }); };
    }
    $('orders').onclick = e => { const b = e.target.closest('button'); if (!b) return; S.order = b.dataset.v; S.pinned = null; S.shown = 30; render(); };
    if ($('unpin')) $('unpin').onclick = () => { S.pinned = null; render(); };
    if ($('log-more')) $('log-more').onclick = () => { S.shown += 30; render(); };
    document.querySelectorAll('[data-toggle]').forEach(b => {
      b.onclick = () => { const gid = +b.dataset.toggle; S.open = S.open === gid ? null : gid; render(); };
    });
  }

  if (!id) { app.innerHTML = '<div class="empty">No player chosen. <a href="./">Back to the leaderboard</a></div>'; return; }
  if (await load()) {
    // a linked game opens in the log
    if (S.pinned != null && !roleGames().some(r => r.game === S.pinned) && P.two) S.role = S.role === 'hitting' ? 'pitching' : 'hitting';
    render();
    if (S.pinned != null) $('game-log')?.scrollIntoView();
  }
})();
