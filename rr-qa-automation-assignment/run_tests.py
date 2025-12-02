#!/usr/bin/env python3
"""
Test Runner Script
"""
import subprocess
import sys
import os
from datetime import datetime

def run_tests():
    """Execute test suite with different configurations"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/test_report_{timestamp}.html"
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    print("=" * 60)
    print("Running QA Automation Test Suite")
    print("=" * 60)
    
    # Run tests with HTML report
    cmd = [
        "pytest",
        "tests/",
        "-v",
        f"--html={report_file}",
        "--self-contained-html",
        "--capture=tee-sys"
    ]
    
    # Add markers if specified
    if len(sys.argv) > 1:
        if sys.argv[1] == "smoke":
            cmd.extend(["-m", "smoke"])
            print("Running SMOKE tests only")
        elif sys.argv[1] == "regression":
            cmd.extend(["-m", "regression"])
            print("Running REGRESSION tests only")
        elif sys.argv[1] == "negative":
            cmd.extend(["-m", "negative"])
            print("Running NEGATIVE tests only")
    
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    # Execute tests
    result = subprocess.run(cmd)
    
    print("-" * 60)
    if os.path.exists(report_file):
        print(f"✅ HTML Report: {report_file}")
    print("=" * 60)
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)