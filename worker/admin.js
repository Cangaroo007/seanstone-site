/**
 * The private record. Server-rendered, no framework, no client JS beyond a
 * filter box — this page exists to be read quickly on a phone, not admired.
 *
 * Gated by HTTP basic auth against the ADMIN_PASSWORD secret. That is a thin
 * lock: it is one password over TLS with no rate limiting beyond Cloudflare's
 * own, which is proportionate for a list of enquiries and would not be for
 * anything more sensitive.
 */

const CSS = `
:root{color-scheme:light dark;--paper:#E8EBE7;--ink:#101513;--soft:#38413C;--muted:#5D665F;
  --rule:rgba(16,21,19,.14);--card:#F6F8F4;--accent:#0E6E63;--signal:#C2551E}
@media(prefers-color-scheme:dark){:root{--paper:#0B0F0D;--ink:#E6EBE7;--soft:#C2CBC5;
  --muted:#8D978F;--rule:rgba(230,235,231,.16);--card:#141A17;--accent:#5FC9BC;--signal:#E8834A}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:15px/1.5 ui-sans-serif,-apple-system,Segoe UI,sans-serif;padding:24px 20px 80px}
h1{font-size:22px;margin:0 0 4px;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:13px;margin:0 0 22px}
.tabs{display:flex;gap:8px;margin-bottom:18px;flex-wrap:wrap}
.tabs a{text-decoration:none;font:12px/1 ui-monospace,Menlo,monospace;letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted);border:1px solid var(--rule);border-radius:999px;padding:8px 14px}
.tabs a.on{background:var(--ink);color:var(--paper);border-color:var(--ink)}
#q{width:100%;max-width:420px;font:15px/1.4 inherit;color:var(--ink);background:var(--card);
  border:1px solid var(--rule);border-radius:6px;padding:11px 14px;margin-bottom:18px}
.row{border:1px solid var(--rule);border-left:3px solid var(--rule);border-radius:6px;
  background:var(--card);padding:16px 18px;margin-bottom:12px}
.row.hot{border-left-color:var(--signal)}
.row.enq{border-left-color:var(--accent)}
.top{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;justify-content:space-between;margin-bottom:8px}
.who{font-weight:600;font-size:16px}
.who a{color:var(--accent)}
.when{font:11px/1 ui-monospace,Menlo,monospace;color:var(--muted);white-space:nowrap}
.facts{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.f{font:11px/1.4 ui-monospace,Menlo,monospace;border:1px solid var(--rule);border-radius:3px;
  padding:4px 8px;color:var(--soft)}
.f b{color:var(--ink);font-weight:600}
.msg{white-space:pre-wrap;font:12.5px/1.6 ui-monospace,Menlo,monospace;color:var(--soft);
  background:var(--paper);border:1px solid var(--rule);border-radius:5px;padding:12px;margin-top:10px;
  max-height:260px;overflow:auto}
.none{color:var(--muted);padding:40px 0;text-align:center}
.err{color:var(--signal)}
`;

const esc = (s) =>
  String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function when(ts) {
  try {
    const d = new Date(ts);
    const mins = Math.round((Date.now() - d.getTime()) / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return mins + 'm ago';
    if (mins < 1440) return Math.round(mins / 60) + 'h ago';
    return d.toISOString().slice(0, 16).replace('T', ' ') + 'Z';
  } catch (e) { return ts; }
}

function facts(pairs) {
  return '<div class="facts">' + pairs
    .filter((p) => p[1] !== null && p[1] !== undefined && p[1] !== '' && p[1] !== 0)
    .map((p) => `<span class="f">${esc(p[0])} <b>${esc(p[1])}</b></span>`)
    .join('') + '</div>';
}

function enquiryRow(r) {
  const who = r.email
    ? `<a href="mailto:${esc(r.email)}">${esc(r.email)}</a>`
    : '<span style="color:var(--muted)">no address given</span>';
  return `<div class="row enq">
    <div class="top"><div class="who">${who}</div><div class="when">${esc(when(r.ts))}</div></div>
    <div style="font-size:14px;color:var(--soft)">${esc(r.subject || '')}</div>
    ${facts([['company', r.company], ['city', r.city], ['country', r.country],
             ['network', r.network], ['segment', r.segment], ['score', r.score],
             ['read', r.depth ? r.depth + '%' : ''], ['weakest', r.weakzone],
             ['scope', r.scopehours ? r.scopehours + 'h' : ''], ['asked', r.asked],
             ['from', r.referrer]])}
    ${r.body ? `<div class="msg">${esc(r.body)}</div>` : ''}
  </div>`;
}

function sessionRow(r) {
  const who = r.company
    ? esc(r.company)
    : (r.city ? esc(r.city) : 'Unidentified visitor');
  return `<div class="row hot">
    <div class="top"><div class="who">${who}</div><div class="when">${esc(when(r.ts))}</div></div>
    <div style="font-size:14px;color:var(--soft)">${esc(r.stage || '')}</div>
    ${facts([['score', r.score], ['city', r.city], ['country', r.country],
             ['network', r.network], ['segment', r.segment],
             ['read', r.depth ? r.depth + '%' : ''], ['minutes', r.minutes],
             ['visit', r.visits], ['weakest', r.weakzone],
             ['scope', r.scopehours ? r.scopehours + 'h' : ''],
             ['asked', r.asked], ['signals', r.signals], ['from', r.referrer]])}
    ${r.nba ? `<div class="msg">${esc(r.nba)}</div>` : ''}
  </div>`;
}

export function unauthorised() {
  return new Response('Authentication required.', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="seanstone", charset="UTF-8"',
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
}

export function authorised(request, env) {
  if (!env.ADMIN_PASSWORD) { return false; }
  const h = request.headers.get('Authorization') || '';
  if (!h.startsWith('Basic ')) { return false; }
  let decoded = '';
  try { decoded = atob(h.slice(6)); } catch (e) { return false; }
  const given = decoded.slice(decoded.indexOf(':') + 1);
  // Length-independent comparison. Not a defence against a determined attacker
  // — the rest of this endpoint isn't either — but free to do correctly.
  const a = new TextEncoder().encode(given);
  const b = new TextEncoder().encode(env.ADMIN_PASSWORD);
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) {
    diff |= (a[i] || 0) ^ (b[i] || 0);
  }
  return diff === 0;
}

export async function render(request, env) {
  const url = new URL(request.url);
  const view = url.searchParams.get('v') === 'sessions' ? 'sessions' : 'enquiries';

  let rows = [], error = '';
  if (!env.DB) {
    error = 'No D1 database is bound to this Worker, so nothing has been stored yet.';
  } else {
    try {
      const sql = view === 'sessions'
        ? 'SELECT * FROM sessions ORDER BY id DESC LIMIT 300'
        : 'SELECT * FROM enquiries ORDER BY id DESC LIMIT 300';
      const res = await env.DB.prepare(sql).all();
      rows = res.results || [];
    } catch (e) {
      error = 'Query failed: ' + (e && e.message ? e.message : 'unknown') +
              ' — has schema.sql been applied?';
    }
  }

  const body = rows.map(view === 'sessions' ? sessionRow : enquiryRow).join('');
  const tab = (v, label) =>
    `<a class="${view === v ? 'on' : ''}" href="?v=${v}">${label}</a>`;

  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Record — seanstone.com</title><style>${CSS}</style></head><body>
<h1>The record</h1>
<p class="sub">${rows.length} most recent, newest first. Not indexed, not linked from the site.</p>
<div class="tabs">${tab('enquiries', 'Enquiries')}${tab('sessions', 'Hot sessions')}
<a href="https://seanstone.com/" style="margin-left:auto">The site &rarr;</a></div>
${error ? `<p class="none err">${esc(error)}</p>` : ''}
<input id="q" placeholder="Filter — company, city, email, anything" autocomplete="off">
${body || (error ? '' : '<p class="none">Nothing here yet.</p>')}
<script>
document.getElementById('q').addEventListener('input', function(){
  var t = this.value.toLowerCase();
  document.querySelectorAll('.row').forEach(function(r){
    r.style.display = !t || r.textContent.toLowerCase().indexOf(t) >= 0 ? '' : 'none';
  });
});
</script>
</body></html>`;

  return new Response(html, {
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}
