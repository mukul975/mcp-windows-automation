#!/usr/bin/env python3
"""
Quick Test Runner for MCP Windows Security Tools
"""

import subprocess
import sys
import time
from datetime import datetime

def run_test_suite(test_command, test_name):
    """Run a test suite and return results"""
    print(f"🧪 Running {test_name}...")
    start_time = time.time()
    
    try:
        result = subprocess.run(
            test_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {test_name} PASSED ({duration:.1f}s)")
            return True, duration, result.stdout
        else:
            print(f"❌ {test_name} FAILED ({duration:.1f}s)")
            print(f"Error: {result.stderr}")
            return False, duration, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} TIMEOUT (>300s)")
        return False, 300, "Test timed out"
    except Exception as e:
        print(f"💥 {test_name} ERROR: {str(e)}")
        return False, 0, str(e)

def main():
    """Main test runner"""
    print("🚀 Starting MCP Security Quick Tests")
    print("=" * 50)
    
    start_time = time.time()
    
    # Test suites to run
    test_suites = [
        ("python -m pytest tests/security/test_authentication.py -v --tb=short", "Authentication Tests"),
        ("python -m pytest tests/security/test_security_vulnerabilities.py::TestSecurityVulnerabilities::test_sql_injection_prevention -v", "SQL Injection Tests"),
        ("python -m pytest tests/security/test_security_vulnerabilities.py::TestSecurityVulnerabilities::test_xss_protection -v", "XSS Protection Tests"),
        ("python -m pytest tests/security/test_security_vulnerabilities.py::TestSecurityVulnerabilities::test_command_injection_prevention -v", "Command Injection Tests"),
        ("python -m pytest tests/performance/test_performance.py::TestPerformance::test_memory_usage_monitoring -v", "Memory Performance Tests"),
        ("python -m pytest tests/performance/test_performance.py::TestPerformance::test_concurrent_request_handling -v", "Concurrency Tests"),
    ]
    
    results = []
    total_duration = 0
    
    for test_command, test_name in test_suites:
        success, duration, output = run_test_suite(test_command, test_name)
        results.append((test_name, success, duration, output))
        total_duration += duration
    
    end_time = time.time()
    
    # Generate summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success, _, _ in results if success)
    failed = len(results) - passed
    
    print(f"Total Tests: {len(results)}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    print(f"Total Duration: {total_duration:.1f}s")
    
    print("\n📋 DETAILED RESULTS:")
    for test_name, success, duration, _ in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name} ({duration:.1f}s)")
    
    print(f"\n🕐 Test run completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return success if all tests passed
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
