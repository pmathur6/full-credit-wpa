/* Game page: team totals, win-probability chart, split for any play, play-by-play */
(async () => {
  const { fmt, esc, COLORS, LABEL, NICK, BASES, ordinal } = FC;
  const app = document.getElementById('app');
  const p = FC.params();
  const gid = p.get('id');
  let meta;
  try { meta = await FC.seasons(); } catch (e) { app.innerHTML = '<div class="empty">Couldn\'t load the data.</div>'; return; }
  const S = { closed: new Set(), season: p.get('season') || String(meta.seasons[0]), unit: p.get('unit') || 'w', player: p.get('player') ? +p.get('player') : null, sel: null };
  const $ = x => document.getElementById(x);
  if (!gid) { app.innerHTML = '<div class="empty">No game chosen. <a href="games.html">Browse games</a></div>'; return; }
  let G;
  try { G = await FC.getJSON(`data/${S.season}/games/${gid}.json`); }
  catch (e) { app.innerHTML = `<a class="back" href="games.html">← Games</a><div class="empty">Couldn't find this game in ${esc(S.season)}.</div>`; return; }
  const ci = Object.fromEntries(G.cols.map((c, i) => [c, i]));
  const E = G.events.map(e => ({
    key: e[ci.key], kind: e[ci.kind], type: e[ci.type], inning: e[ci.inning], half: e[ci.half], outs: e[ci.outs], bases: e[ci.bases],
    away: e[ci.away], home: e[ci.home], desc: e[ci.desc] || e[ci.type], batter: e[ci.batter], pitcher: e[ci.pitcher],
    wpb: e[ci.wp_before], wpa: e[ci.wp_after], dw: e[ci.d_w], dr: e[ci.d_r],
    credits: e[ci.credits].map(c => ({ pid: c[0], team: c[1], bucket: c[2], role: c[3], w: c[4], r: c[5], note: c[6] })),
  }));
  const nameOf = pid => G.names[String(pid)] || String(pid);
  E.forEach(e => {
    e.bat = e.half === 'bottom' ? G.home : G.away;
    const run = e.credits.find(c => c.bucket === 'baserunning' && c.pid);
    e.desc = FC.eventText(e.kind, e.type, e.desc, run ? nameOf(run.pid) : '');
  });
  const playerTeam = S.player ? (E.flatMap(e => e.credits).find(c => c.pid === S.player) || {}).team : null;
  const focus = playerTeam || G.home;                 // chart and swings from this team's side
  const other = focus === G.home ? G.away : G.home;
  const homeWon = G.home_runs > G.away_runs;
  const winner = homeWon ? G.home : G.away, loser = homeWon ? G.away : G.home;
  const wR = homeWon ? G.home_runs : G.away_runs, lR = homeWon ? G.away_runs : G.home_runs;
  // swing of an event from a team's side, in the current unit
  const swing = (e, team) => (S.unit === 'w' ? e.dw : e.dr) * (e.bat === team ? 1 : -1);
  const cv = c => (S.unit === 'w' ? c.w : c.r);
  const D = S.unit === 'w' ? 3 : 2;

  function teamTotals(team) {
    const by = { batting: 0, baserunning: 0, fielding: 0, pitching: 0, coaching: 0 }, ppl = {};
    for (const e of E) for (const c of e.credits) {
      if (c.team !== team) continue;
      by[c.bucket] = (by[c.bucket] || 0) + cv(c);
      if (c.pid) ppl[c.pid] = (ppl[c.pid] || 0) + cv(c);
    }
    const total = Object.values(by).reduce((a, b) => a + b, 0);
    const list = Object.entries(ppl).map(([pid, v]) => [+pid, v]);
    return { by, total, top: list.filter(x => x[1] > 0).sort((a, b) => b[1] - a[1]).slice(0, 3), bottom: list.filter(x => x[1] < 0).sort((a, b) => a[1] - b[1]).slice(0, 3) };
  }

  function teamCard(team) {
    const T = teamTotals(team), U = S.unit;
    const pl = (pid, v) => `<div class="r"><a href="player.html?id=${pid}&season=${S.season}&game=${gid}${U === 'r' ? '&unit=r' : ''}">${esc(nameOf(pid))}</a><span style="color:${v >= 0 ? 'var(--link)' : 'var(--neg)'}">${fmt(v, U, D)}</span></div>`;
    return `<div class="teamcard">
      <div class="top"><span class="nm">${esc(FC.TEAMS[team] || team)}</span>${U === 'r' ? `<span class="big" style="color:${T.total >= 0 ? 'var(--link)' : 'var(--neg)'}">${fmt(T.total, U)}</span>` : ''}</div>
      <div class="chips" style="gap:6px">${['batting', 'baserunning', 'fielding', 'pitching', 'coaching'].map(b => `<span class="pill"><span class="dot" style="background:${COLORS[b] || '#8A93A1'}"></span>${b === 'coaching' ? 'Coaching' : LABEL[b]} <b>${fmt(T.by[b] || 0, U)}</b></span>`).join('')}</div>
      <div class="leaders"><div><div class="h">Most added</div>${T.top.map(x => pl(...x)).join('') || '<div class="small">—</div>'}</div>
        <div><div class="h">Most cost</div>${T.bottom.map(x => pl(...x)).join('') || '<div class="small">—</div>'}</div></div>
    </div>`;
  }

  // chart series from the focus team's side
  function series() {
    if (S.unit === 'w') {
      const f = v => (focus === G.home ? v : 1 - v);
      return [f(E[0].wpb), ...E.map(e => f(e.wpa))];
    }
    let run = 0; return [0, ...E.map(e => (run += swing(e, focus)))];
  }

  function chartHTML() {
    const pts = series(), n = E.length, U = S.unit;
    let lo, hi, ticks;
    if (U === 'w') { lo = 0; hi = 1; ticks = [0, 0.25, 0.5, 0.75, 1]; }
    else { const m = Math.max(1, ...pts.map(Math.abs)) * 1.1; lo = -m; hi = m; const st = m > 6 ? 4 : m > 3 ? 2 : 1; ticks = []; for (let v = -Math.floor(m / st) * st; v <= m; v += st) ticks.push(v); }
    const H = 240, X = j => j / n * 1000, Y = v => H - (v - lo) / (hi - lo) * H, pct = v => ((hi - v) / (hi - lo) * 100).toFixed(2);
    const s = S.sel, x = ((s + 1) / n * 100).toFixed(2);
    const inns = []; E.forEach((e, i) => { if (e.half === 'top' && (i === 0 || E[i - 1].inning !== e.inning)) inns.push([i, e.inning]); });
    const step = inns.length > 12 || (inns.length > 9 && window.innerWidth < 600) ? 2 : 1;
    const label = U === 'w' ? `${NICK[focus] || focus} win probability` : `${NICK[focus] || focus} run margin (expected)`;
    return `<section class="block" aria-label="Chart">
      <h2>${U === 'w' ? 'Win probability, play by play' : 'Expected-run margin, play by play'}</h2>
      <p class="small">Tap any point to see who got credit for that play.</p>
      <div class="panel" style="padding:16px 16px 8px">
        <div class="chart"><div class="yaxis" style="height:240px"><span class="ytitle">${esc(label)}</span>
          ${ticks.map(v => `<span class="ytick" style="top:${pct(v)}%">${U === 'w' ? Math.round(v * 100) + '%' : (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v)}</span>`).join('')}</div>
          <div class="plot" style="height:240px">
            ${U === 'w' ? `<span class="wpbg"></span><span class="fav" style="top:6px">${esc(NICK[focus] || focus)} favored</span><span class="fav" style="bottom:6px">${esc(NICK[other] || other)} favored</span>` : `<span class="fav" style="top:6px">${esc(NICK[focus] || focus)} ahead</span><span class="fav" style="bottom:6px">${esc(NICK[other] || other)} ahead</span>`}
            ${inns.slice(1).map(([i]) => `<span class="innline" style="left:${(i / n * 100).toFixed(2)}%"></span>`).join('')}
            <svg aria-hidden="true" viewBox="0 0 1000 240" preserveAspectRatio="none">
              <line x1="0" x2="1000" y1="${Y(U === 'w' ? 0.5 : 0).toFixed(1)}" y2="${Y(U === 'w' ? 0.5 : 0).toFixed(1)}" stroke="#8A93A1" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>
              <polyline points="${pts.map((v, j) => `${X(j).toFixed(1)},${Y(v).toFixed(1)}`).join(' ')}" fill="none" stroke="${COLORS.batting}" stroke-width="2.5" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
            </svg>
            <span class="guide" style="left:${x}%"></span><span class="mark" style="left:${x}%;top:${pct(pts[s + 1])}%"></span>
            <div class="hits" id="hits">${E.map((e, i) => `<button type="button" data-i="${i}" aria-pressed="${i === s}" aria-label="${e.half === 'top' ? 'Top' : 'Bottom'} ${e.inning}: ${esc(e.desc.slice(0, 60))}"></button>`).join('')}</div>
          </div></div>
        <div class="xaxis">${inns.filter((_, j) => j % step === 0).map(([i, inn]) => `<span style="left:${(i / n * 100).toFixed(1)}%">${inn}</span>`).join('')}</div>
        <p class="small" style="margin:2px 0 8px 64px;font-size:12px">Innings</p>
      </div></section>`;
  }

  function selHTML() {
    const e = E[S.sel], U = S.unit;
    const agg = {};
    for (const c of e.credits) {
      const k = `${c.pid ?? 'coach-' + c.team}|${c.bucket === 'coaching' ? c.role : c.bucket}`;
      if (!agg[k]) agg[k] = { pid: c.pid, team: c.team, bucket: c.bucket, what: c.bucket === 'coaching' ? c.role : LABEL[c.bucket], v: 0 };
      agg[k].v += cv(c);
    }
    const neg = U === 'w' ? 0.001 : 0.005;
    const rows = Object.values(agg).filter(a => a.pid || Math.abs(a.v) >= neg).sort((a, b) => (b.team === e.bat) - (a.team === e.bat) || Math.abs(b.v) - Math.abs(a.v));
    const m = Math.max(1e-6, ...rows.map(r => Math.abs(r.v)));
    const sums = {}; for (const r of rows) sums[r.team] = (sums[r.team] || 0) + r.v;
    const from = U === 'w' ? (focus === G.home ? e.wpb : 1 - e.wpb) : null, to = U === 'w' ? (focus === G.home ? e.wpa : 1 - e.wpa) : null;
    const us = focus === G.home ? e.home : e.away, them = focus === G.home ? e.away : e.home;
    return `<section id="selected-play" class="selplay" aria-label="Selected play">
      <div class="head">
        <div style="flex:1 1 320px;min-width:0;display:flex;flex-direction:column;gap:4px">
          <span class="small" style="font-size:13px"><b class="mono" style="color:var(--ink);font-weight:500">${e.half === 'top' ? 'Top' : 'Bottom'} ${ordinal(e.inning)}</b> · ${e.outs} out · ${BASES[e.bases]} · ${focus} ${us}–${them} ${other}${e.kind === 'mid' ? ' · between pitches' : ''}</span>
          <span style="font-size:17px;font-weight:600">${esc(e.desc)}</span>
          <span class="small" style="font-size:14px">${U === 'w' ? `${esc(NICK[focus] || focus)} win probability ${(from * 100).toFixed(1)}% → ${(to * 100).toFixed(1)}%` : `${esc(NICK[focus] || focus)} expected runs ${fmt(swing(e, focus), 'r', 2)}`}</span>
        </div>
        <div style="display:flex;gap:8px"><button type="button" class="icon-btn" id="prev" aria-label="Previous play">‹</button><button type="button" class="icon-btn" id="next" aria-label="Next play">›</button></div>
      </div>
      <div class="split">
        <div class="hdr"><span>Player</span><span>Credited for</span><span class="tr">Share of the swing</span><span style="text-align:right">${U === 'w' ? 'Wins' : 'Runs'}</span></div>
        ${rows.map(r => {
          const w = Math.abs(r.v) / m * 50, color = r.bucket === 'coaching' ? '#8A93A1' : (COLORS[r.bucket] || '#8A93A1');
          const who = r.pid ? `<a href="player.html?id=${r.pid}&season=${S.season}&game=${gid}${U === 'r' ? '&unit=r' : ''}">${esc(nameOf(r.pid))}</a>` : '<b>Coaching</b>';
          return `<div class="ln"><span style="min-width:0">${who} <span class="small" style="font-size:12px">${r.team}</span></span>
            <span style="display:inline-flex;align-items:center;gap:6px;font-size:13px"><span class="dot" style="background:${color}"></span>${esc(r.what.charAt(0).toUpperCase() + r.what.slice(1))}</span>
            <span class="track"><span class="mid"></span><span class="fill" style="background:${r.v >= 0 ? color : 'var(--neg)'};${r.v >= 0 ? `left:50%;width:${w}%` : `left:${50 - w}%;width:${w}%`}"></span></span>
            <span class="v" style="color:${r.v >= 0 ? 'var(--ink)' : 'var(--neg)'}">${Math.abs(r.v) < neg ? 'negligible' : fmt(r.v, U, D)}</span></div>`;
        }).join('')}
      </div>
      <p class="small">Each player's credit is in his own team's ${U === 'w' ? 'wins' : 'runs'}, so the two sides cancel: <span class="mono">${Object.entries(sums).map(([t, v]) => `${t} ${fmt(v, U, D)}`).join(' · ')}</span>.</p>
    </section>`;
  }

  function pbpHTML() {
    const halves = [];
    E.forEach((e, i) => {
      const k = `${e.inning}${e.half}`;
      if (!halves.length || halves[halves.length - 1].k !== k) halves.push({ k, e, items: [] });
      halves[halves.length - 1].items.push(i);
    });
    const U = S.unit;
    S.halves = halves.map(h => h.k);
    for (const h of halves) if (h.items.includes(S.sel)) S.closed.delete(h.k);
    const allClosed = halves.every(h => S.closed.has(h.k));
    return `<section class="block" aria-label="Play by play">
      <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px"><h2>Play by play</h2>
        <button type="button" class="btn" id="toggle-all">${allClosed ? 'Expand all innings' : 'Collapse all innings'}</button></div>
      ${S.player ? `<p class="small"><span style="color:var(--fld)">●</span> marks plays ${esc(nameOf(S.player))} was part of.</p>` : ''}
      <div style="display:flex;flex-direction:column;gap:12px">
      ${halves.map(h => {
        const last = E[h.items[h.items.length - 1]];
        const runs = h.e.half === 'top' ? (lastScore(h.items).away - h.e.away) : (lastScore(h.items).home - h.e.home);
        const open = !S.closed.has(h.k);
        return `<details class="half" data-k="${h.k}"${open ? ' open' : ''}><summary class="ht"><span>${h.e.half === 'top' ? 'Top' : 'Bottom'} ${ordinal(h.e.inning)} · ${esc(NICK[h.e.bat] || h.e.bat)} batting</span><span>${runs ? `${runs} run${runs > 1 ? 's' : ''} · ` : ''}${h.items.length} play${h.items.length > 1 ? 's' : ''}</span></summary>
          ${h.items.map(i => {
            const e = E[i], v = swing(e, focus), mine = S.player && (e.batter === S.player || e.pitcher === S.player || e.credits.some(c => c.pid === S.player && Math.abs(cv(c)) > 0));
            return `<a href="#selected-play" class="pl${i === S.sel ? ' on' : ''}${mine ? ' mine' : ''}" data-i="${i}"><span class="d">${esc(e.desc)}</span><span class="s" style="color:${v >= 0 ? 'var(--link)' : 'var(--neg)'}">${fmt(v, U, D)}</span></a>`;
          }).join('')}</details>`;
      }).join('')}
      </div>
      <p class="small">Numbers are each play's swing in ${esc(NICK[focus] || focus)} ${U === 'w' ? 'win probability' : 'expected runs'}. Tap a play to see the split.</p></section>`;
  }
  // score after the last event of a half (start of the next event, or the final)
  function lastScore(items) {
    const j = items[items.length - 1] + 1;
    return j < E.length ? { home: E[j].home, away: E[j].away } : { home: G.home_runs, away: G.away_runs };
  }

  function headline() {
    const U = S.unit;
    let best = 0; E.forEach((e, i) => { if (swing(e, winner) > swing(E[best], winner)) best = i; });
    const e = E[best];
    return `The biggest play for the ${esc(NICK[winner] || winner)}: ${esc(e.desc.replace(/\.$/, ''))} (${e.half === 'top' ? 'top' : 'bottom'} of the ${ordinal(e.inning)}, ${fmt(swing(e, winner), U, D)}${U === 'w' ? ' wins' : ' runs'}).`;
  }

  function render() {
    const d = new Date(G.date + 'T12:00:00');
    const dateStr = d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
    if (S.sel === null) {
      const pi = p.get('play') ? E.findIndex(e => e.key === p.get('play')) : -1;
      if (pi >= 0) S.sel = pi;
      else {
        const cand = E.map((e, i) => i).filter(i => !S.player || E[i].credits.some(c => c.pid === S.player));
        const pool = cand.length ? cand : E.map((e, i) => i);
        S.sel = pool.reduce((a, i) => (Math.abs(S.player ? E[i].credits.filter(c => c.pid === S.player).reduce((s, c) => s + cv(c), 0) : swing(E[i], focus)) >
          Math.abs(S.player ? E[a].credits.filter(c => c.pid === S.player).reduce((s, c) => s + cv(c), 0) : swing(E[a], focus)) ? i : a), pool[0]);
      }
    }
    document.title = `${NICK[G.away]} @ ${NICK[G.home]}, ${G.date} — Full-Credit WPA`;
    app.innerHTML = `
      <nav class="backs" aria-label="Back"><a class="back" href="./?season=${S.season}">← Leaderboard</a><a class="back" href="games.html?season=${S.season}">← Games</a>
        ${S.player ? `<a class="back" href="player.html?id=${S.player}&season=${S.season}&game=${gid}${S.unit === 'r' ? '&unit=r' : ''}">← ${esc(nameOf(S.player))}</a>` : ''}</nav>
      <header class="site-head">
        <div class="intro">
          <p class="eyebrow">${esc(dateStr)} · ${G.innings} innings · ${esc(G.away)} @ ${esc(G.home)}</p>
          <h1>${esc(NICK[winner] || winner)} ${wR}, ${esc(NICK[loser] || loser)} ${lR}</h1>
          <p class="lede">${headline()}</p>
        </div>
        <div class="controls"><div class="field">Measure<div class="seg" role="radiogroup" aria-label="Measure" id="unit">${[['w', 'Wins'], ['r', 'Runs (context-neutral)']].map(([v, l]) => `<button type="button" role="radio" data-v="${v}" aria-checked="${S.unit === v}">${l}</button>`).join('')}</div></div></div>
      </header>
      <section class="teams" aria-label="Team totals">${teamCard(winner)}${teamCard(loser)}</section>
      ${chartHTML()}
      ${selHTML()}
      ${pbpHTML()}
      <footer class="site-foot"><p>${S.unit === 'w' ? 'Wins added, weighted by game situation.' : 'Runs added, every play weighted equally.'} Data: MLB Stats API, Baseball Savant.</p><p><a href="about.html">How it works</a></p></footer>`;
    FC.setParams({ id: gid, season: S.season, unit: S.unit, player: S.player ?? '', play: E[S.sel].key }, { unit: 'w', season: String(meta.seasons[0]) });
    $('unit').onclick = ev => { const b = ev.target.closest('button'); if (!b) return; S.unit = b.dataset.v; render(); };
    $('hits').onclick = ev => { const b = ev.target.closest('button'); if (!b) return; S.sel = +b.dataset.i; render(); };
    $('prev').onclick = () => { S.sel = Math.max(0, S.sel - 1); render(); $('selected-play').scrollIntoView({ block: 'nearest' }); };
    $('next').onclick = () => { S.sel = Math.min(E.length - 1, S.sel + 1); render(); $('selected-play').scrollIntoView({ block: 'nearest' }); };
    document.querySelectorAll('details.half').forEach(d => { d.ontoggle = () => { d.open ? S.closed.delete(d.dataset.k) : S.closed.add(d.dataset.k); }; });
    $('toggle-all').onclick = () => {
      const close = !S.halves.every(k => S.closed.has(k));
      S.closed = new Set(close ? S.halves : []);
      document.querySelectorAll('details.half').forEach(d => { d.ontoggle = null; d.open = !close; });
      $('toggle-all').textContent = close ? 'Expand all innings' : 'Collapse all innings';
      document.querySelectorAll('details.half').forEach(d => { d.ontoggle = () => { d.open ? S.closed.delete(d.dataset.k) : S.closed.add(d.dataset.k); }; });
    };
    document.querySelectorAll('a.pl').forEach(a => { a.onclick = ev => { ev.preventDefault(); S.sel = +a.dataset.i; render(); $('selected-play').scrollIntoView({ behavior: 'smooth' }); }; });
  }
  render();
  if (p.get('play')) $('selected-play').scrollIntoView();
})();
