"use strict";
// ─────────────────────────────────────────────────────────────
// Config
// ─────────────────────────────────────────────────────────────
const API_URL = 'http://localhost:8000/analyze';
// ── Cursor ───────────────────────────────────────────────────
const c1 = document.getElementById('c1');
const c2 = document.getElementById('c2');
let mx = 0, my = 0, fx = 0, fy = 0;
document.addEventListener('mousemove', (e) => {
    mx = e.clientX;
    my = e.clientY;
    c1.style.left = mx + 'px';
    c1.style.top = my + 'px';
});
(function tick() {
    fx += (mx - fx) * 0.12;
    fy += (my - fy) * 0.12;
    c2.style.left = fx + 'px';
    c2.style.top = fy + 'px';
    requestAnimationFrame(tick);
})();
// ── Nav scroll effect ─────────────────────────────────────────
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => nav.classList.toggle('stuck', window.scrollY > 60));
// ── Scroll reveal ─────────────────────────────────────────────
const ro = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting)
            e.target.classList.add('in');
    });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => ro.observe(el));
// ── File Upload ───────────────────────────────────────────────
const dz = document.getElementById('dz');
const fileIn = document.getElementById('fileIn');
const dzInner = document.getElementById('dzInner');
const dzPrev = document.getElementById('dzPrev');
const prevImg = document.getElementById('prevImg');
const analyzeBtn = document.getElementById('analyzeBtn');
let selectedFile = null;
dz.addEventListener('dragover', (e) => {
    e.preventDefault();
    dz.classList.add('over');
});
dz.addEventListener('dragleave', () => dz.classList.remove('over'));
dz.addEventListener('drop', (e) => {
    e.preventDefault();
    dz.classList.remove('over');
    if (e.dataTransfer && e.dataTransfer.files[0]) {
        const f = e.dataTransfer.files[0];
        if (f.type.startsWith('image/'))
            setFile(f);
    }
});
fileIn.addEventListener('change', (e) => {
    const target = e.target;
    if (target.files && target.files[0]) {
        setFile(target.files[0]);
    }
});
function setFile(f) {
    selectedFile = f;
    prevImg.src = URL.createObjectURL(f);
    dzInner.style.display = 'none';
    dzPrev.style.display = 'block';
    analyzeBtn.disabled = false;
    showEmpty();
}
// ── Analysis ─────────────────────────────────────────────────
analyzeBtn.addEventListener('click', runAnalysis);
async function runAnalysis() {
    if (!selectedFile)
        return;
    analyzeBtn.disabled = true;
    document.getElementById('btnTxt').textContent = 'Analysing…';
    document.getElementById('btnSpin').style.display = 'block';
    showLoading();
    const stepIds = ['ls1', 'ls2', 'ls3', 'ls4'];
    for (let i = 0; i < stepIds.length; i++) {
        await wait(700);
        if (i > 0)
            document.getElementById(stepIds[i - 1]).classList.replace('active', 'done');
        document.getElementById(stepIds[i]).classList.add('active');
    }
    await wait(500);
    document.getElementById('ls4').classList.replace('active', 'done');
    await wait(200);
    // Real API call to FastAPI backend
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        const response = await fetch(API_URL, { method: 'POST', body: formData });
        const json = await response.json();
        if (!json.success || !json.data) {
            throw new Error(json.error || 'Unknown error from server.');
        }
        showResult(mapApiResponse(json.data));
    }
    catch (err) {
        showError(err.message);
    }
    analyzeBtn.disabled = false;
    document.getElementById('btnTxt').textContent = 'Analyse Plant Health';
    document.getElementById('btnSpin').style.display = 'none';
}
// ── Map FastAPI response → display format ─────────────────────
function mapApiResponse(data) {
    const isHealthy = data.condition.toLowerCase().includes('healthy');
    const conf = data.confidence;
    const score = isHealthy ? Math.round(conf) : Math.max(15, Math.round(100 - conf * 0.6));
    const info = data.info || {};
    const conds = [
        { i: '🔬', l: 'Condition', v: data.condition, c: isHealthy ? 'g' : 'b' },
        { i: '📊', l: 'Confidence', v: conf.toFixed(1) + '%', c: data.low_confidence ? 'w' : 'g' },
    ];
    if (!isHealthy && info.severity)
        conds.push({ i: '⚠️', l: 'Severity', v: info.severity, c: 'b' });
    if (!isHealthy && info.urgency)
        conds.push({ i: '⏰', l: 'Urgency', v: info.urgency, c: 'b' });
    let diag = '';
    if (isHealthy) {
        diag = info.fun_fact || 'Your plant looks healthy — keep up the great care!';
    }
    else {
        diag = info.what_is_it || `${data.condition} detected. Consult an agronomist for advice.`;
    }
    let recs = [];
    if (isHealthy) {
        recs = info.care_tips || ['Maintain your current care routine.'];
    }
    else {
        recs = info.treatment || ['Consult an agronomist for specific treatment advice.'];
        if (info.prevention)
            recs = [...recs, ...info.prevention];
    }
    return {
        name: data.plant_name,
        sci: 'Detected via PlantPal Neural Network',
        status: isHealthy ? 'healthy' : 'diseased',
        score,
        conf: Math.round(conf),
        conds,
        diag,
        recs,
        lowConf: data.low_confidence,
        expertNote: info.expert_note || null,
    };
}
// ── Render result ─────────────────────────────────────────────
function showResult(d) {
    hideEl('loadState');
    const panel = document.getElementById('resultsPanel');
    const rc = document.getElementById('resultContent');
    panel.style.alignItems = 'flex-start';
    rc.classList.add('show');
    document.getElementById('rName').textContent = d.name;
    document.getElementById('rSci').textContent = d.sci;
    const badge = document.getElementById('rBadge');
    badge.textContent = d.status === 'healthy' ? '✓ Healthy' : '⚠ Disease Detected';
    badge.className = 'status-badge ' + d.status;
    document.getElementById('scoreConds').innerHTML = d.conds
        .map(c => `<div class="cond"><span class="cond-ico">${c.i}</span><span class="cond-lbl">${c.l}</span><span class="cond-v ${c.c}">${c.v}</span></div>`)
        .join('');
    const db = document.getElementById('diagBox');
    db.className = 'diag-box' + (d.status === 'diseased' ? ' sick' : '');
    document.getElementById('diagLabel').textContent = d.status === 'healthy' ? '🌟 Did You Know?' : '📖 What Is This?';
    document.getElementById('diagText').textContent = d.diag;
    document.getElementById('recsLabel').textContent = d.status === 'healthy' ? '💧 Care Tips' : '🛠️ What To Do Right Now';
    document.getElementById('recList').innerHTML = d.recs.map(r => `<li>${r}</li>`).join('');
    const expertNote = document.getElementById('expertNote');
    if (d.expertNote) {
        expertNote.style.display = 'block';
        expertNote.innerHTML = `<strong>👨‍🔬 Expert Note:</strong> <em>${d.expertNote}</em>`;
    }
    else {
        expertNote.style.display = 'none';
    }
    const lowConfWarn = document.getElementById('lowConfWarn');
    lowConfWarn.style.display = d.lowConf ? 'block' : 'none';
    document.getElementById('confVal').textContent = d.conf + '%';
    setTimeout(() => document.getElementById('confFill').style.width = d.conf + '%', 200);
    animScore(d.score);
}
function animScore(target) {
    const circle = document.getElementById('scoreCircle');
    const numEl = document.getElementById('scoreNum');
    const circ = 220;
    let n = 0;
    const t = setInterval(() => {
        n = Math.min(n + 1, target);
        numEl.textContent = n.toString();
        circle.style.strokeDashoffset = (circ - (circ * n / 100)).toString();
        if (n >= target) {
            clearInterval(t);
            circle.style.stroke = target >= 75 ? '#b5f23d' : target >= 50 ? '#fbbf24' : '#f87171';
        }
    }, 14);
}
// ── States ────────────────────────────────────────────────────
function showEmpty() {
    document.getElementById('emptyState').style.display = '';
    hideEl('loadState');
    document.getElementById('resultContent').classList.remove('show');
    document.getElementById('resultsPanel').style.alignItems = 'center';
}
function showLoading() {
    hideEl('emptyState');
    document.getElementById('loadState').classList.add('show');
    document.getElementById('resultContent').classList.remove('show');
    document.getElementById('resultsPanel').style.alignItems = 'center';
    ['ls1', 'ls2', 'ls3', 'ls4'].forEach(id => {
        const el = document.getElementById(id);
        if (el)
            el.classList.remove('active', 'done');
    });
}
function showError(message) {
    hideEl('loadState');
    const panel = document.getElementById('resultsPanel');
    panel.style.alignItems = 'center';
    panel.innerHTML = `
        <div style="text-align:center">
            <div style="font-size:3rem;margin-bottom:1rem">⚠️</div>
            <div class="error-box">${message}</div>
            <button class="reset-btn" style="margin:1.2rem auto 0" onclick="resetAll()">↩ Try again</button>
        </div>`;
}
function hideEl(id) {
    const el = document.getElementById(id);
    if (!el)
        return;
    if (el.classList.contains('show'))
        el.classList.remove('show');
    else
        el.style.display = 'none';
}
// ── Reset ─────────────────────────────────────────────────────
window.resetAll = resetAll; // Expose to global scope for HTML onclick
function resetAll() {
    selectedFile = null;
    fileIn.value = '';
    prevImg.src = '';
    dzInner.style.display = '';
    dzPrev.style.display = 'none';
    analyzeBtn.disabled = true;
    const panel = document.getElementById('resultsPanel');
    panel.innerHTML = `
        <div class="empty-state" id="emptyState">
            <div class="empty-ico">🌱</div>
            <div class="empty-h">No plant analysed yet</div>
            <p class="empty-p">Upload a leaf photo and hit<br>
                <strong style="color:rgba(255,255,255,.4)">Analyse Plant Health</strong>
                to see your full report here.</p>
        </div>
        <div class="loading-state" id="loadState">
            <div class="scanner">
                <div class="scanner-ring"></div><div class="scanner-ring"></div><div class="scanner-ring"></div>
                <div class="scanner-core">🌿</div>
                <div class="scan-line"></div>
            </div>
            <div class="loading-h">Analysing your plant…</div>
            <div class="loading-steps">
                <div class="lstep" id="ls1"><div class="lstep-dot"></div> Identifying plant species…</div>
                <div class="lstep" id="ls2"><div class="lstep-dot"></div> Scanning for diseases…</div>
                <div class="lstep" id="ls3"><div class="lstep-dot"></div> Calculating health score…</div>
                <div class="lstep" id="ls4"><div class="lstep-dot"></div> Generating care plan…</div>
            </div>
        </div>
        <div class="result-content" id="resultContent">
            <div class="result-header">
                <div class="result-plant">
                    <h3 id="rName">—</h3>
                    <p id="rSci">—</p>
                </div>
                <div class="status-badge" id="rBadge">—</div>
            </div>
            <div class="score-row">
                <div class="score-circle">
                    <svg viewBox="0 0 90 90" width="90" height="90">
                        <circle class="track" cx="45" cy="45" r="35"/>
                        <circle class="fill" id="scoreCircle" cx="45" cy="45" r="35"/>
                    </svg>
                    <div class="score-inner">
                        <span id="scoreNum">0</span>
                        <span>Health</span>
                    </div>
                </div>
                <div class="score-conds" id="scoreConds"></div>
            </div>
            <div class="diag-box" id="diagBox">
                <div class="diag-label" id="diagLabel">Diagnosis</div>
                <p id="diagText">—</p>
            </div>
            <div class="recs-box">
                <div class="recs-label" id="recsLabel">Care Recommendations</div>
                <ul class="rec-list" id="recList"></ul>
            </div>
            <div class="low-conf-warn" id="lowConfWarn" style="display:none">
                ⚠️ Low confidence — try a clearer, well-lit photo for better accuracy.
            </div>
            <div class="low-conf-warn" id="expertNote" style="display:none;background:rgba(255,255,255,0.05);color:#e5e7eb"></div>
            <div class="conf-row">
                <span>Model Confidence</span>
                <div class="conf-track"><div class="conf-fill" id="confFill"></div></div>
                <span class="conf-val" id="confVal">—</span>
            </div>
            <button class="reset-btn" onclick="resetAll()">↩ Analyse another plant</button>
        </div>`;
    panel.style.alignItems = 'center';
}
// ── Utility ───────────────────────────────────────────────────
function wait(ms) {
    return new Promise(r => setTimeout(r, ms));
}
