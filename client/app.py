import streamlit as st

from server.analyzer import analyze_plant_image
from client.styles import STYLES, PAGE_JS
from client.sections import (
    CURSOR_NAV,
    HERO,
    FEATURES,
    HOW_IT_WORKS,
    DIAGNOSE_HEADER,
    DIAGNOSE_CLOSE,
    EMPTY_STATE,
    SDG_FOOTER,
)
from client.results import render_results


def run_client():
    st.set_page_config(
        page_title="PlantPal — Smart Plant Health Monitoring",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # ── Styles ───────────────────────────────────────────────────────────────
    st.markdown(STYLES, unsafe_allow_html=True)

    # ── All static sections + nav scroll JS in one block ────────────────────
    # Kept together so anchor links (#features, #how, #diagnose) share one DOM
    st.markdown(
        CURSOR_NAV + HERO + FEATURES + HOW_IT_WORKS + DIAGNOSE_HEADER + PAGE_JS,
        unsafe_allow_html=True,
    )

    # ── Two-column interactive area ──────────────────────────────────────────
    st.markdown('<div class="diag-columns">', unsafe_allow_html=True)
    col_upload, col_results = st.columns(2, gap="large")

    with col_upload:
        st.markdown(
            '<span style="font-size:.72rem;font-weight:700;letter-spacing:.1em;'
            'text-transform:uppercase;color:#b5f23d">📁 Upload Leaf Sample</span>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Drop your plant image here",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Leaf Sample", width="stretch")

        analyze_clicked = st.button(
            "🔬 Analyse Plant Health",
            disabled=(uploaded_file is None),
            use_container_width=True,
        )
        st.markdown(
            '<div class="upload-note" style="margin-top:.5rem">'
            "🔒 Images are processed locally and never stored</div>",
            unsafe_allow_html=True,
        )

    with col_results:
        if "analysis_results" not in st.session_state:
            st.session_state.analysis_results = None
        if "last_file" not in st.session_state:
            st.session_state.last_file = None

        if uploaded_file is not None and uploaded_file != st.session_state.last_file:
            st.session_state.last_file = uploaded_file
            st.session_state.analysis_results = None

        if analyze_clicked and uploaded_file is not None:
            with st.spinner("Analysing your plant…"):
                results = analyze_plant_image(uploaded_file)
            if results:
                st.session_state.analysis_results = results
            else:
                st.error("Model Error: Could not process the image.")

        if st.session_state.analysis_results:
            st.markdown(
                render_results(st.session_state.analysis_results),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(EMPTY_STATE, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(DIAGNOSE_CLOSE + SDG_FOOTER, unsafe_allow_html=True)


if __name__ == "__main__":
    run_client()