/* ── 1. CONFIG ── */
const API_URL        = '/analyze';
const ALLOWED_TYPES  = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_FILE_SIZE  = 10 * 1024 * 1024; // 10 MB

/* ── 2. TRANSLATIONS ── */
const translations = {
  en: {
    // Nav
    'nav.features':         'Features',
    'nav.how':              'How It Works',
    'nav.diagnose':         'Diagnose',
    // Hero
    'hero.badge':           'AI-Powered • Free',
    'hero.h1.line1':        'Know Your',
    'hero.h1.accent':       "Plant's",
    'hero.h1.ghost':        'Health',
    'hero.p':               "Snap a photo of any leaf. PlantPal's machine learning engine detects diseases and provides care plans instantly.",
    'hero.btn':             'Diagnose My Plant',
    'hero.stat1':           '38+',
    'hero.stat1_label':     'Diseases Detected',
    'hero.stat2':           '99%',
    'hero.stat2_label':     'Accuracy',
    'hero.stat3':           '3s',
    'hero.stat3_label':     'Analysis Time',
    // Features section
    'feat.eyebrow':         'Why PlantPal',
    'feat.heading':         'Everything your plant',
    'feat.heading.em':      'needs',
    'feat1.title':          'AI Diagnosis',
    'feat1.desc':           'Instantly identify 38+ plant diseases with our trained ML model, right from your browser.',
    'feat1.tag':            'ML Powered',
    'feat2.title':          'Treatment Plans',
    'feat2.desc':           "Get step-by-step care instructions tailored to your plant's specific condition.",
    'feat2.tag':            'Actionable',
    'feat3.title':          'Multilingual',
    'feat3.desc':           'Available in English, Hindi and Marathi so every farmer can access it.',
    'feat3.tag':            '3 Languages',
    'feat4.title':          'Instant Results',
    'feat4.desc':           'Analysis completes in under 3 seconds. No waiting, no sign-up required.',
    'feat4.tag':            'Free',
    // How It Works
    'how.eyebrow':          'Simple Process',
    'how.heading':          'Three steps to',
    'how.heading.em':       'clarity',
    'step1.n':              'Step 01',
    'step1.title':          'Snap a Photo',
    'step1.desc':           'Take a clear close-up of the affected leaf or upload one from your gallery.',
    'step2.n':              'Step 02',
    'step2.title':          'AI Analyses',
    'step2.desc':           'Our model scans for visual disease markers and calculates a health score.',
    'step3.n':              'Step 03',
    'step3.title':          'Get Your Report',
    'step3.desc':           'Receive a full diagnosis with confidence score, treatment plan, and prevention tips.',
    // Diagnose
    'diag.eyebrow':         'Try It Now',
    'diag.heading':         'Diagnose your',
    'diag.heading.em':      'plant',
    'dz.heading':           'Drop plant image here',
    'dz.sub':               'or',
    'dz.sub.strong':        'click to browse',
    'dz.hint':              'JPG · PNG · WEBP · max 10 MB',
    'btn.analyse':          '🔬 Analyse Plant Health',
    'btn.analysing':        'Analysing…',
    'upload.note':          '🔒 Images are never stored',
    'empty.h':              'No image yet',
    'empty.p':              'Upload a leaf photo to see the diagnosis report.',
    'loading.h':            'Analysing your plant…',
    'result.diag.label':    'Diagnosis',
    'result.conf.label':    'Confidence',
    'result.reset':         '↩ Try Another',
  },

  hi: {
    'nav.features':         'विशेषताएं',
    'nav.how':              'यह कैसे काम करता है',
    'nav.diagnose':         'निदान',
    'hero.badge':           'AI-संचालित • मुफ़्त',
    'hero.h1.line1':        'जानें अपने',
    'hero.h1.accent':       'पौधे का',
    'hero.h1.ghost':        'स्वास्थ्य',
    'hero.p':               'किसी भी पत्ते की फोटो लें। PlantPal का ML इंजन तुरंत बीमारियाँ पहचानता है और देखभाल योजना देता है।',
    'hero.btn':             'पौधा जांचें',
    'hero.stat1':           '38+',
    'hero.stat1_label':     'रोग पहचाने',
    'hero.stat2':           '99%',
    'hero.stat2_label':     'सटीकता',
    'hero.stat3':           '3s',
    'hero.stat3_label':     'विश्लेषण समय',
    'feat.eyebrow':         'PlantPal क्यों?',
    'feat.heading':         'आपके पौधे को चाहिए',
    'feat.heading.em':      'सब कुछ',
    'feat1.title':          'AI निदान',
    'feat1.desc':           'हमारे ML मॉडल से 38+ पौधों की बीमारियाँ तुरंत पहचानें।',
    'feat1.tag':            'ML आधारित',
    'feat2.title':          'उपचार योजना',
    'feat2.desc':           'आपके पौधे की स्थिति के अनुसार चरण-दर-चरण देखभाल निर्देश पाएं।',
    'feat2.tag':            'कार्यकारी',
    'feat3.title':          'बहुभाषी',
    'feat3.desc':           'अंग्रेजी, हिंदी और मराठी में उपलब्ध ताकि हर किसान उपयोग कर सके।',
    'feat3.tag':            '3 भाषाएं',
    'feat4.title':          'तत्काल परिणाम',
    'feat4.desc':           '3 सेकंड में विश्लेषण पूरा। कोई प्रतीक्षा नहीं, साइन-अप नहीं।',
    'feat4.tag':            'मुफ़्त',
    'how.eyebrow':          'सरल प्रक्रिया',
    'how.heading':          'तीन कदम',
    'how.heading.em':       'स्पष्टता की ओर',
    'step1.n':              'चरण 01',
    'step1.title':          'फोटो लें',
    'step1.desc':           'प्रभावित पत्ते की स्पष्ट क्लोज़-अप फोटो लें।',
    'step2.n':              'चरण 02',
    'step2.title':          'AI विश्लेषण',
    'step2.desc':           'हमारा मॉडल रोग के दृश्य संकेत खोजकर स्वास्थ्य स्कोर देता है।',
    'step3.n':              'चरण 03',
    'step3.title':          'रिपोर्ट पाएं',
    'step3.desc':           'पूरा निदान, विश्वास स्कोर, उपचार योजना और रोकथाम के सुझाव पाएं।',
    'diag.eyebrow':         'अभी आज़माएं',
    'diag.heading':         'अपने पौधे का',
    'diag.heading.em':      'निदान करें',
    'dz.heading':           'पौधे की छवि यहाँ डालें',
    'dz.sub':               'या',
    'dz.sub.strong':        'ब्राउज़ करें',
    'dz.hint':              'JPG · PNG · WEBP · अधिकतम 10 MB',
    'btn.analyse':          '🔬 पौधे का स्वास्थ्य जांचें',
    'btn.analysing':        'विश्लेषण हो रहा है…',
    'upload.note':          '🔒 छवियाँ कभी संग्रहीत नहीं होतीं',
    'empty.h':              'कोई छवि नहीं',
    'empty.p':              'निदान रिपोर्ट देखने के लिए पत्ते की फोटो अपलोड करें।',
    'loading.h':            'आपके पौधे का विश्लेषण हो रहा है…',
    'result.diag.label':    'निदान',
    'result.conf.label':    'विश्वास',
    'result.reset':         '↩ दूसरा प्रयास करें',
  },

  mr: {
    'nav.features':         'वैशिष्ट्ये',
    'nav.how':              'हे कसे कार्य करते',
    'nav.diagnose':         'निदान',
    'hero.badge':           'AI-चालित • मोफत',
    'hero.h1.line1':        'जाणा तुमच्या',
    'hero.h1.accent':       'झाडाचे',
    'hero.h1.ghost':        'आरोग्य',
    'hero.p':               'कोणत्याही पानाचा फोटो घ्या. PlantPal चे ML इंजिन लगेच रोग ओळखते आणि काळजी योजना देते.',
    'hero.btn':             'झाड तपासा',
    'hero.stat1':           '38+',
    'hero.stat1_label':     'रोग ओळखले',
    'hero.stat2':           '99%',
    'hero.stat2_label':     'अचूकता',
    'hero.stat3':           '3s',
    'hero.stat3_label':     'विश्लेषण वेळ',
    'feat.eyebrow':         'PlantPal का?',
    'feat.heading':         'तुमच्या झाडाला लागते',
    'feat.heading.em':      'सगळे काही',
    'feat1.title':          'AI निदान',
    'feat1.desc':           'आमच्या ML मॉडेलद्वारे 38+ झाडांचे रोग त्वरित ओळखा.',
    'feat1.tag':            'ML आधारित',
    'feat2.title':          'उपचार योजना',
    'feat2.desc':           'तुमच्या झाडाच्या स्थितीनुसार टप्प्याटप्प्याने काळजी सूचना मिळवा.',
    'feat2.tag':            'कृती करण्यायोग्य',
    'feat3.title':          'बहुभाषिक',
    'feat3.desc':           'इंग्रजी, हिंदी आणि मराठीत उपलब्ध.',
    'feat3.tag':            '3 भाषा',
    'feat4.title':          'त्वरित निकाल',
    'feat4.desc':           '3 सेकंदात विश्लेषण पूर्ण. कोणतीही प्रतीक्षा नाही.',
    'feat4.tag':            'मोफत',
    'how.eyebrow':          'सोपी प्रक्रिया',
    'how.heading':          'तीन पायऱ्या',
    'how.heading.em':       'स्पष्टतेकडे',
    'step1.n':              'पायरी 01',
    'step1.title':          'फोटो घ्या',
    'step1.desc':           'बाधित पानाचा स्पष्ट क्लोज-अप फोटो घ्या.',
    'step2.n':              'पायरी 02',
    'step2.title':          'AI विश्लेषण',
    'step2.desc':           'आमचे मॉडेल रोगाची दृश्य चिन्हे शोधते आणि आरोग्य गुण देते.',
    'step3.n':              'पायरी 03',
    'step3.title':          'अहवाल मिळवा',
    'step3.desc':           'पूर्ण निदान, आत्मविश्वास गुण, उपचार योजना आणि प्रतिबंध टिप्स मिळवा.',
    'diag.eyebrow':         'आत्ता वापरून पहा',
    'diag.heading':         'तुमच्या झाडाचे',
    'diag.heading.em':      'निदान करा',
    'dz.heading':           'झाडाची प्रतिमा येथे टाका',
    'dz.sub':               'किंवा',
    'dz.sub.strong':        'ब्राउज़ करा',
    'dz.hint':              'JPG · PNG · WEBP · कमाल 10 MB',
    'btn.analyse':          '🔬 झाडाचे आरोग्य तपासा',
    'btn.analysing':        'विश्लेषण होत आहे…',
    'upload.note':          '🔒 प्रतिमा कधीच साठवल्या जात नाहीत',
    'empty.h':              'कोणतीही प्रतिमा नाही',
    'empty.p':              'निदान अहवाल पाहण्यासाठी पानाचा फोटो अपलोड करा.',
    'loading.h':            'तुमच्या झाडाचे विश्लेषण होत आहे…',
    'result.diag.label':    'निदान',
    'result.conf.label':    'आत्मविश्वास',
    'result.reset':         '↩ दुसरा प्रयत्न करा',
  }
};

/* ── 3. STATE ── */
let currentLanguage = localStorage.getItem('plantpal-lang') || 'en';
let file = null;

/* ── 4. LANGUAGE ── */
function t(key) {
  const lang = translations[currentLanguage];
  return (lang && lang[key]) || translations['en'][key] || key;
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.getAttribute('data-i18n'));
  });
  // Also refresh the analyse button if it's not mid-analysis
  const btn = document.getElementById('analyzeBtn');
  if (btn && document.getElementById('btnSpin').style.display !== 'block') {
    document.getElementById('btnTxt').textContent = t('btn.analyse');
  }
}

function setLanguage(lang) {
  if (!translations[lang]) return;
  currentLanguage = lang;
  localStorage.setItem('plantpal-lang', lang);
  document.getElementById('langSelect').value = lang;
  applyTranslations();
}

/* ── 5. THEME ── */
function toggleTheme() {
  const html     = document.documentElement;
  const current  = html.getAttribute('data-theme') || 'dark';
  const next     = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('plantpal-theme', next);
  document.getElementById('themeToggle').textContent = next === 'dark' ? '🌙' : '☀️';
}

/* ── 6. LOADING STATE HELPERS ── */
function showLoading() {
  document.getElementById('emptyState').style.display    = 'none';
  document.getElementById('resultContent').classList.remove('show');
  document.getElementById('loadState').classList.add('show');
}

function hideLoading() {
  document.getElementById('loadState').classList.remove('show');
}

/* ── 7. FILE HANDLING ── */
function validateAndSetFile(f) {
  if (!ALLOWED_TYPES.includes(f.type)) {
    alert('Please upload a JPG, PNG or WEBP image.');
    return;
  }
  if (f.size > MAX_FILE_SIZE) {
    alert('File is too large. Maximum size is 10 MB.');
    return;
  }
  file = f;
  document.getElementById('prevImg').src           = URL.createObjectURL(f);
  document.getElementById('dzInner').style.display = 'none';
  document.getElementById('dzPrev').style.display  = 'block';
  document.getElementById('analyzeBtn').disabled   = false;
}

/* ── 8. ANALYSIS ── */
async function runAnalysis() {
  if (!file) return;

  const btn = document.getElementById('analyzeBtn');
  btn.disabled = true;
  document.getElementById('btnSpin').style.display = 'block';
  document.getElementById('btnTxt').textContent    = t('btn.analysing');

  showLoading();

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(API_URL, { method: 'POST', body: formData });
    if (!response.ok) throw new Error(`Server error: ${response.status}`);
    const json = await response.json();
    if (json.success) {
      showResult(json.data);
    } else {
      throw new Error(json.error || 'Unknown error');
    }
  } catch (err) {
    hideLoading();
    document.getElementById('emptyState').style.display = 'block';
    alert('Analysis failed: ' + err.message);
  } finally {
    btn.disabled = false;
    document.getElementById('btnSpin').style.display = 'none';
    document.getElementById('btnTxt').textContent    = t('btn.analyse');
  }
}

/* ── 9. SHOW RESULT ── */
function showResult(data) {
  hideLoading();
  const info = data.info || {}; // Access the rich data from treatments.py

  // 1. Header & Status
  // Uses the specific display name (e.g., "Apple — Cedar Apple Rust")
  document.getElementById('rName').textContent = info.display_name || data.plant_name;
  document.getElementById('rSci').textContent  = info.urgency || data.condition;

  const isHealthy = data.condition.toLowerCase().includes('healthy');
  const badge = document.getElementById('rBadge');
  
  // Displays severity emoji and text (e.g., "🟡 Moderate")
  badge.textContent = isHealthy ? '✓ Healthy' : `⚠ ${info.severity || 'Disease Detected'}`;
  badge.className = 'status-badge ' + (isHealthy ? 'healthy' : 'diseased');

  // 2. Score Circle
  const score = Math.round(data.confidence);
  const circum = 2 * Math.PI * 35;
  document.getElementById('scoreNum').textContent = score + '%';
  document.getElementById('scoreCircle').style.strokeDashoffset = circum - (score / 100) * circum;

  // 3. Detailed Diagnosis & Treatment Report
  // We use innerHTML to render the <ul> and <li> tags for the lists
  let reportHtml = `<div class="report-section">
                      <strong>What is it:</strong>
                      <p>${info.what_is_it || data.condition}</p>
                    </div>`;

  // Dynamically build the Treatment list
  if (info.treatment && info.treatment.length > 0) {
    reportHtml += `<div class="report-section">
                    <strong>Treatment Plan:</strong>
                    <ul>${info.treatment.map(step => `<li>${step}</li>`).join('')}</ul>
                   </div>`;
  }

  // Dynamically build the Prevention list
  if (info.prevention && info.prevention.length > 0) {
    reportHtml += `<div class="report-section">
                    <strong>Prevention:</strong>
                    <ul>${info.prevention.map(step => `<li>${step}</li>`).join('')}</ul>
                   </div>`;
  }

  // Highlight the Expert Note if it exists
  if (info.expert_note) {
    reportHtml += `<div class="expert-note">
                     <strong>Expert Note:</strong> ${info.expert_note}
                   </div>`;
  }

  document.getElementById('diagText').innerHTML = reportHtml;
  document.getElementById('diagBox').className = 'diag-box' + (isHealthy ? '' : ' sick');

  // 4. Confidence Bar
  document.getElementById('confFill').style.width = score + '%';
  document.getElementById('confVal').textContent = score + '%';

  document.getElementById('resultContent').classList.add('show');
}

/* ── 10. RESET ── */
function resetAll() {
  file = null;
  document.getElementById('dzInner').style.display = 'block';
  document.getElementById('dzPrev').style.display  = 'none';
  document.getElementById('fileIn').value          = '';
  document.getElementById('analyzeBtn').disabled   = true;
  document.getElementById('resultContent').classList.remove('show');
  document.getElementById('loadState').classList.remove('show');
  document.getElementById('emptyState').style.display = 'block';
}

/* ── 11. INIT ── */
document.addEventListener('DOMContentLoaded', () => {

  // Restore theme
  const savedTheme = localStorage.getItem('plantpal-theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  document.getElementById('themeToggle').textContent = savedTheme === 'dark' ? '🌙' : '☀️';

  // Restore language
  const savedLang = localStorage.getItem('plantpal-lang') || 'en';
  document.getElementById('langSelect').value = savedLang;
  currentLanguage = savedLang;
  applyTranslations();

  // Sticky nav
  window.addEventListener('scroll', () => {
    document.getElementById('nav').classList.toggle('stuck', window.scrollY > 20);
  });

  // Scroll reveal
  const ro = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); });
  }, { threshold: 0.05 });
  document.querySelectorAll('.reveal').forEach(el => ro.observe(el));

  // File input
  document.getElementById('fileIn').addEventListener('change', e => {
    if (e.target.files[0]) validateAndSetFile(e.target.files[0]);
  });

  // Drag-and-drop
  const dz = document.getElementById('dz');
  dz.addEventListener('dragover',  e => { e.preventDefault(); dz.classList.add('over'); });
  dz.addEventListener('dragleave', () => dz.classList.remove('over'));
  dz.addEventListener('drop', e => {
    e.preventDefault();
    dz.classList.remove('over');
    if (e.dataTransfer.files[0]) validateAndSetFile(e.dataTransfer.files[0]);
  });

  // Analyse button
  document.getElementById('analyzeBtn').addEventListener('click', runAnalysis);
});