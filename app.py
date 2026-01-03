import streamlit as st
from pathlib import Path
import tempfile

from main import run_matching
from plot_utils import plot_strengths

st.set_page_config(
    page_title="Smart Resume & Job Matcher",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Smart Resume & Job Matcher")
st.write(
    "Comparaison de deux représentations (structurée vs full-text) "
    "pour un matching CV / offre robuste."
)

st.divider()

cv_file = st.file_uploader("Uploader le CV (PDF)", type=["pdf"])
job_file = st.file_uploader("Uploader l'offre (TXT ou PDF)", type=["txt", "pdf"])

run_button = st.button("🚀 Lancer l’analyse")

if run_button:
    if not cv_file or not job_file:
        st.error("Veuillez uploader les deux fichiers.")
    else:
        with st.spinner("Analyse en cours..."):
            with tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                cv_path = tmp / cv_file.name
                job_path = tmp / job_file.name
                cv_path.write_bytes(cv_file.getbuffer())
                job_path.write_bytes(job_file.getbuffer())

                result = run_matching(cv_path, job_path, n_runs=5)

        st.success("Analyse terminée")

        scores = result["scores_mean"]
        std = result["scores_std"]

        st.metric(
            "Matching global",
            f"{scores.get('total', 0) * 100:.1f} %",
            f"± {std.get('total', 0) * 100:.1f} %"
        )

        st.progress(scores.get("total", 0))

        st.divider()
        st.subheader("🔍 Comparaison des deux approches")

        tab1, tab2 = st.tabs(["🧠 Structuré (LLM)", "📄 Full-text"])

        with tab1:
            st.markdown("### CV")
            st.json(result["cv_structured"])
            st.markdown("### Offre")
            st.json(result["job_structured"])

        with tab2:
            st.markdown("### CV")
            st.text(result["cv_full_view"])
            st.markdown("### Offre")
            st.text(result["job_full_view"])

        st.divider()
        st.subheader("📈 Analyse Forces / Faiblesses")
        fig = plot_strengths(scores)
        st.pyplot(fig)

        st.divider()
        st.subheader("🧠 Explication IA")
        st.write(result["explanation"])
