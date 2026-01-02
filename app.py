

import streamlit as st
from pathlib import Path
import tempfile

from main import run_matching

# -------------------------
# Config page
# -------------------------
st.set_page_config(
    page_title="Smart Resume & Job Matcher",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Smart Resume & Job Matcher")
st.write("Matching intelligent entre un CV et une offre d’emploi")

st.divider()

# -------------------------
# Upload fichiers
# -------------------------
st.subheader("1️⃣ Charger les fichiers")

cv_file = st.file_uploader(
    "Uploader le CV (PDF)",
    type=["pdf"]
)

job_file = st.file_uploader(
    "Uploader l'offre d'emploi (TXT ou PDF)",
    type=["txt", "pdf"]
)

st.divider()

# -------------------------
# Bouton lancement
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
        with st.spinner("Analyse en cours..."):
            # Sauvegarde temporaire des fichiers
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_dir = Path(tmp_dir)

                cv_path = tmp_dir / cv_file.name
                job_path = tmp_dir / job_file.name

                cv_path.write_bytes(cv_file.getbuffer())
                job_path.write_bytes(job_file.getbuffer())

                # Appel du pipeline IA
                result = run_matching(
                    cv_path=str(cv_path),
                    job_path=str(job_path)
                )

        st.success("✅ Analyse terminée")

        # -------------------------
        # Résultats
        # -------------------------
        st.divider()
        st.subheader("📊 Résultats du matching")

        scores_mean = result["scores_mean"]
        scores_std = result["scores_std"]
        n_runs = result["n_runs"]

        col1, col2, col3 = st.columns(3)

        total_mean = float(scores_mean.get("total", 0))
        total_std = float(scores_std.get("total", 0))

        percentage = round(total_mean * 100, 1)
        percentage_std = round(total_std * 100, 1)


        col1.metric(
            "Matching global",
            f"{percentage} %",
            f"± {percentage_std} %"
        )

        col2.metric(
            "Hard skills",
            round(scores_mean.get("hard_skills", 0), 3)
        )

        col3.metric(
            "Soft skills",
            round(scores_mean.get("soft_skills", 0), 3)
        )


        st.progress(total_mean)

        # -------------------------
        # Explication IA
        # -------------------------
        st.info(
            f"Score estimé à partir de {n_runs} exécutions indépendantes. "
            "De légères variations sont normales."
        )

        st.divider()
        st.subheader("🧠 Explication IA")

        st.write(result["explanation"])

