// ─────────────────────────────────────────────────────────────
// Translation System (i18n)
// ─────────────────────────────────────────────────────────────
type TranslationObject = { [key: string]: any };
let translations: { [lang: string]: TranslationObject } = {};
let currentLanguage: string = 'en';

async function loadTranslations(): Promise<void> {
    try {
        const response = await Promise.all([
            fetch('translations/en.json'),
            fetch('translations/hi.json'),
            fetch('translations/mr.json'),
        ]);
        
        const [enData, hiData, mrData] = await Promise.all(response.map(r => r.json()));
        translations = {
            'en': enData,
            'hi': hiData,
            'mr': mrData,
        };
        
        // Load saved language preference or default to 'en'
        const savedLang = localStorage.getItem('plantpal-language') || 'en';
        setLanguage(savedLang);
    } catch (err) {
        console.error('Failed to load translations:', err);
    }
}

function t(key: string, defaultValue?: string): string {
    const keys = key.split('.');
    let value: any = translations[currentLanguage] || translations['en'];
    
    for (const k of keys) {
        value = value?.[k];
        if (!value) return defaultValue || key;
    }
    
    return typeof value === 'string' ? value : (defaultValue || key);
}

function setLanguage(lang: string): void {
    if (!translations[lang]) {
        console.warn(`Language ${lang} not available, defaulting to English`);
        lang = 'en';
    }
    
    currentLanguage = lang;
    localStorage.setItem('plantpal-language', lang);
    
    // Update language selector
    const langSelect = document.getElementById('langSelect') as HTMLSelectElement;
    if (langSelect) langSelect.value = lang;
    
    // Update HTML lang attribute
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    
    // Translate all elements with data-i18n attribute
    translateDOM();
}

function translateDOM(): void {
    document.querySelectorAll('[data-i18n]').forEach((el) => {
        const key = el.getAttribute('data-i18n');
        if (key) {
            const translatedText = t(key);
            
            // Check if element has child elements (like button with span + svg)
            const textNode = Array.from(el.childNodes).find(
                node => node.nodeType === Node.TEXT_NODE || 
                        (node.nodeType === Node.ELEMENT_NODE && (node as HTMLElement).tagName === 'SPAN')
            );
            
            if (textNode && textNode.nodeType === Node.TEXT_NODE) {
                textNode.textContent = translatedText;
            } else if (el.tagName === 'BUTTON' && el.querySelector('span')) {
                // For buttons with child spans (like analyze button)
                const span = el.querySelector('span');
                if (span) span.textContent = translatedText;
            } else {
                el.textContent = translatedText;
            }
        }
    });
}

// ─────────────────────────────────────────────────────────────
// Interfaces (Defining the data structure from Python)
// ─────────────────────────────────────────────────────────────
interface PlantInfo {
    care_tips?: string[];
    treatment?: string[];
    prevention?: string[];
    what_is_it?: string;
    fun_fact?: string;
    severity?: string;
    urgency?: string;
    expert_note?: string;
}

interface ApiData {
    plant_name: string;
    condition: string;
    confidence: number;
    low_confidence: boolean;
    info: PlantInfo;
}

interface ApiResponse {
    success: boolean;
    data?: ApiData;
    error?: string;
}

interface ConditionRow {
    i: string;
    l: string;
    v: string;
    c: string;
}

interface MappedData {
    name: string;
    sci: string;
    status: 'healthy' | 'diseased';
    score: number;
    conf: number;
    conds: ConditionRow[];
    diag: string;
    recs: string[];
    lowConf: boolean;
    expertNote: string | null;
}

// ─────────────────────────────────────────────────────────────
// Config
// ─────────────────────────────────────────────────────────────
const API_URL: string = 'http://localhost:8000/analyze';

// ── Cursor ───────────────────────────────────────────────────
const c1 = document.getElementById('c1') as HTMLElement;
const c2 = document.getElementById('c2') as HTMLElement;
let mx = 0, my = 0, fx = 0, fy = 0;

document.addEventListener('mousemove', (e: MouseEvent) => {
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
const nav = document.getElementById('nav') as HTMLElement;
window.addEventListener('scroll', () => nav.classList.toggle('stuck', window.scrollY > 60));

// ── Scroll reveal ─────────────────────────────────────────────
const ro = new IntersectionObserver(
    (entries: IntersectionObserverEntry[]) => {
        entries.forEach(e => { 
            if (e.isIntersecting) e.target.classList.add('in'); 
        });
    },
    { threshold: 0.12 }
);
document.querySelectorAll('.reveal').forEach(el => ro.observe(el));

// ── File Upload ───────────────────────────────────────────────
const dz = document.getElementById('dz') as HTMLElement;
const fileIn = document.getElementById('fileIn') as HTMLInputElement;
const dzInner = document.getElementById('dzInner') as HTMLElement;
const dzPrev = document.getElementById('dzPrev') as HTMLElement;
const prevImg = document.getElementById('prevImg') as HTMLImageElement;
const analyzeBtn = document.getElementById('analyzeBtn') as HTMLButtonElement;

let selectedFile: File | null = null;

dz.addEventListener('dragover', (e: DragEvent) => { 
    e.preventDefault(); 
    dz.classList.add('over'); 
});

dz.addEventListener('dragleave', () => dz.classList.remove('over'));

dz.addEventListener('drop', (e: DragEvent) => {
    e.preventDefault(); 
    dz.classList.remove('over');
    if (e.dataTransfer && e.dataTransfer.files[0]) {
        const f = e.dataTransfer.files[0];
        if (f.type.startsWith('image/')) setFile(f);
    }
});

fileIn.addEventListener('change', (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        setFile(target.files[0]);
    }
});

function setFile(f: File): void {
    selectedFile = f;
    prevImg.src = URL.createObjectURL(f);
    dzInner.style.display = 'none';
    dzPrev.style.display = 'block';
    analyzeBtn.disabled = false;
    showEmpty();
}

// ── Analysis ─────────────────────────────────────────────────
analyzeBtn.addEventListener('click', runAnalysis);

async function runAnalysis(): Promise<void> {
    if (!selectedFile) return;

    analyzeBtn.disabled = true;
    (document.getElementById('btnTxt') as HTMLElement).textContent = t('results.analyzing');
    (document.getElementById('btnSpin') as HTMLElement).style.display = 'block';
    showLoading();

    const stepIds: string[] = ['ls1', 'ls2', 'ls3', 'ls4'];
    const stepKeys = ['results.step1', 'results.step2', 'results.step3', 'results.step4'];
    
    for (let i = 0; i < stepIds.length; i++) {
        await wait(700);
        if (i > 0) (document.getElementById(stepIds[i - 1]) as HTMLElement).classList.replace('active', 'done');
        const stepEl = document.getElementById(stepIds[i]) as HTMLElement;
        stepEl.classList.add('active');
        // Update step text
        const textEl = stepEl.lastChild as Node;
        if (textEl && textEl.nodeType === Node.TEXT_NODE) {
            textEl.textContent = t(stepKeys[i]);
        } else {
            const spans = stepEl.querySelectorAll('span');
            if (spans.length > 0) {
                spans[0].textContent = t(stepKeys[i]);
            }
        }
    }
    await wait(500);
    (document.getElementById('ls4') as HTMLElement).classList.replace('active', 'done');
    await wait(200);

    // Real API call to FastAPI backend
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch(API_URL, { method: 'POST', body: formData });
        const json: ApiResponse = await response.json();

        if (!json.success || !json.data) {
            throw new Error(json.error || 'Unknown error from server.');
        }

        showResult(mapApiResponse(json.data));
    } catch (err: any) {
        showError(err.message);
    }

    analyzeBtn.disabled = false;
    (document.getElementById('btnTxt') as HTMLElement).textContent = t('diagnose.btn');
    (document.getElementById('btnSpin') as HTMLElement).style.display = 'none';
}

// ── Map FastAPI response → display format ─────────────────────
function mapApiResponse(data: ApiData): MappedData {
    const isHealthy = data.condition.toLowerCase().includes('healthy');
    const conf = data.confidence;
    const score = isHealthy ? Math.round(conf) : Math.max(15, Math.round(100 - conf * 0.6));
    const info = data.info || {};

    const conds: ConditionRow[] = [
        { i: '🔬', l: 'Condition', v: data.condition, c: isHealthy ? 'g' : 'b' },
        { i: '📊', l: 'Confidence', v: conf.toFixed(1) + '%', c: data.low_confidence ? 'w' : 'g' },
    ];
    
    if (!isHealthy && info.severity) conds.push({ i: '⚠️', l: 'Severity', v: info.severity, c: 'b' });
    if (!isHealthy && info.urgency)  conds.push({ i: '⏰', l: 'Urgency', v: info.urgency, c: 'b' });

    let diag = '';
    if (isHealthy) {
        diag = info.fun_fact || 'Your plant looks healthy — keep up the great care!';
    } else {
        diag = info.what_is_it || `${data.condition} detected. Consult an agronomist for advice.`;
    }

    let recs: string[] = [];
    if (isHealthy) {
        recs = info.care_tips || ['Maintain your current care routine.'];
    } else {
        recs = info.treatment || ['Consult an agronomist for specific treatment advice.'];
        if (info.prevention) recs = [...recs, ...info.prevention];
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
function showResult(d: MappedData): void {
    hideEl('loadState');
    const panel = document.getElementById('resultsPanel') as HTMLElement;
    const rc = document.getElementById('resultContent') as HTMLElement;
    panel.style.alignItems = 'flex-start';
    rc.classList.add('show');

    (document.getElementById('rName') as HTMLElement).textContent = d.name;
    (document.getElementById('rSci') as HTMLElement).textContent = d.sci;

    const badge = document.getElementById('rBadge') as HTMLElement;
    badge.textContent = d.status === 'healthy' ? '✓ Healthy' : '⚠ Disease Detected';
    badge.className = 'status-badge ' + d.status;

    (document.getElementById('scoreConds') as HTMLElement).innerHTML = d.conds
        .map(c => `<div class="cond"><span class="cond-ico">${c.i}</span><span class="cond-lbl">${c.l}</span><span class="cond-v ${c.c}">${c.v}</span></div>`)
        .join('');

    const db = document.getElementById('diagBox') as HTMLElement;
    db.className = 'diag-box' + (d.status === 'diseased' ? ' sick' : '');
    (document.getElementById('diagLabel') as HTMLElement).textContent = d.status === 'healthy' ? '🌟 Did You Know?' : '📖 What Is This?';
    (document.getElementById('diagText') as HTMLElement).textContent = d.diag;

    (document.getElementById('recsLabel') as HTMLElement).textContent = d.status === 'healthy' ? '💧 Care Tips' : '🛠️ What To Do Right Now';
    (document.getElementById('recList') as HTMLElement).innerHTML = d.recs.map(r => `<li>${r}</li>`).join('');

    const expertNote = document.getElementById('expertNote') as HTMLElement;
    if (d.expertNote) {
        expertNote.style.display = 'block';
        expertNote.innerHTML = `<strong>👨‍🔬 Expert Note:</strong> <em>${d.expertNote}</em>`;
    } else {
        expertNote.style.display = 'none';
    }

    const lowConfWarn = document.getElementById('lowConfWarn') as HTMLElement;
    lowConfWarn.style.display = d.lowConf ? 'block' : 'none';

    (document.getElementById('confVal') as HTMLElement).textContent = d.conf + '%';
    setTimeout(() => (document.getElementById('confFill') as HTMLElement).style.width = d.conf + '%', 200);
    animScore(d.score);
}

function animScore(target: number): void {
    const circle = document.getElementById('scoreCircle') as HTMLElement;
    const numEl = document.getElementById('scoreNum') as HTMLElement;
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
function showEmpty(): void {
    (document.getElementById('emptyState') as HTMLElement).style.display = '';
    hideEl('loadState');
    (document.getElementById('resultContent') as HTMLElement).classList.remove('show');
    (document.getElementById('resultsPanel') as HTMLElement).style.alignItems = 'center';
}

function showLoading(): void {
    hideEl('emptyState');
    (document.getElementById('loadState') as HTMLElement).classList.add('show');
    (document.getElementById('resultContent') as HTMLElement).classList.remove('show');
    (document.getElementById('resultsPanel') as HTMLElement).style.alignItems = 'center';
    ['ls1', 'ls2', 'ls3', 'ls4'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('active', 'done');
    });
}

function showError(message: string): void {
    hideEl('loadState');
    const panel = document.getElementById('resultsPanel') as HTMLElement;
    panel.style.alignItems = 'center';
    panel.innerHTML = `
        <div style="text-align:center">
            <div style="font-size:3rem;margin-bottom:1rem">⚠️</div>
            <div class="error-box">${message}</div>
            <button class="reset-btn" style="margin:1.2rem auto 0" onclick="resetAll()">↩ Try again</button>
        </div>`;
}

function hideEl(id: string): void {
    const el = document.getElementById(id);
    if (!el) return;
    if (el.classList.contains('show')) el.classList.remove('show');
    else el.style.display = 'none';
}

// ── Reset ─────────────────────────────────────────────────────
(window as any).resetAll = resetAll; // Expose to global scope for HTML onclick
function resetAll(): void {
    selectedFile = null;
    fileIn.value = '';
    prevImg.src = '';
    dzInner.style.display = '';
    dzPrev.style.display = 'none';
    analyzeBtn.disabled = true;

    const panel = document.getElementById('resultsPanel') as HTMLElement;
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
function wait(ms: number): Promise<void> { 
    return new Promise(r => setTimeout(r, ms)); 
}

// ── Initialize on Page Load ────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
    // Load translations
    await loadTranslations();
    
    // Set up language selector
    const langSelect = document.getElementById('langSelect') as HTMLSelectElement;
    if (langSelect) {
        langSelect.addEventListener('change', (e) => {
            const target = e.target as HTMLSelectElement;
            setLanguage(target.value);
        });
    }
});

// Export functions for HTML onclick handlers
(window as any).setLanguage = setLanguage;
(window as any).toggleTheme = toggleTheme;
(window as any).resetAll = resetAll;
