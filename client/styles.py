STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

/* ── Hide Streamlit chrome ── */
#MainMenu, header[data-testid="stHeader"], footer[data-testid="stFooter"],
.stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppViewBlockContainer"] > div > div > div:first-child { display: none !important; }
.stApp { background: #060d08 !important; }
.block-container, .stMainBlockContainer { padding: 0 !important; max-width: 100% !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }
div[data-testid="stVerticalBlockBorderWrapper"] { padding: 0 !important; }

/* ── Design System ── */
*{ box-sizing: border-box; }
:root {
  --bg:#060d08; --card:#0c1a10; --card2:#101f14;
  --border:rgba(255,255,255,.07); --lime:#b5f23d;
  --lime-dim:rgba(181,242,61,.12); --lime-glow:rgba(181,242,61,.25);
  --mint:#4ade80; --white:#fff; --muted:rgba(255,255,255,.38);
  --muted2:rgba(255,255,255,.55); --red:#f87171; --amber:#fbbf24;
}
html { scroll-behavior: smooth; }
body { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg); color: var(--white); overflow-x: hidden; }
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: var(--lime); border-radius: 4px; }

/* ── Nav ── */
nav { position:fixed;top:0;inset-inline:0;z-index:200;padding:1.6rem 5%;display:flex;align-items:center;justify-content:space-between;transition:all .4s; }
nav.stuck { background:rgba(6,13,8,.9);backdrop-filter:blur(24px);padding:1rem 5%;border-bottom:1px solid var(--border); }
.logo { font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:800;letter-spacing:-.02em;display:flex;align-items:center;gap:.4rem; }
.logo em { color:var(--lime);font-style:normal; }
.logo-icon { width:28px;height:28px;background:var(--lime);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:.9rem; }
nav ul { display:flex;gap:2.5rem;list-style:none; }
nav ul a { color:var(--muted);font-size:.85rem;font-weight:500;text-decoration:none;transition:color .2s; }
nav ul a:hover { color:var(--white); }
.nav-cta { background:var(--lime);color:#060d08;border:none;padding:.55rem 1.4rem;border-radius:8px;font-family:'Plus Jakarta Sans',sans-serif;font-weight:600;font-size:.85rem;cursor:pointer;transition:all .2s; }
.nav-cta:hover { transform:translateY(-2px);box-shadow:0 8px 30px var(--lime-glow); }

/* ── Hero ── */
#hero { min-height:100vh;display:flex;align-items:center;padding:0 5%;position:relative;overflow:hidden; }
.hero-canvas { position:absolute;inset:0;pointer-events:none; }
.hero-canvas::before { content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(181,242,61,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(181,242,61,.03) 1px,transparent 1px);background-size:80px 80px; }
.hero-canvas::after { content:'';position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(181,242,61,.06) 0%,transparent 65%);top:-300px;right:-200px; }
.hero-inner { display:grid;grid-template-columns:1.1fr .9fr;gap:5rem;align-items:center;width:100%;position:relative;z-index:2; }
.hero-left { animation:up .8s cubic-bezier(.16,1,.3,1) both; }
.hero-right { animation:up .8s .15s cubic-bezier(.16,1,.3,1) both; }
@keyframes up { from{opacity:0;transform:translateY(50px)}to{opacity:1;transform:translateY(0)} }
h1 { font-family:'Syne',sans-serif;font-size:clamp(3.8rem,5.5vw,6rem);font-weight:800;line-height:.95;letter-spacing:-.04em;margin-bottom:1.8rem; }
h1 .accent { color:var(--lime); }
h1 .ghost { color:transparent;-webkit-text-stroke:1px rgba(255,255,255,.18); }
.hero-p { color:var(--muted2);font-size:1.05rem;line-height:1.8;font-weight:400;max-width:450px;margin-bottom:2.8rem; }
.btns { display:flex;gap:1rem;align-items:center;margin-bottom:4rem; }
.btn-main { display:inline-flex;align-items:center;gap:.6rem;background:var(--lime);color:#060d08;border:none;padding:.9rem 2.2rem;border-radius:10px;font-family:'Plus Jakarta Sans',sans-serif;font-weight:600;font-size:.95rem;cursor:pointer;transition:all .25s; }
.btn-main:hover { transform:translateY(-3px);box-shadow:0 20px 50px rgba(181,242,61,.35); }
.btn-main svg { width:15px;transition:transform .3s; }
.btn-main:hover svg { transform:translateX(4px); }
.btn-ghost { color:var(--muted);font-size:.9rem;font-weight:500;text-decoration:none;display:flex;align-items:center;gap:.4rem;transition:color .2s; }
.btn-ghost:hover { color:var(--white); }
.stats-row { display:flex;gap:3rem; }
.stat-n { font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:var(--lime);line-height:1;letter-spacing:-.04em; }
.stat-l { font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;margin-top:.3rem; }

/* ── Hero Card ── */
.hero-card-wrap { position:relative;padding:30px; }
.hcard { background:linear-gradient(145deg,rgba(255,255,255,.05),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.09);border-radius:24px;padding:2rem;backdrop-filter:blur(10px);animation:levitate 6s ease-in-out infinite;box-shadow:0 30px 80px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.08); }
@keyframes levitate { 0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-16px) rotate(.5deg)} }
.hcard-top { display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem; }
.hcard-plant { display:flex;align-items:center;gap:.8rem; }
.plant-thumb { width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#1a4d28,#2d7a42);display:flex;align-items:center;justify-content:center;font-size:1.4rem; }
.plant-name { font-weight:700;font-size:.95rem; }
.plant-sci { font-size:.75rem;color:var(--muted);font-style:italic; }
.health-chip { background:rgba(74,222,128,.12);border:1px solid rgba(74,222,128,.25);color:#4ade80;padding:.3rem .8rem;border-radius:100px;font-size:.72rem;font-weight:700;white-space:nowrap; }
/* Hero card donut score */
.hcard-score-wrap { display:flex;align-items:center;gap:1.2rem;margin-bottom:1.5rem; }
.hcard-score-circle { position:relative;width:90px;height:90px;flex-shrink:0; }
.hcard-score-circle svg { transform:rotate(-90deg); }
.hcs-track { fill:none;stroke:rgba(255,255,255,.06);stroke-width:7; }
.hcs-fill { fill:none;stroke:#b5f23d;stroke-width:7;stroke-linecap:round;stroke-dasharray:220;stroke-dashoffset:13; }
.hcs-inner { position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center; }
.hcs-num { font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;line-height:1;color:#b5f23d; }
.hcs-lbl { font-size:.55rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em; }
.hcard-conds { display:flex;flex-direction:column;gap:.4rem;flex:1; }
.hcond { display:flex;align-items:center;gap:.5rem;font-size:.8rem; }
.hcond-lbl { color:var(--muted);flex:1; }
.hcond-v { font-weight:700; }
.hcond-v.g { color:#4ade80; }
.hcond-v.w { color:var(--amber); }
.hcond-v.b { color:var(--red); }
.disease-tag { background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.2);border-radius:10px;padding:.7rem 1rem;display:flex;align-items:center;gap:.6rem; }
.disease-icon { font-size:1rem; }
.disease-text { font-size:.78rem;color:#fbbf24;font-weight:600;line-height:1.4; }
/* chips contained within the card, no overflow positioning */
.chip-float { display:inline-flex;align-items:center;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:100px;padding:.45rem 1rem;font-size:.75rem;font-weight:600;backdrop-filter:blur(10px);white-space:nowrap;margin-bottom:.75rem;margin-right:.5rem; }
.chip1 { color:var(--lime);border-color:rgba(181,242,61,.2); }
.chip2 { color:var(--mint);border-color:rgba(74,222,128,.2); }

/* ── Features ── */
#features { padding:8rem 5%;background:var(--bg);position:relative; }
#features::before { content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(181,242,61,.015) 0%,transparent 50%);pointer-events:none; }
.eyebrow { font-size:.72rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--lime);text-align:center;margin-bottom:.8rem; }
.section-h { font-family:'Syne',sans-serif;font-size:clamp(2.2rem,3.5vw,3.2rem);font-weight:800;letter-spacing:-.04em;text-align:center;line-height:1.1;margin-bottom:4rem; }
.section-h em { color:var(--lime);font-style:italic;font-family:'Plus Jakarta Sans',sans-serif;font-weight:300; }
.feat-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;max-width:1200px;margin:0 auto; }
.feat { background:var(--card);border:1px solid var(--border);border-radius:20px;padding:2rem 1.8rem;position:relative;overflow:hidden;transition:all .35s;cursor:default; }
.feat::before { content:'';position:absolute;inset:0;background:linear-gradient(135deg,var(--lime-dim),transparent);opacity:0;transition:opacity .35s; }
.feat:hover { border-color:rgba(181,242,61,.2);transform:translateY(-8px);box-shadow:0 30px 60px rgba(0,0,0,.4); }
.feat:hover::before { opacity:1; }
.feat-num { font-family:'Syne',sans-serif;font-size:3.5rem;font-weight:800;color:rgba(181,242,61,.06);line-height:1;position:absolute;top:1.2rem;right:1.5rem;letter-spacing:-.06em; }
.feat-ico { width:52px;height:52px;background:var(--lime-dim);border:1px solid rgba(181,242,61,.15);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin-bottom:1.4rem; }
.feat h3 { font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;margin-bottom:.7rem;letter-spacing:-.01em; }
.feat p { color:var(--muted);font-size:.85rem;line-height:1.65; }
.feat-tag { display:inline-block;margin-top:1.2rem;font-size:.68rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--lime);background:var(--lime-dim);border-radius:4px;padding:.25rem .6rem; }

/* ── How It Works ── */
#how { padding:8rem 5%;background:linear-gradient(180deg,var(--bg) 0%,var(--card) 50%,var(--bg) 100%); }
.steps { display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;max-width:1000px;margin:0 auto;position:relative; }
.steps::before { content:'';position:absolute;top:3.5rem;left:calc(16.67% + 1rem);right:calc(16.67% + 1rem);height:1px;background:linear-gradient(90deg,transparent,rgba(181,242,61,.3),transparent); }
.step { text-align:center;padding:2.5rem 2rem;background:var(--card2);border:1px solid var(--border);border-radius:20px;position:relative;transition:all .3s; }
.step:hover { border-color:rgba(181,242,61,.2);transform:translateY(-6px); }
.step-n { font-family:'Syne',sans-serif;font-size:.72rem;font-weight:800;color:var(--lime);letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.2rem; }
.step-ico-wrap { width:70px;height:70px;border-radius:50%;background:var(--lime-dim);border:1px solid rgba(181,242,61,.15);display:flex;align-items:center;justify-content:center;font-size:2rem;margin:0 auto 1.5rem; }
.step h3 { font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:.7rem; }
.step p { color:var(--muted);font-size:.85rem;line-height:1.65; }

/* ── Diagnose ── */
#diagnose { padding:8rem 5%;background:var(--bg); }
.results-panel { background:var(--card);border:1px solid var(--border);border-radius:24px;padding:2.5rem;min-height:500px;display:flex;align-items:center;justify-content:center; }
.empty-state { text-align:center; }
.empty-ico { font-size:4rem;opacity:.25;filter:grayscale(1);margin-bottom:1rem; }
.empty-h { font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:rgba(255,255,255,.3);margin-bottom:.5rem; }
.empty-p { color:rgba(255,255,255,.2);font-size:.82rem;line-height:1.6; }
.upload-note { color:rgba(255,255,255,.2);font-size:.75rem;text-align:center;display:flex;align-items:center;justify-content:center;gap:.4rem; }

/* ── Results ── */
.result-content { display:flex;flex-direction:column;gap:1.5rem;width:100%; }
.result-header { display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:1.2rem;border-bottom:1px solid var(--border); }
.result-plant h3 { font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.2rem; }
.result-plant p { color:var(--muted);font-size:.8rem;font-style:italic; }
.status-badge { padding:.4rem 1rem;border-radius:100px;font-size:.75rem;font-weight:700;letter-spacing:.04em; }
.status-badge.healthy { background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.25);color:#4ade80; }
.status-badge.diseased { background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.25);color:var(--red); }
.score-row { display:flex;align-items:center;gap:1.5rem; }
.score-circle { position:relative;width:90px;height:90px;flex-shrink:0; }
.score-circle svg { transform:rotate(-90deg); }
.score-circle .track { fill:none;stroke:rgba(255,255,255,.06);stroke-width:7; }
.score-circle .fill { fill:none;stroke:var(--lime);stroke-width:7;stroke-linecap:round;stroke-dasharray:220;transition:stroke-dashoffset 1.5s cubic-bezier(.34,1.56,.64,1); }
.score-inner { position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center; }
.score-inner span:first-child { font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;line-height:1;color:var(--lime); }
.score-inner span:last-child { font-size:.55rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em; }
.score-conds { display:flex;flex-direction:column;gap:.4rem;flex:1; }
.cond { display:flex;align-items:center;gap:.6rem;font-size:.82rem; }
.cond-ico { font-size:.9rem; }
.cond-lbl { color:var(--muted);flex:1; }
.cond-v { font-weight:700; }
.cond-v.g { color:#4ade80; }
.cond-v.w { color:var(--amber); }
.cond-v.b { color:var(--red); }
.diag-box { background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:12px;padding:1rem 1.2rem;border-left:3px solid var(--lime); }
.diag-box.sick { border-left-color:var(--red); }
.diag-label { font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.4rem; }
.diag-box p { color:var(--muted2);font-size:.85rem;line-height:1.65; }
.recs-label { font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:.7rem; }
.rec-list { list-style:none;display:flex;flex-direction:column;gap:.4rem;padding:0; }
.rec-list li { display:flex;gap:.6rem;font-size:.83rem;color:var(--muted2);line-height:1.55; }
.rec-list li::before { content:'→';color:var(--lime);flex-shrink:0;font-weight:700; }
.conf-row { display:flex;align-items:center;gap:.8rem;font-size:.78rem;color:var(--muted); }
.conf-track { flex:1;height:4px;background:rgba(255,255,255,.07);border-radius:4px; }
.conf-fill { height:100%;background:linear-gradient(90deg,var(--lime),var(--mint));border-radius:4px;transition:width 1.2s ease; }
.conf-val { font-weight:700;color:var(--lime); }
.low-conf-warn { background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.2);border-radius:10px;padding:.7rem 1rem;font-size:.8rem;color:var(--amber);font-weight:600; }

/* ── SDG ── */
#sdg { padding:5rem 5%;background:var(--card); }
.sdg-inner { max-width:900px;margin:0 auto;display:grid;grid-template-columns:1fr auto;gap:4rem;align-items:center; }
.sdg-label { font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--lime);margin-bottom:.7rem; }
.sdg-inner h3 { font-family:'Syne',sans-serif;font-size:1.7rem;font-weight:800;letter-spacing:-.03em;margin-bottom:.8rem;line-height:1.2; }
.sdg-inner > div > p { color:var(--muted);font-size:.88rem;line-height:1.7; }
.sdg-pills { display:flex;flex-direction:column;gap:.6rem; }
.sdg-pill { display:flex;align-items:center;gap:.6rem;background:rgba(181,242,61,.06);border:1px solid rgba(181,242,61,.12);border-radius:100px;padding:.5rem 1rem;font-size:.78rem;font-weight:600;color:var(--lime);white-space:nowrap; }

/* ── Footer ── */
footer { background:var(--bg);border-top:1px solid var(--border);padding:3rem 5%;text-align:center; }
.footer-logo { font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.5rem; }
.footer-logo span { color:var(--lime); }
.footer-tagline { font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:1.5rem; }
.footer-team { color:rgba(255,255,255,.4);font-size:.82rem;margin-bottom:.3rem; }
.footer-team strong { color:rgba(255,255,255,.6); }
.footer-bottom { color:rgba(255,255,255,.2);font-size:.75rem;margin-top:.5rem; }

/* ── Streamlit Widget Overrides ── */
[data-testid="stFileUploader"] { background: transparent !important; }
[data-testid="stFileUploader"] > div {
  background: rgba(181,242,61,.02) !important;
  border: 2px dashed rgba(181,242,61,.2) !important;
  border-radius: 16px !important;
  padding: 2rem !important;
  transition: all .3s !important;
}
[data-testid="stFileUploader"] > div:hover {
  border-color: #b5f23d !important;
  background: rgba(181,242,61,.12) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] { color: rgba(255,255,255,.55) !important; }
[data-testid="stFileUploaderDropzoneInstructions"] span { color: #b5f23d !important; }
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-primary"] {
  background: linear-gradient(135deg,#b5f23d,#8fcf2a) !important;
  color: #060d08 !important; border: none !important;
  border-radius: 12px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important; font-size: 1rem !important;
  padding: 0.75rem 1.5rem !important;
  transition: all .3s !important; width: 100% !important;
}
[data-testid="stBaseButton-secondary"]:hover, [data-testid="stBaseButton-primary"]:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 16px 40px rgba(181,242,61,.3) !important;
  background: linear-gradient(135deg,#c5ff52,#9fdf3a) !important;
}
[data-testid="stBaseButton-secondary"]:disabled {
  opacity: .35 !important; cursor: not-allowed !important;
  transform: none !important; box-shadow: none !important;
}
[data-testid="stSpinner"] p { color: var(--lime) !important; }
[data-testid="stImage"] img { border-radius: 12px; border: 1px solid rgba(181,242,61,.15); width: 100% !important; height: 220px; object-fit: cover; }
.diag-columns [data-testid="stHorizontalBlock"] { gap: 1.5rem !important; max-width: 1100px; margin: 0 auto; padding: 0 5%; }
.diag-columns [data-testid="stHorizontalBlock"] > div:first-child,
.diag-columns [data-testid="stHorizontalBlock"] > div:last-child {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 24px; padding: 2.5rem !important;
}

/* ── Scroll reveal: always visible — JS cannot reach across Streamlit iframes ── */
.reveal { opacity:1; transform:none; }
.reveal[data-d="1"] { }
.reveal[data-d="2"] { }
.reveal[data-d="3"] { }
.reveal[data-d="4"] { }

/* ── Responsive ── */
@media(max-width:1024px) {
  .hero-inner { grid-template-columns:1fr;gap:3rem; }
  .hero-right { display:none; }
  .feat-grid { grid-template-columns:1fr 1fr; }
}
@media(max-width:768px) {
  nav { padding:1rem 5%; }
  nav ul,.nav-cta { display:none; }
  h1 { font-size:3rem; }
  .feat-grid { grid-template-columns:1fr; }
  .steps { grid-template-columns:1fr; }
  .steps::before { display:none; }
  .sdg-inner { grid-template-columns:1fr; }
}
</style>
"""

PAGE_JS = """
<script>
// Nav scroll effect — works because nav is in the same st.markdown DOM
const nav = document.getElementById('nav');
if (nav) {
  window.addEventListener('scroll', () =>
    nav.classList.toggle('stuck', window.scrollY > 60)
  );
}
</script>
"""