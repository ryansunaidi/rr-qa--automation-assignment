"""
Report generation utilities
"""
import json
import os
from datetime import datetime
from config.config import Config

class TestReport:
    """Test report generator"""
    
    def __init__(self, test_suite_name="QA Automation Test Suite"):
        self.suite_name = test_suite_name
        self.start_time = datetime.now()
        self.tests = []
        self.failed_tests = []
        self.passed_tests = []
        self.skipped_tests = []
        
    def add_test_result(self, test_name, status, error_message=None, screenshot=None):
        """Add test result to report"""
        test_result = {
            "name": test_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "error": error_message,
            "screenshot": screenshot
        }
        
        self.tests.append(test_result)
        
        if status == "PASSED":
            self.passed_tests.append(test_result)
        elif status == "FAILED":
            self.failed_tests.append(test_result)
        elif status == "SKIPPED":
            self.skipped_tests.append(test_result)
    
    def generate_summary(self):
        """Generate test summary"""
        total = len(self.tests)
        passed = len(self.passed_tests)
        failed = len(self.failed_tests)
        skipped = len(self.skipped_tests)
        
        summary = {
            "test_suite": self.suite_name,
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration": str(datetime.now() - self.start_time),
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "failed_tests": [test["name"] for test in self.failed_tests]
        }
        
        return summary
    
    def generate_json_report(self):
        """Generate JSON report"""
        report = {
            "summary": self.generate_summary(),
            "test_details": self.tests
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{Config.REPORT_DIR}/test_report_{timestamp}.json"
        
        os.makedirs(Config.REPORT_DIR, exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        
        return filename
    
    def print_console_report(self):
        """Print report to console"""
        summary = self.generate_summary()
        
        print("\n" + "=" * 60)
        print("TEST EXECUTION SUMMARY")
        print("=" * 60)
        print(f"Test Suite: {summary['test_suite']}")
        print(f"Start Time: {summary['start_time']}")
        print(f"End Time: {summary['end_time']}")
        print(f"Duration: {summary['duration']}")
        print("-" * 60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Skipped: {summary['skipped']}")
        print(f"Pass Rate: {summary['pass_rate']:.2f}%")
        
        if summary['failed_tests']:
            print("\n" + "-" * 60)
            print("FAILED TESTS:")
            for test in summary['failed_tests']:
                print(f"  - {test}")
        
        print("=" * 60)