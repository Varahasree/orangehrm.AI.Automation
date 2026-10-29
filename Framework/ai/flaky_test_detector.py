
from collections import defaultdict


class FlakyTestDetector:
    """Identify tests with mixed pass/fail outcomes across runs."""

    @staticmethod
    def analyze_results(results):
        """
        Expected input:
        [
            {"test": "test_login", "outcome": "passed"},
            {"test": "test_login", "outcome": "failed"},
        ]
        """
        outcomes = defaultdict(list)

        for result in results:
            test_name = result.get("test")
            outcome = result.get("outcome")

            if not test_name or outcome not in {
                "passed", "failed", "skipped"
            }:
                continue

            outcomes[test_name].append(outcome)

        report = {}

        for test_name, test_outcomes in outcomes.items():
            passed = test_outcomes.count("passed")
            failed = test_outcomes.count("failed")
            skipped = test_outcomes.count("skipped")

            # A mixed pass/fail history is a potential flake.
            is_flaky = passed > 0 and failed > 0

            report[test_name] = {
                "runs": len(test_outcomes),
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "potentially_flaky": is_flaky,
            }

        return report
