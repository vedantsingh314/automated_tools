import streamlit as st
import os
import shutil
import pandas as pd

from halstead import halstead_metrics
from complexity import cyclomatic_complexity
from maintainability import maintainability_index
from oo_metrics import compute_oo_metrics


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Software Quality Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PATH SETUP ----------------
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------- HELPER FUNCTIONS ----------------
def count_loc(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return len([line for line in f if line.strip()])


def interpret_metrics(row):
    insights = []

    if row["Cyclomatic Complexity"] <= 10:
        insights.append("🟢 Low complexity")
    elif row["Cyclomatic Complexity"] <= 20:
        insights.append("🟡 Moderate complexity")
    else:
        insights.append("🔴 High complexity")

    if row["Maintainability Index"] >= 65:
        insights.append("🟢 High maintainability")
    elif row["Maintainability Index"] >= 40:
        insights.append("🟡 Medium maintainability")
    else:
        insights.append("🔴 Low maintainability")

    if row["Halstead Effort"] < 50_000:
        insights.append("🟢 Low Halstead effort")
    elif row["Halstead Effort"] < 500_000:
        insights.append("🟡 Medium Halstead effort")
    else:
        insights.append("🔴 High Halstead effort")

    return " | ".join(insights)


# ---------------- SIDEBAR ----------------
st.sidebar.title("📂 Upload Source Code")
uploaded_files = st.sidebar.file_uploader(
    "Upload Python (.py) files",
    type=["py"],
    accept_multiple_files=True
)

analyze_btn = st.sidebar.button("Analyze", use_container_width=True)


# ---------------- MAIN HEADER ----------------
st.title("📊 Software Quality Analysis Dashboard")
st.caption("Static analysis of Python source code")

st.info(
    "This tool analyzes uploaded Python source code using standard "
    "software engineering metrics. Files are processed temporarily and not stored."
)


# ---------------- ANALYSIS ----------------
if analyze_btn and uploaded_files:
    shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for file in uploaded_files:
        with open(os.path.join(UPLOAD_DIR, file.name), "wb") as f:
            f.write(file.getbuffer())

    results = []

    for file in os.listdir(UPLOAD_DIR):
        if not file.endswith(".py"):
            continue

        path = os.path.join(UPLOAD_DIR, file)

        # ---- Metrics computation ----
        halstead = halstead_metrics(path)
        complexity = cyclomatic_complexity(path)
        loc = count_loc(path)

        mi = maintainability_index(
            halstead["Volume"],   # ✅ FIXED
            complexity,
            loc
        )

        results.append({
            "File": file,

            # 🔹 FULL HALSTEAD METRICS
            "n1 (Distinct Operators)": halstead["n1"],
            "n2 (Distinct Operands)": halstead["n2"],
            "N1 (Total Operators)": halstead["N1"],
            "N2 (Total Operands)": halstead["N2"],
            "Vocabulary": halstead["Vocabulary"],
            "Program Length": halstead["ProgramLength"],
            "Halstead Volume": halstead["Volume"],          # ✅ FIXED
            "Halstead Difficulty": halstead["Difficulty"], # ✅ FIXED
            "Halstead Effort": halstead["Effort"],         # ✅ FIXED
            "Estimated Bugs": halstead["Estimated Bugs"],

            # 🔹 OTHER METRICS
            "Cyclomatic Complexity": complexity,
            "Maintainability Index": mi
        })

    df = pd.DataFrame(results)

    # ---------------- HALSTEAD METRICS ----------------
    with st.expander("📐 Halstead Complexity Metrics", expanded=True):
        st.dataframe(
            df[
                [
                    "File",
                    "n1 (Distinct Operators)",
                    "n2 (Distinct Operands)",
                    "N1 (Total Operators)",
                    "N2 (Total Operands)",
                    "Vocabulary",
                    "Program Length",
                    "Halstead Volume",
                    "Halstead Difficulty",
                    "Halstead Effort",
                    "Estimated Bugs"
                ]
            ],
            use_container_width=True
        )

    # ---------------- OTHER METRICS ----------------
    with st.expander("📊 Control Flow & Maintainability Metrics", expanded=True):
        st.dataframe(
            df[
                [
                    "File",
                    "Cyclomatic Complexity",
                    "Maintainability Index"
                ]
            ],
            use_container_width=True
        )

    # ---------------- INSIGHTS ----------------
    with st.expander("🧠 Code Quality Insights", expanded=True):
        for _, row in df.iterrows():
            st.markdown(f"### 📄 `{row['File']}`")
            st.write(interpret_metrics(row))

    # ---------------- DOWNLOAD ----------------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Full Metrics Report (CSV)",
        csv,
        "software_metrics_report.csv",
        "text/csv"
    )

elif analyze_btn:
    st.warning("Please upload at least one Python file to analyze.")
