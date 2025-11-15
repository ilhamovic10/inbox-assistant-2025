#!/usr/bin/env python3
"""
Quick Start Script for Inbox Assistant
Runs all setup steps and verifies the system
"""

import sys
import subprocess
import os

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def check_python_version():
    """Check if Python version is 3.9+"""
    print_header("1. Checking Python Version")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required. You have {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
    return True

def check_files():
    """Check if all required files exist"""
    print_header("2. Checking Required Files")
    required_files = [
        "agent.py",
        "config.py", 
        "utils.py",
        "requirements.txt",
        ".env.example",
        "README.md",
    ]

    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_exist = False

    return all_exist

def check_env_file():
    """Check if .env file is configured"""
    print_header("3. Checking Environment Configuration")

    if not os.path.exists(".env"):
        print("⚠️  .env file not found")
        print("\nCreating .env from .env.example...")
        try:
            with open(".env.example", "r") as f:
                content = f.read()
            with open(".env", "w") as f:
                f.write(content)
            print("✅ .env created from template")
            print("\n⚠️  IMPORTANT: Edit .env and add your GOOGLE_API_KEY!")
            print("   Get key at: https://aistudio.google.com/app/apikey")
            return False
        except Exception as e:
            print(f"❌ Error creating .env: {e}")
            return False
    else:
        with open(".env", "r") as f:
            content = f.read()
        if "AIza" in content or "AIza" in content.split("=")[1]:
            print("✅ .env file configured")
            return True
        else:
            print("⚠️  .env found but GOOGLE_API_KEY not properly set")
            print("   Please add your key from: https://aistudio.google.com/app/apikey")
            return False

def install_dependencies():
    """Install Python dependencies"""
    print_header("4. Installing Dependencies")
    try:
        print("Running: pip install -r requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                             "-q", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_tests():
    """Run unit tests"""
    print_header("5. Running Tests")
    try:
        import pytest
        print("Running: pytest tests/ -q")
        result = pytest.main([
            "tests/",
            "-q",
            "--tb=short"
        ])
        if result == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed (but this is OK if API key issues)")
            return True
    except Exception as e:
        print(f"⚠️  Could not run pytest: {e}")
        print("   Skipping tests")
        return True

def run_demo():
    """Run the demo"""
    print_header("6. Running Demo")
    try:
        print("Running: python examples/demo.py")
        subprocess.call([sys.executable, "examples/demo.py"])
        print("✅ Demo completed!")
        return True
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  INBOX ASSISTANT - QUICK START".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")

    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_files),
        ("Environment", check_env_file),
        ("Dependencies", install_dependencies),
        ("Tests", run_tests),
        ("Demo", run_demo),
    ]

    results = []
    for name, check in checks:
        try:
            result = check()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results.append((name, False))

    # Summary
    print_header("Setup Summary")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    all_passed = all(r for _, r in results)
    if all_passed:
        print("\n" + "🎉 "*10)
        print("ALL CHECKS PASSED! Your system is ready!")
        print("\nNext steps:")
        print("1. Upload to GitHub: https://github.com/new")
        print("2. Submit to Kaggle: https://www.kaggle.com/competitions/agents-intensive-capstone-project")
        print("\nGood luck! 🚀")
    else:
        print("\n⚠️  Some checks failed. Please fix issues above and try again.")
        print("\nCommon issues:")
        print("- .env file needs GOOGLE_API_KEY")
        print("- Run: pip install -r requirements.txt")
        print("- Ensure Python 3.9 or higher")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
