import streamlit as st
from pathlib import Path
import tempfile
import matplotlib.pyplot as plt

from main import run_matching, plot_strengths

# -------------------------
# Config page
# -------------------------
st.set_page_config(
    page_title="Smart Resume & Job Matcher",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Smart Resume & Job Matcher")
st.write(
    "Matching intelligent entre un CV et une offre d’emploi "
    "basé sur une compréhension sémantique multi-exécutions."
)

st.divider()

# -------------------------
# Upload fichiers
# -------------------------
st.subheader("1️⃣ Charger les fichiers")

cv_file = st.file_uploader("Uploader le CV (PDF)", type=["pdf"])
job_file = st.file_uploader("Uploader l'offre d'emploi (TXT ou PDF)", type=["txt", "pdf"])

st.divider()

# -------------------------
# Lancer analyse
# -------------------------
st.subheader("2️⃣ Lancer le matching")

run_button = st.button("🚀 Lancer l’analyse")

# -------------------------
# Traitement
# -------------------------
if run_button:
    if cv_file is None or job_file is None:
        st.error("⚠️ Veuillez uploader le CV et l'offre d'emploi.")
    else:
        with st.spinner("Analyse sémantique en cours (LLM + multi-runs)..."):
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_dir = Path(tmp_dir)

                cv_path = tmp_dir / cv_file.name
                job_path = tmp_dir / job_file.name

                cv_path.write_bytes(cv_file.getbuffer())
                job_path.write_bytes(job_file.getbuffer())

                scores_mean, scores_std, explanation = run_matching(
                    cv_path=cv_path,
                    job_path=job_path,
                    n_runs=5
                )

        st.success("✅ Analyse terminée")

        # -------------------------
        # Résultats globaux
        # -------------------------
        st.divider()
        st.subheader("📊 Résultats du matching")

        total_mean = scores_mean.get("total", 0)
        total_std = scores_std.get("total", 0)

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Matching global",
            f"{total_mean * 100:.1f} %",
            f"± {total_std * 100:.1f} %"
        )

        col2.metric(
            "Hard skills",
            f"{scores_mean.get('hard_skills', 0):.3f}"
        )

        col3.metric(
            "Soft skills",
            f"{scores_mean.get('soft_skills', 0):.3f}"
        )

        st.progress(min(max(total_mean, 0.0), 1.0))

        st.caption(
            "Score estimé à partir de plusieurs exécutions indépendantes. "
            "La variabilité reflète l’incertitude sémantique du modèle."
        )

        # -------------------------
        # Diagramme Forces / Faiblesses
        # -------------------------
        st.divider()
        st.subheader("📈 Analyse Forces / Faiblesses")

        fig = plot_strengths(scores_mean)
        st.pyplot(fig)

        # -------------------------
        # Explication IA
        # -------------------------
        st.divider()
        st.subheader("🧠 Explication IA")

        st.write(explanation)
