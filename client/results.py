def render_results(r: dict) -> str:
    """Convert analyzer output dict into a styled HTML results panel."""

    is_healthy = "healthy" in r["condition"].lower()
    status_class = "healthy" if is_healthy else "diseased"
    badge_text = "✓ Healthy" if is_healthy else "⚠ Disease Detected"

    # Health score: reflect confidence when healthy; penalise when diseased
    conf = r["confidence"]
    score = int(conf) if is_healthy else max(15, 100 - int(conf * 0.6))
    score_color = "#b5f23d" if score >= 75 else "#fbbf24" if score >= 50 else "#f87171"
    stroke_offset = f"{220 - (220 * score / 100):.1f}"

    # Condition pill colours
    conf_class = "g" if not r["low_confidence"] else "w"
    health_class = "g" if is_healthy else "b"

    # Treatment text → bullet list items
    lines = [ln.strip().strip("-•").strip() for ln in r["treatment"].split("\n") if ln.strip()]
    if not lines:
        lines = [r["treatment"]]
    recs_html = "".join(f"<li>{line}</li>" for line in lines)

    # Optional low-confidence warning
    low_conf_html = ""
    if r["low_confidence"]:
        low_conf_html = (
            '<div class="low-conf-warn">'
            "⚠️ Low confidence — try a clearer, well-lit photo for better accuracy."
            "</div>"
        )

    diagnosis_text = (
        "Your plant looks healthy — no disease or infection detected. Keep up the good work!"
        if is_healthy
        else f"{r['condition']} detected. Review the care recommendations below and act promptly to prevent further spread."
    )

    # NOTE: NO leading whitespace before the opening <div.
    # st.markdown treats 4-space-indented lines as code blocks,
    # which would render the HTML as raw text instead of rendering it.
    return (
        f'<div class="results-panel" style="align-items:flex-start">'
        f'<div class="result-content">'

        f'<div class="result-header">'
        f'<div class="result-plant">'
        f'<h3>{r["plant_name"]}</h3>'
        f'<p>Detected via PlantPal Neural Network</p>'
        f'</div>'
        f'<div class="status-badge {status_class}">{badge_text}</div>'
        f'</div>'

        f'<div class="score-row">'
        f'<div class="score-circle">'
        f'<svg viewBox="0 0 90 90" width="90" height="90">'
        f'<circle class="track" cx="45" cy="45" r="35"/>'
        f'<circle class="fill" cx="45" cy="45" r="35"'
        f' stroke="{score_color}"'
        f' stroke-dasharray="220"'
        f' stroke-dashoffset="{stroke_offset}"/>'
        f'</svg>'
        f'<div class="score-inner">'
        f'<span style="color:{score_color}">{score}</span>'
        f'<span>Health</span>'
        f'</div>'
        f'</div>'
        f'<div class="score-conds">'
        f'<div class="cond"><span class="cond-ico">🔬</span>'
        f'<span class="cond-lbl">Condition</span>'
        f'<span class="cond-v {health_class}">{r["condition"]}</span></div>'
        f'<div class="cond"><span class="cond-ico">📊</span>'
        f'<span class="cond-lbl">Confidence</span>'
        f'<span class="cond-v {conf_class}">{conf:.1f}%</span></div>'
        f'<div class="cond">'
        f'<span class="cond-ico">{"✅" if is_healthy else "⚠️"}</span>'
        f'<span class="cond-lbl">Status</span>'
        f'<span class="cond-v {health_class}">{"No Disease" if is_healthy else "Needs Care"}</span>'
        f'</div>'
        f'</div>'
        f'</div>'

        f'<div class="diag-box {"" if is_healthy else "sick"}">'
        f'<div class="diag-label">Diagnosis</div>'
        f'<p>{diagnosis_text}</p>'
        f'</div>'

        f'<div class="recs-box">'
        f'<div class="recs-label">Care Recommendations</div>'
        f'<ul class="rec-list">{recs_html}</ul>'
        f'</div>'

        f'<div class="conf-row">'
        f'<span>Model Confidence</span>'
        f'<div class="conf-track">'
        f'<div class="conf-fill" style="width:{int(conf)}%"></div>'
        f'</div>'
        f'<span class="conf-val">{int(conf)}%</span>'
        f'</div>'

        f'{low_conf_html}'
        f'</div>'
        f'</div>'
    )