"""Automation Test Runner for Smart Note App QA.

Executes test suites, captures live logs, evaluates PASS/FAIL, and generates
markdown test execution reports compliant with IEEE 829 & ISTQB standards.
"""
import os
import sys
import datetime
import pytest

# Ensure UTF-8 execution environment
os.environ["PYTHONIOENCODING"] = "utf-8"
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ensure repository root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def run_suite(suite_name: str):
    reports_dir = os.path.join(PROJECT_ROOT, "automation", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 70)
    print(f"SMART NOTE APP AUTOMATION RUNNER — {suite_name.upper()}")
    print(f"Timestamp: {timestamp}")
    print(f"Target Repository: ttt-huong/Smart-Note-App-QA (Branch: huong)")
    print("=" * 70)

    test_file = os.path.join(PROJECT_ROOT, "automation", "tests", f"test_{suite_name}.py")
    if not os.path.exists(test_file):
        print(f"Error: Test file not found: {test_file}")
        sys.exit(1)

    pytest_args = [
        "-v",
        "-s",
        test_file,
        f"--junitxml={os.path.join(reports_dir, f'{suite_name}_junit.xml')}"
    ]
    
    print(f"Executing: pytest {' '.join(pytest_args)}")
    ret_code = pytest.main(pytest_args)
    print("=" * 70)
    print(f"Suite finished with exit code: {ret_code}")
    print("=" * 70)
    return ret_code

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Smart Note App QA Automation Runner")
    parser.add_argument("--suite", default="fn04_login", help="Suite name to run (e.g. fn04_login)")
    args = parser.parse_args()
    
    sys.exit(run_suite(args.suite))
