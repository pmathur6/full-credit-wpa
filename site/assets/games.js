/* Games index: every game in a season, by date, filterable by team and month */
(async () => {
  const { esc, NICK, MONTHS } = FC;
  const app = document.getElementById('app');
  const p = FC.params();
  let meta;
  try { meta = await FC.seasons(); } catch (e) { app.innerHTML = '<div class="empty">Couldn\'t load the data.</div>'; return; }
  const S = { season: p.get('season') || String(meta.seasons[0]), team: p.get('team') || '', month: p.get('month') || '', extra: p.get('extra') === '1', close: p.get('close') === '1' };
  const $ = x => document.getElementById(x);
  app.innerHTML = `${FC.header('games', { title: 'Games', lede: 'Every game of the season. Open one to see the win-probability chart and who got credit for each play.' })}
    <section class="filters" aria-label="Filters">
      <label class="field">Season<select id="season">${meta.seasons.map(y => `<option${String(y) === S.season ? ' selected' : ''}>${y}</option>`).join('')}</select></label>
      <label class="field">Team<select id="team"></select></label>
      <label class="field">Month<select id="month"></select></label>
      <label class="field" style="flex-direction:row;align-items:center;gap:8px;min-height:44px;font-size:14px;color:var(--ink)"><input type="checkbox" id="extra" style="width:20px;height:20px"> Extra innings</label>
      <label class="field" style="flex-direction:row;align-items:center;gap:8px;min-height:44px;font-size:14px;color:var(--ink)"><input type="checkbox" id="close" style="width:20px;height:20px"> One-run games</label>
    </section>
    <section id="list" aria-live="polite"></section>
    <footer class="site-foot"><p>Data: MLB Stats API, Baseball Savant.</p></footer>`;
  let rows = [];
  async function load() {
    const d = await FC.getJSON(`data/${S.season}/games.json`);
    rows = FC.rowsToObjects(d.cols, d.rows);
    const teams = [...new Set(rows.flatMap(r => [r.away, r.home]))].sort();
    $('team').innerHTML = '<option value="">All teams</option>' + teams.map(t => `<option value="${t}"${t === S.team ? ' selected' : ''}>${esc(FC.TEAMS[t] || t)}</option>`).join('');
    const months = [...new Set(rows.map(r => r.date.slice(5, 7)))].sort();
    $('month').innerHTML = '<option value="">All months</option>' + months.map(m => `<option value="${m}"${m === S.month ? ' selected' : ''}>${MONTHS[+m - 1]}</option>`).join('');
  }
  function render() {
    $('extra').checked = S.extra; $('close').checked = S.close;
    const list = rows.filter(r => (!S.team || r.away === S.team || r.home === S.team) && (!S.month || r.date.slice(5, 7) === S.month)
      && (!S.extra || r.innings > 9) && (!S.close || Math.abs(r.home_runs - r.away_runs) === 1)).reverse();
    const byDay = {};
    for (const r of list) (byDay[r.date] = byDay[r.date] || []).push(r);
    const days = Object.keys(byDay);
    const card = (r, withDate) => {
      const aw = r.away_runs > r.home_runs;
      return `<a class="gamecard" href="game.html?id=${r.id}&season=${S.season}">
        ${withDate ? `<span class="x">${FC.shortDate(r.date)}</span>` : ''}
        <span class="ln${aw ? ' w' : ''}"><span>${esc(NICK[r.away] || r.away)}</span><span>${r.away_runs}</span></span>
        <span class="ln${aw ? '' : ' w'}"><span>@ ${esc(NICK[r.home] || r.home)}</span><span>${r.home_runs}</span></span>
        ${r.innings !== 9 ? `<span class="x">${r.innings} innings</span>` : ''}</a>`;
    };
    // one team: a single grid with dates on the cards; otherwise grouped by day
    $('list').innerHTML = !list.length ? '<div class="empty">No games match.</div>' : `<p class="small" style="margin-bottom:12px">${list.length} games</p>` + (S.team
      ? `<div class="gamegrid">${list.map(r => card(r, true)).join('')}</div>`
      : `<div class="daylist">${days.map(d => {
        const dt = new Date(d + 'T12:00:00').toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
        return `<div class="day"><h3>${dt}</h3><div class="gamegrid">${byDay[d].map(r => card(r, false)).join('')}</div></div>`;
      }).join('')}</div>`);
    FC.setParams({ season: S.season, team: S.team, month: S.month, extra: S.extra ? 1 : '', close: S.close ? 1 : '' }, { season: String(meta.seasons[0]) });
  }
  $('season').onchange = async e => { S.season = e.target.value; await load(); render(); };
  $('team').onchange = e => { S.team = e.target.value; render(); };
  $('month').onchange = e => { S.month = e.target.value; render(); };
  $('extra').onchange = e => { S.extra = e.target.checked; render(); };
  $('close').onchange = e => { S.close = e.target.checked; render(); };
  await load(); render();
})();
