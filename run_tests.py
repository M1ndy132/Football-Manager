"""
Test runner script for Football Manager application.
Run all tests with proper configuration and reporting.
"""

import pytest
import sys
import os
from pathlib import Path

def run_tests():
    """Run all tests with comprehensive reporting."""
    
    # Add the app directory to Python path
    app_root = Path(__file__).parent.parent
    sys.path.insert(0, str(app_root))
    
    # Test configuration
    pytest_args = [
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker validation
        "--disable-warnings",  # Disable warnings for cleaner output
        "-x",  # Stop on first failure
        "--maxfail=5",  # Stop after 5 failures
        "app/tests/",  # Test directory
    ]
    
    # Add coverage if available
    try:
        import coverage
        pytest_args.extend([
            "--cov=app",  # Coverage for app module
            "--cov-report=term-missing",  # Show missing lines
            "--cov-report=html:htmlcov",  # HTML coverage report
            "--cov-fail-under=70",  # Require 70% coverage
        ])
        print("📊 Running tests with coverage analysis...")
    except ImportError:
        print("⚠️  Coverage not available. Install with: pip install pytest-cov")
        print("🧪 Running tests without coverage...")
    
    print("🚀 Starting Football Manager test suite...")
    print(f"📁 Test directory: {Path('app/tests/').absolute()}")
    print("=" * 60)
    
    # Run tests
    exit_code = pytest.main(pytest_args)
    
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✅ All tests passed successfully!")
        print("🎉 Your Football Manager application is ready for demo!")
    else:
        print(f"❌ Tests failed with exit code: {exit_code}")
        print("🔧 Please fix the failing tests before your demo.")
    
    return exit_code

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
