
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Make the project root available for imports.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Framework.ai.flaky_test_detector import FlakyTestDetector

INPUT_FILE = ROOT / "reports" / "flaky_history.json"
OUTPUT_FILE = ROOT / "reports" / "flaky_analysis.json"



def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Results file not found: {INPUT_FILE}"
        )

    results = json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )

    report = FlakyTestDetector.analyze_results(results)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_FILE.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    for test_name, details in report.items():
        status = (
            "POTENTIALLY FLAKY"
            if details["potentially_flaky"]
            else "NO MIXED OUTCOMES"
        )

        print(f"{test_name}: {status} — {details}")

    print(f"\nReport written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
