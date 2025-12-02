#!/usr/bin/env python3
"""
Setup script for QA Automation Assignment
"""
import os
import subprocess
import sys

def setup_environment():
    """Set up the test environment"""
    print("=" * 60)
    print("Setting up QA Automation Test Environment")
    print("=" * 60)
    
    # Create necessary directories
    directories = ["reports", "screenshots", "logs", "config", "pages", "tests", "utils"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    try:
        with open("requirements.txt", "w") as f:
            f.write("""selenium==4.15.0
pytest==7.4.3
pytest-html==4.0.2
webdriver-manager==4.0.1
requests==2.31.0""")
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
    except Exception as e:
        print(f"⚠️ Could not install from requirements.txt: {e}")
        print("Installing individually...")
        packages = ["selenium", "pytest", "pytest-html", "webdriver-manager", "requests"]
        for package in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("\n✅ Setup completed successfully!")
    print("\nTo run tests:")
    print("  python3 run_tests.py              # Run all tests")
    print("  python3 run_tests.py smoke        # Run smoke tests only")
    print("  python3 run_tests.py regression   # Run regression tests only")
    print("\nThe tests will document known issues found in the website.")
    print("=" * 60)

if __name__ == "__main__":
    setup_environment()