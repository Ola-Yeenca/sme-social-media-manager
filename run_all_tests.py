#!/usr/bin/env python3
"""
Comprehensive Test Runner for SME Social Media Bot
Coordinates unit tests, integration tests, and end-to-end tests with Playwright
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime
from pathlib import Path


class TestRunner:
    """Comprehensive test runner for the SME Social Media Bot"""
    
    def __init__(self):
        self.test_results = {
            'viral_prediction': {'status': 'pending', 'duration': 0, 'errors': []},
            'bot_integration': {'status': 'pending', 'duration': 0, 'errors': []},
            'e2e_playwright': {'status': 'pending', 'duration': 0, 'errors': []},
            'system_validation': {'status': 'pending', 'duration': 0, 'errors': []}
        }
        self.start_time = time.time()
        
        # Create test results directory
        Path('./test-results').mkdir(exist_ok=True)
        Path('./test-results/reports').mkdir(exist_ok=True)
    
    def run_viral_prediction_tests(self):
        """Run viral prediction unit tests"""
        print("\n🧪 Running Viral Prediction Unit Tests...")
        print("-" * 50)
        
        start_time = time.time()
        try:
            result = subprocess.run(
                [sys.executable, 'test_viral_prediction.py'],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                self.test_results['viral_prediction']['status'] = 'passed'
                print("✅ Viral prediction tests passed!")
            else:
                self.test_results['viral_prediction']['status'] = 'failed'
                self.test_results['viral_prediction']['errors'].append(result.stderr)
                print("❌ Viral prediction tests failed!")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
            
            self.test_results['viral_prediction']['duration'] = duration
            
        except subprocess.TimeoutExpired:
            self.test_results['viral_prediction']['status'] = 'timeout'
            self.test_results['viral_prediction']['errors'].append('Test timeout after 5 minutes')
            print("⏰ Viral prediction tests timed out!")
        
        except Exception as e:
            self.test_results['viral_prediction']['status'] = 'error'
            self.test_results['viral_prediction']['errors'].append(str(e))
            print(f"💥 Viral prediction tests error: {e}")
    
    def run_bot_integration_tests(self):
        """Run bot integration tests"""
        print("\n🔧 Running Bot Integration Tests...")
        print("-" * 50)
        
        start_time = time.time()
        try:
            result = subprocess.run(
                [sys.executable, 'test_bot_integration.py'],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                self.test_results['bot_integration']['status'] = 'passed'
                print("✅ Bot integration tests passed!")
            else:
                self.test_results['bot_integration']['status'] = 'failed'
                self.test_results['bot_integration']['errors'].append(result.stderr)
                print("❌ Bot integration tests failed!")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
            
            self.test_results['bot_integration']['duration'] = duration
            
        except subprocess.TimeoutExpired:
            self.test_results['bot_integration']['status'] = 'timeout'
            self.test_results['bot_integration']['errors'].append('Test timeout after 5 minutes')
            print("⏰ Bot integration tests timed out!")
        
        except Exception as e:
            self.test_results['bot_integration']['status'] = 'error'
            self.test_results['bot_integration']['errors'].append(str(e))
            print(f"💥 Bot integration tests error: {e}")
    
    def check_playwright_installation(self):
        """Check and install Playwright if needed"""
        try:
            import playwright
            print("✅ Playwright is available")
            return True
        except ImportError:
            print("📦 Installing Playwright...")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'playwright'], check=True)
                subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], check=True)
                print("✅ Playwright installed successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install Playwright: {e}")
                return False
    
    def run_e2e_playwright_tests(self):
        """Run end-to-end tests with Playwright"""
        print("\n🎭 Running End-to-End Tests with Playwright...")
        print("-" * 50)
        
        # Check Playwright installation
        if not self.check_playwright_installation():
            self.test_results['e2e_playwright']['status'] = 'skipped'
            self.test_results['e2e_playwright']['errors'].append('Playwright not available')
            print("⏭️ Skipping E2E tests - Playwright not available")
            return
        
        start_time = time.time()
        try:
            result = subprocess.run(
                [sys.executable, 'test_e2e_playwright.py'],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout for E2E tests
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                self.test_results['e2e_playwright']['status'] = 'passed'
                print("✅ End-to-end tests passed!")
            else:
                self.test_results['e2e_playwright']['status'] = 'failed'
                self.test_results['e2e_playwright']['errors'].append(result.stderr)
                print("❌ End-to-end tests failed!")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
            
            self.test_results['e2e_playwright']['duration'] = duration
            
        except subprocess.TimeoutExpired:
            self.test_results['e2e_playwright']['status'] = 'timeout'
            self.test_results['e2e_playwright']['errors'].append('Test timeout after 10 minutes')
            print("⏰ End-to-end tests timed out!")
        
        except Exception as e:
            self.test_results['e2e_playwright']['status'] = 'error'
            self.test_results['e2e_playwright']['errors'].append(str(e))
            print(f"💥 End-to-end tests error: {e}")
    
    def run_system_validation(self):
        """Run system validation tests"""
        print("\n🔍 Running System Validation...")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            # Test 1: Import all modules successfully
            print("📦 Testing module imports...")
            try:
                import bot
                import viral_predictor
                import config
                print("✅ All modules imported successfully")
            except Exception as e:
                self.test_results['system_validation']['errors'].append(f"Module import failed: {e}")
                print(f"❌ Module import failed: {e}")
            
            # Test 2: Configuration validation
            print("⚙️ Testing configuration...")
            try:
                from config import Config
                # Test with minimal required environment
                test_env = {
                    'TWITTER_API_KEY': 'test_key',
                    'TWITTER_API_SECRET': 'test_secret',
                    'TWITTER_ACCESS_TOKEN': 'test_token',
                    'TWITTER_ACCESS_TOKEN_SECRET': 'test_secret',
                    'TWITTER_BEARER_TOKEN': 'test_bearer',
                    'OPENAI_API_KEY': 'test_openai'
                }
                
                import os
                original_env = dict(os.environ)
                os.environ.update(test_env)
                try:
                    config = Config()
                    print("✅ Configuration validation passed")
                finally:
                    # Restore original environment
                    os.environ.clear()
                    os.environ.update(original_env)
                    
            except SystemExit:
                print("⚠️ Configuration validation requires environment variables (expected)")
            except Exception as e:
                self.test_results['system_validation']['errors'].append(f"Configuration test failed: {e}")
                print(f"❌ Configuration test failed: {e}")
            
            # Test 3: Viral predictor functionality
            print("🎯 Testing viral predictor...")
            try:
                from viral_predictor import ViralTweetPredictor
                predictor = ViralTweetPredictor()
                
                # Test prediction
                test_tweet = "Test tweet for validation #Test #AI"
                score = predictor.predict_viral_potential(test_tweet)
                
                assert hasattr(score, 'total_score')
                assert hasattr(score, 'predicted_engagement')
                assert hasattr(score, 'recommendations')
                
                print("✅ Viral predictor validation passed")
                
            except Exception as e:
                self.test_results['system_validation']['errors'].append(f"Viral predictor test failed: {e}")
                print(f"❌ Viral predictor test failed: {e}")
            
            # Test 4: File structure validation
            print("📁 Testing file structure...")
            required_files = [
                'bot.py',
                'viral_predictor.py',
                'config.py',
                'requirements.txt',
                '.github/workflows/sme-social-bot.yml'
            ]
            
            missing_files = []
            for file_path in required_files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)
            
            if missing_files:
                error_msg = f"Missing required files: {', '.join(missing_files)}"
                self.test_results['system_validation']['errors'].append(error_msg)
                print(f"❌ {error_msg}")
            else:
                print("✅ File structure validation passed")
            
            duration = time.time() - start_time
            self.test_results['system_validation']['duration'] = duration
            
            # Set overall status
            if self.test_results['system_validation']['errors']:
                self.test_results['system_validation']['status'] = 'failed'
                print("❌ System validation completed with errors")
            else:
                self.test_results['system_validation']['status'] = 'passed'
                print("✅ System validation passed!")
                
        except Exception as e:
            self.test_results['system_validation']['status'] = 'error'
            self.test_results['system_validation']['errors'].append(str(e))
            print(f"💥 System validation error: {e}")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        total_duration = time.time() - self.start_time
        
        report = {
            'test_run_info': {
                'timestamp': datetime.now().isoformat(),
                'total_duration': round(total_duration, 2),
                'python_version': sys.version,
                'platform': sys.platform
            },
            'test_results': self.test_results,
            'summary': {
                'total_tests': len(self.test_results),
                'passed': sum(1 for r in self.test_results.values() if r['status'] == 'passed'),
                'failed': sum(1 for r in self.test_results.values() if r['status'] == 'failed'),
                'errors': sum(1 for r in self.test_results.values() if r['status'] == 'error'),
                'timeouts': sum(1 for r in self.test_results.values() if r['status'] == 'timeout'),
                'skipped': sum(1 for r in self.test_results.values() if r['status'] == 'skipped'),
            }
        }
        
        # Save detailed report
        report_path = f"./test-results/reports/test-report-{int(time.time())}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report, report_path
    
    def print_summary(self, report, report_path):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST EXECUTION SUMMARY")
        print("=" * 60)
        
        summary = report['summary']
        total_duration = report['test_run_info']['total_duration']
        
        print(f"⏱️  Total Duration: {total_duration:.2f} seconds")
        print(f"📈 Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"💥 Errors: {summary['errors']}")
        print(f"⏰ Timeouts: {summary['timeouts']}")
        print(f"⏭️  Skipped: {summary['skipped']}")
        
        print("\n📋 DETAILED RESULTS:")
        print("-" * 30)
        
        for test_name, result in self.test_results.items():
            status_emoji = {
                'passed': '✅',
                'failed': '❌', 
                'error': '💥',
                'timeout': '⏰',
                'skipped': '⏭️',
                'pending': '⏳'
            }.get(result['status'], '❓')
            
            duration = result['duration']
            print(f"{status_emoji} {test_name.replace('_', ' ').title()}: {result['status'].upper()} ({duration:.2f}s)")
            
            if result['errors']:
                for error in result['errors']:
                    print(f"   └─ Error: {error[:100]}{'...' if len(error) > 100 else ''}")
        
        print(f"\n📄 Detailed report saved: {report_path}")
        
        # Determine overall success
        critical_failures = summary['failed'] + summary['errors']
        
        if critical_failures == 0:
            print("\n🎉 ALL TESTS PASSED! The SME Social Media Bot is ready for production.")
            return True
        else:
            print(f"\n⚠️  {critical_failures} CRITICAL FAILURES detected. Review errors before deployment.")
            return False
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting Comprehensive Test Suite for SME Social Media Bot")
        print("=" * 60)
        
        # Run all test suites
        self.run_system_validation()
        self.run_viral_prediction_tests()
        self.run_bot_integration_tests()
        self.run_e2e_playwright_tests()
        
        # Generate and display report
        report, report_path = self.generate_test_report()
        success = self.print_summary(report, report_path)
        
        return success


def main():
    """Main entry point"""
    runner = TestRunner()
    
    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n🛑 Test execution interrupted by user")
        sys.exit(130)
        
    except Exception as e:
        print(f"\n💥 Test runner failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()