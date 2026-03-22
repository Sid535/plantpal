CURSOR_NAV = """
<nav id="nav">
<div class="logo"><div class="logo-icon">🌿</div>Plant<em>Pal</em></div>
<ul>
<li><a href="#features">Features</a></li>
<li><a href="#how">How It Works</a></li>
<li><a href="#diagnose">Diagnose</a></li>
</ul>
<button class="nav-cta" onclick="document.getElementById('diagnose').scrollIntoView({behavior:'smooth'})">Try For Free</button>
</nav>
"""

HERO = (
'<section id="hero">'
'<div class="hero-canvas"></div>'
'<div class="hero-inner">'

'<div class="hero-left">'
'<h1>Know Your<br><span class="accent">Plant\'s</span><br><span class="ghost">Health</span></h1>'
'<p class="hero-p">Snap a photo of any leaf. PlantPal\'s machine learning engine detects diseases, scores health, and gives you a personalised care plan — instantly.</p>'
'<div class="btns">'
'<button class="btn-main" onclick="document.getElementById(\'diagnose\').scrollIntoView({behavior:\'smooth\'})">'
'<span>Diagnose My Plant</span>'
'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
'</button>'
'<a href="#how" class="btn-ghost">See how it works '
'<svg width="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 9l-7 7-7-7"/></svg>'
'</a>'
'</div>'
'<div class="stats-row">'
'<div class="stat-item"><div class="stat-n">38+</div><div class="stat-l">Diseases Detected</div></div>'
'<div class="stat-item"><div class="stat-n">95%</div><div class="stat-l">Accuracy Rate</div></div>'
'<div class="stat-item"><div class="stat-n">&lt;3s</div><div class="stat-l">Avg. Analysis</div></div>'
'</div>'
'</div>'

'<div class="hero-right">'
'<div class="hero-card-wrap">'
'<div style="margin-bottom:.75rem">'
'<span class="chip-float chip1">🔬 ML Powered</span>'
'<span class="chip-float chip2">⚡ Instant Results</span>'
'</div>'
'<div class="hcard">'

'<div class="hcard-top">'
'<div class="hcard-plant">'
'<div class="plant-thumb" style="background:linear-gradient(135deg,#1a4d1a,#2d7a2d)">🍅</div>'
'<div><div class="plant-name">Tomato</div><div class="plant-sci">Solanum lycopersicum</div></div>'
'</div>'
'<div class="health-chip">✓ Healthy</div>'
'</div>'

'<div class="hcard-score-wrap">'
'<div class="hcard-score-circle">'
'<svg viewBox="0 0 90 90" width="90" height="90">'
'<circle class="hcs-track" cx="45" cy="45" r="35"/>'
'<circle class="hcs-fill" cx="45" cy="45" r="35"/>'
'</svg>'
'<div class="hcs-inner"><span class="hcs-num">94</span><span class="hcs-lbl">Health</span></div>'
'</div>'
'<div class="hcard-conds">'
'<div class="hcond"><span>💧</span><span class="hcond-lbl">Watering</span><span class="hcond-v g">Good</span></div>'
'<div class="hcond"><span>☀️</span><span class="hcond-lbl">Sunlight</span><span class="hcond-v g">Optimal</span></div>'
'<div class="hcond"><span>🌱</span><span class="hcond-lbl">Growth</span><span class="hcond-v g">Active</span></div>'
'</div>'
'</div>'

'<div class="disease-tag" style="background:rgba(74,222,128,.06);border-color:rgba(74,222,128,.2)">'
'<div class="disease-icon">✅</div>'
'<div class="disease-text" style="color:#4ade80">No disease detected — plant is in excellent condition.</div>'
'</div>'

'</div>'
'</div>'
'</div>'
'</div>'
'</section>'
)

FEATURES = (
'<section id="features">'
'<p class="eyebrow">What PlantPal Can Do</p>'
'<h2 class="section-h">Built for every <em>plant parent</em></h2>'
'<div class="feat-grid">'
'<div class="feat"><div class="feat-num">01</div><div class="feat-ico">🔬</div><h3>Disease Detection</h3>'
'<p>Our CNN model scans leaf images for fungal, bacterial, and viral infections with clinical-level precision.</p>'
'<div class="feat-tag">Image Classification</div></div>'
'<div class="feat"><div class="feat-num">02</div><div class="feat-ico">💊</div><h3>Smart Care Tips</h3>'
'<p>Get condition-specific guidance — watering schedules, treatments, and fertiliser advice personalised to your plant\'s state.</p>'
'<div class="feat-tag">AI Recommendations</div></div>'
'<div class="feat"><div class="feat-num">03</div><div class="feat-ico">🌿</div><h3>14 Plant Species</h3>'
'<p>Tomatoes, apples, grapes, corn, potatoes and more — PlantPal recognises every species in the PlantVillage dataset.</p>'
'<div class="feat-tag">Multi-Species</div></div>'
'<div class="feat"><div class="feat-num">04</div><div class="feat-ico">📊</div><h3>Health Scoring</h3>'
'<p>Get a clear health percentage score, confidence metrics, and visual indicators — no jargon, just clarity.</p>'
'<div class="feat-tag">Visual Analytics</div></div>'
'</div>'
'</section>'
)

HOW_IT_WORKS = (
'<section id="how">'
'<p class="eyebrow">The Process</p>'
'<h2 class="section-h">Three steps to a <em>healthier plant</em></h2>'
'<div class="steps">'
'<div class="step"><div class="step-n">Step 01</div><div class="step-ico-wrap">📷</div>'
'<h3>Upload a Leaf Photo</h3><p>Drag &amp; drop or browse your device. Works with any clear photo of a plant leaf.</p></div>'
'<div class="step"><div class="step-n">Step 02</div><div class="step-ico-wrap">🤖</div>'
'<h3>ML Model Analyses</h3><p>TensorFlow scans the image, identifies the species, and checks for 38+ known diseases.</p></div>'
'<div class="step"><div class="step-n">Step 03</div><div class="step-ico-wrap">✅</div>'
'<h3>Get Your Report</h3><p>Receive a full health report with diagnosis, health score, and a personalised care plan.</p></div>'
'</div>'
'</section>'
)

DIAGNOSE_HEADER = (
'<section id="diagnose" style="padding:8rem 5% 2rem;background:var(--bg)">'
'<p class="eyebrow">Try It Now</p>'
'<h2 class="section-h" style="margin-bottom:2rem">Upload a leaf, get <em>instant answers</em></h2>'
'</section>'
)

DIAGNOSE_CLOSE = '<div style="padding:0 0 8rem;background:var(--bg)"></div>'

EMPTY_STATE = (
'<div class="results-panel">'
'<div class="empty-state">'
'<div class="empty-ico">🌱</div>'
'<div class="empty-h">No plant analysed yet</div>'
'<p class="empty-p">Upload a leaf photo and hit<br>'
'<strong style="color:rgba(255,255,255,.4)">Analyse Plant Health</strong>'
' to see your full report here.</p>'
'</div>'
'</div>'
)

SDG_FOOTER = (
'<section id="sdg"><div class="sdg-inner">'
'<div>'
'<div class="sdg-label">🌍 SDG 12 Alignment</div>'
'<h3>Fighting plant waste through early detection</h3>'
'<p>PlantPal supports Responsible Consumption &amp; Production by catching disease before it spreads — cutting down on water overuse, excessive fertilisers, and preventable plant loss.</p>'
'</div>'
'<div class="sdg-pills">'
'<div class="sdg-pill">♻️ Reduces plant waste</div>'
'<div class="sdg-pill">💧 Saves water</div>'
'<div class="sdg-pill">🌱 Sustainable care</div>'
'</div>'
'</div></section>'
'<footer>'
'<div class="footer-logo">Plant<span>Pal</span></div>'
'<div class="footer-tagline">Smart Plant Health Monitoring</div>'
'<div class="footer-team">Made with 🌱 by <strong>TE_A_12</strong> — Karunya Ingale · Yash Jikamade · Swastik Mahajan · Siddesh Koli</div>'
'<div class="footer-team" style="margin-top:.3rem">Guide: <strong>Prof. Snehal Mali</strong></div>'
'<div class="footer-bottom">Powered by TensorFlow · Streamlit · Pandas · NumPy</div>'
'</footer>'
)