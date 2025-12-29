import streamlit as st
import os
import shutil
import pandas as pd

from halstead import halstead_metrics
from complexity import cyclomatic_complexity
from maintainability import maintainability_index
from oo_metrics import compute_oo_metrics

# ---------------- CONFIG ----------------
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(
    page_title="Software Metrics Analyzer",
    layout="wide"
)

st.title("📊 Automated Software Metrics Analyzer")
st.write(
    "Upload Python source files to compute **Halstead Metrics**, "
    "**Cyclomatic Complexity**, and **Maintainability Index**."
)

# ---------------- HELPER FUNCTIONS ----------------
def count_loc(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return len([line for line in f if line.strip()])


def interpret_metrics(row):
    interpretation = []

    # Cyclomatic Complexity
    if row["Cyclomatic Complexity"] <= 10:
        interpretation.append("🟢 Low control-flow complexity")
    elif row["Cyclomatic Complexity"] <= 20:
        interpretation.append("🟡 Moderate control-flow complexity")
    else:
        interpretation.append("🔴 High control-flow complexity")

    # Maintainability Index
    if row["Maintainability Index"] >= 65:
        interpretation.append("🟢 Highly maintainable code")
    elif row["Maintainability Index"] >= 40:
        interpretation.append("🟡 Moderately maintainable code")
    else:
        interpretation.append("🔴 Poor maintainability (needs refactoring)")

    # Halstead Effort
    if row["Halstead Effort"] < 50_000:
        interpretation.append("🟢 Easy to understand and modify")
    elif row["Halstead Effort"] < 500_000:
        interpretation.append("🟡 Moderate effort required")
    else:
        interpretation.append("🔴 Very high development & maintenance effort")

    return " | ".join(interpretation)


# ---------------- FILE UPLOAD ----------------
uploaded_files = st.file_uploader(
    "📂 Upload Python source files",
    type=["py"],
    accept_multiple_files=True
)

if uploaded_files:
    # Clear previous uploads
    shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save uploaded files
    for uploaded_file in uploaded_files:
        with open(os.path.join(UPLOAD_DIR, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

    st.success("✅ Files uploaded successfully!")

    results = []

    # Analyze files
    for file in os.listdir(UPLOAD_DIR):
        if not file.endswith(".py"):
            continue

        path = os.path.join(UPLOAD_DIR, file)

        halstead = halstead_metrics(path)
        complexity = cyclomatic_complexity(path)
        loc = count_loc(path)

        mi = maintainability_index(
            halstead["Halstead Volume"],
            complexity,
            loc
        )

        classes, noc = compute_oo_metrics(path)

        if not classes:
            results.append({
                "File": file,
                "Class": "Script / No Class",
                "Cyclomatic Complexity": complexity,
                "Maintainability Index": mi,
                "Halstead Volume": halstead["Halstead Volume"],
                "Halstead Difficulty": halstead["Halstead Difficulty"],
                "Halstead Effort": halstead["Halstead Effort"],
                "Estimated Bugs": halstead["Estimated Bugs"]
            })
        else:
            for cls in classes:
                results.append({
                    "File": file,
                    "Class": cls,
                    "Cyclomatic Complexity": complexity,
                    "Maintainability Index": mi,
                    "Halstead Volume": halstead["Halstead Volume"],
                    "Halstead Difficulty": halstead["Halstead Difficulty"],
                    "Halstead Effort": halstead["Halstead Effort"],
                    "Estimated Bugs": halstead["Estimated Bugs"]
                })

    df = pd.DataFrame(results)

    # ---------------- DISPLAY RESULTS ----------------
    st.subheader("📋 Metrics Summary")
    st.dataframe(df, use_container_width=True)

    st.subheader("🧠 Interpretation")
    for _, row in df.iterrows():
        st.markdown(f"### 📄 `{row['File']}`")
        st.write(interpret_metrics(row))

    # Download option
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Metrics as CSV",
        csv,
        "software_metrics_report.csv",
        "text/csv"
    )
