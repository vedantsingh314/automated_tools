import os
import csv

from halstead import halstead_metrics
from oo_metrics import compute_oo_metrics
from complexity import cyclomatic_complexity
from maintainability import maintainability_index


# ---------------- PATH SETUP (ROBUST) ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "input_code")
OUTPUT_FILE = os.path.join(BASE_DIR, "output.csv")


# ---------------- HELPER FUNCTION ----------------
def count_loc(file_path):
    """Count non-empty lines of code"""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return len([line for line in f if line.strip()])


# ---------------- MAIN ANALYSIS ----------------
def run_metrics():
    if not os.path.exists(INPUT_FOLDER):
        raise FileNotFoundError(f"Input folder not found: {INPUT_FOLDER}")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # CSV Header
        writer.writerow([
            "File",
            "Class",
            "WMC",
            "NOC",
            "Cyclomatic Complexity",
            "Maintainability Index",
            "Halstead Volume",
            "Halstead Difficulty",
            "Halstead Effort",
            "Estimated Bugs"
        ])

        # Process each Python file
        for file in os.listdir(INPUT_FOLDER):
            if not file.endswith(".py"):
                continue

            path = os.path.join(INPUT_FOLDER, file)

            # Compute metrics
            halstead = halstead_metrics(path)
            complexity = cyclomatic_complexity(path)
            loc = count_loc(path)

            mi = maintainability_index(
                halstead["Halstead Volume"],
                complexity,
                loc
            )

            classes, noc = compute_oo_metrics(path)

            # ---------------- SCRIPT-BASED FILE ----------------
            if not classes:
                writer.writerow([
                    file,
                    "Script / No Class",
                    0,
                    0,
                    complexity,
                    mi,
                    halstead["Halstead Volume"],
                    halstead["Halstead Difficulty"],
                    halstead["Halstead Effort"],
                    halstead["Estimated Bugs"]
                ])

            # ---------------- CLASS-BASED FILE ----------------
            else:
                for cls, wmc in classes.items():
                    writer.writerow([
                        file,
                        cls,
                        wmc,
                        noc.get(cls, 0),
                        complexity,
                        mi,
                        halstead["Halstead Volume"],
                        halstead["Halstead Difficulty"],
                        halstead["Halstead Effort"],
                        halstead["Estimated Bugs"]
                    ])

    print("✅ Metrics analysis complete. Output saved to output.csv")


# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    run_metrics()
