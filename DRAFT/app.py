# app.py

import streamlit as st
import tempfile
from pathlib import Path

from main import run_matching


st.set_page_config(
    page_title="Smart Resume & Job Matcher",
    layout="centered"
)

st.title("📄 Smart Resume & Job Matcher")
st.subheader("Matching intelligent entre un CV et une offre d’emploi")

# =========================
# Upload files
# =========================
st.markdown("### 1️⃣ Charger les fichiers")

cv_file = st.file_uploader(
    "Uploader le CV (PDF)",
    type=["pdf"]
)

job_file = st.file_uploader(
    "Uploader l'offre d'emploi (TXT ou PDF)",
    type=["txt", "pdf"]
)

# =========================
# Run matching
# =========================
st.markdown("### 2️⃣ Lancer le matching")

if cv_file and job_file and st.button("Lancer le matching"):
    with st.spinner("Analyse en cours..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            cv_path = Path(tmpdir) / cv_file.name
            job_path = Path(tmpdir) / job_file.name

            cv_path.write_bytes(cv_file.read())
            job_path.write_bytes(job_file.read())

            st.info("Appel du pipeline IA")

            result = run_matching(
                cv_path=str(cv_path),
                job_path=str(job_path),
                n_runs=5
            )

    st.success("✅ Analyse terminée")

    # =========================
    # Display results
    # =========================
    st.markdown("### 📊 Résultats du matching")

    scores = result["scores_mean"]
    stds = result["scores_std"]

    global_score = scores.get("total", 0.0)
    global_std = stds.get("total", 0.0)

    st.metric(
        "Matching global",
        f"{global_score * 100:.1f} %",
        f"± {global_std * 100:.1f} %"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Hard skills",
            f"{scores.get('hard_skills', 0.0):.3f}"
        )

    with col2:
        st.metric(
            "Soft skills",
            f"{scores.get('soft_skills', 0.0):.3f}"
        )

    st.caption(
        f"Score estimé à partir de {result['n_runs']} exécutions indépendantes. "
        "De légères variations sont normales."
    )

    # =========================
    # Explanation
    # =========================
    st.markdown("### 🧠 Explication IA")
    st.write(result["explanation"])
