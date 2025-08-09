# SME Social Media Bot - Comprehensive Testing Suite

This document describes the comprehensive testing strategy for the SME Social Media Bot, including unit tests, integration tests, and end-to-end tests using Playwright.

## 🎯 Testing Strategy Overview

Our testing approach follows the test pyramid pattern:

```
     /\
    /  \    E2E Tests (Playwright)
   /____\   - Complete user workflows
  /      \  - GitHub Actions integration
 /        \ - API mocking and validation
/__________\
Integration Tests
- Component interactions
- API integrations (mocked)
- Workflow coordination
- Error handling scenarios

Unit Tests
- Individual functions and classes
- Viral prediction algorithms
- Configuration validation
- Content generation logic
```

## 📋 Test Files Overview

### Core Test Files

1. **`test_viral_prediction.py`** - Unit tests for viral prediction system
   - Viral score calculation
   - Content analysis algorithms
   - Tweet optimization
   - Viral variations generation
   - Recommendation engine

2. **`test_bot_integration.py`** - Integration tests for bot components
   - Bot initialization and configuration
   - Content generation with AI providers
   - Twitter API integration (mocked)
   - Workflow coordination
   - Error handling and recovery

3. **`test_e2e_playwright.py`** - End-to-end tests using Playwright
   - Complete workflow simulation
   - GitHub Actions integration
   - API interactions with mocking
   - Browser automation for UI validation
   - Performance and reliability testing

4. **`playwright.config.py`** - Playwright configuration
   - Browser settings and options
   - Timeout configurations
   - Screenshot and video recording
   - Test data and mock responses

5. **`run_all_tests.py`** - Comprehensive test runner
   - Coordinates all test suites
   - Generates detailed reports
   - Provides summary and status
   - Handles test environment setup

### Configuration Files

- **`requirements_test.txt`** - Testing dependencies
- **`.github/workflows/test-suite.yml`** - CI/CD test automation
- **`TESTING.md`** - This documentation file

## 🚀 Quick Start

### Local Testing

1. **Install test dependencies:**
   ```bash
   pip install -r requirements_test.txt
   ```

2. **Run all tests:**
   ```bash
   python run_all_tests.py
   ```

3. **Run specific test suites:**
   ```bash
   # Viral prediction tests only
   python test_viral_prediction.py
   
   # Integration tests only
   python test_bot_integration.py
   
   # E2E tests only (requires Playwright)
   python test_e2e_playwright.py
   ```

### Using pytest (Alternative)

```bash
# Install Playwright browsers (one-time setup)
playwright install chromium

# Run with pytest
pytest test_viral_prediction.py -v
pytest test_bot_integration.py -v
pytest test_e2e_playwright.py -v --headed  # Run with visible browser
```

## 📊 Test Coverage Areas

### 1. Viral Prediction System Tests

**File:** `test_viral_prediction.py`

**Coverage:**
- ✅ Viral score calculation algorithm
- ✅ Content analysis (emotional triggers, power words, CTAs)
- ✅ Timing optimization (peak hours, weekdays vs weekends)
- ✅ Hashtag effectiveness scoring
- ✅ Engagement potential prediction
- ✅ Trend alignment analysis
- ✅ Tweet optimization workflow
- ✅ Viral variations generation
- ✅ Recommendation engine
- ✅ Confidence level calculation
- ✅ Edge cases and error handling

**Key Test Scenarios:**
```python
# High viral potential content
"🚀 BREAKING: AI revolutionizes small business analytics! 10x revenue growth proven. What's your take? #AI #Business"

# Low viral potential content  
"We updated our website today."

# Optimization testing
original → optimized → improved_score
```

### 2. Bot Integration Tests

**File:** `test_bot_integration.py`

**Coverage:**
- ✅ Bot initialization and configuration
- ✅ AI provider integration (OpenAI, Anthropic, Grok)
- ✅ Content generation workflow
- ✅ Twitter API integration (mocked)
- ✅ Viral prediction integration
- ✅ Mention checking and engagement
- ✅ Reply generation
- ✅ Error handling and recovery
- ✅ Rate limit handling
- ✅ Session statistics tracking
- ✅ Workflow coordination

**Mock API Responses:**
```python
# Twitter API responses
twitter_post_success = {
    'data': {'id': '123456789', 'text': 'Generated content...'}
}

# OpenAI responses
openai_response = {
    'choices': [{'message': {'content': 'Generated tweet content'}}]
}
```

### 3. End-to-End Tests

**File:** `test_e2e_playwright.py`

**Coverage:**
- ✅ Complete bot workflow execution
- ✅ GitHub Actions workflow validation
- ✅ API integration with request interception
- ✅ Configuration validation
- ✅ Error recovery workflows
- ✅ Performance validation
- ✅ Browser automation for UI components
- ✅ Screenshot and video recording for debugging

**Playwright Features:**
```python
# Request interception for API mocking
page.route("**/*", handle_route)

# Screenshot capture
page.screenshot(path="test-results/screenshot.png")

# Network monitoring
intercepted_requests = []
```

## 🛠️ Test Environment Setup

### Environment Variables

For local testing, create a `.env.test` file:

```bash
# Required for tests (can use dummy values)
TWITTER_API_KEY=test_twitter_key
TWITTER_API_SECRET=test_twitter_secret
TWITTER_ACCESS_TOKEN=test_access_token
TWITTER_ACCESS_TOKEN_SECRET=test_access_secret
TWITTER_BEARER_TOKEN=test_bearer_token

# AI providers (at least one required)
OPENAI_API_KEY=test_openai_key
ANTHROPIC_API_KEY=test_anthropic_key
GROK_API_KEY=test_grok_key

# Optional
RUN_LIVE_TESTS=false  # Set to true for live API testing
```

### Test Data Directory Structure

```
test-results/
├── screenshots/     # Playwright screenshots
├── videos/         # Test execution videos
├── traces/         # Playwright traces for debugging  
├── reports/        # Test execution reports
└── coverage/       # Code coverage reports
```

## 🔍 Test Execution Modes

### 1. Unit Tests Only
```bash
python test_viral_prediction.py
python test_bot_integration.py
```

### 2. Integration Tests  
```bash
python test_bot_integration.py
```

### 3. End-to-End Tests
```bash
# Install Playwright first
pip install playwright
playwright install chromium

# Run E2E tests
python test_e2e_playwright.py
```

### 4. Comprehensive Suite
```bash
python run_all_tests.py
```

### 5. GitHub Actions (CI/CD)
```bash
# Trigger via GitHub UI or
gh workflow run test-suite.yml
```

## 📈 Test Reports and Artifacts

### Generated Reports

1. **JSON Test Report** (`test-results/reports/test-report-{timestamp}.json`)
   ```json
   {
     "test_run_info": {
       "timestamp": "2024-01-15T12:00:00",
       "total_duration": 45.32,
       "python_version": "3.11.0"
     },
     "test_results": {...},
     "summary": {
       "total_tests": 4,
       "passed": 3,
       "failed": 1
     }
   }
   ```

2. **Coverage Report** (generated with pytest-cov)
3. **Playwright Traces** (for debugging E2E test failures)
4. **Screenshots** (on test failures)

### Viewing Results

```bash
# View latest test report
ls -la test-results/reports/

# View coverage report
coverage report

# Open Playwright trace for debugging
playwright show-trace test-results/traces/trace-{test}-{timestamp}.zip
```

## 🐛 Debugging Failed Tests

### 1. Unit/Integration Test Failures

```bash
# Run with verbose output
python test_viral_prediction.py -v

# Run specific test
python -m pytest test_bot_integration.py::TestBotIntegration::test_content_generation -v

# Run with debugger
python -m pytest test_bot_integration.py --pdb
```

### 2. E2E Test Failures

```bash
# Run with visible browser
python test_e2e_playwright.py --headed

# Enable debug mode in config
HEADLESS = False
SLOW_MO = 1000  # Slow down operations

# View trace file
playwright show-trace test-results/traces/trace-{timestamp}.zip
```

### 3. Common Issues and Solutions

**Issue:** Playwright browser not found
```bash
# Solution: Install browsers
playwright install chromium
```

**Issue:** Test timeout
```bash
# Solution: Increase timeout in config
DEFAULT_TIMEOUT = 60000  # 60 seconds
```

**Issue:** API rate limits
```bash
# Solution: Use test mode or mocks
bot = SMESocialBot(test_mode=True)
```

## 🔧 Continuous Integration

### GitHub Actions Workflow

The test suite runs automatically on:
- **Push to main/develop branches**
- **Pull requests to main**
- **Manual triggers with options**

**Workflow Features:**
- ✅ Multiple Python versions (3.9, 3.10, 3.11)
- ✅ Parallel test execution
- ✅ Code coverage reporting
- ✅ Artifact collection (screenshots, videos, reports)
- ✅ Security analysis (bandit, safety)
- ✅ Performance benchmarks
- ✅ Live API validation (optional)

### Manual Workflow Triggers

```bash
# Trigger specific test type
gh workflow run test-suite.yml -f test_type=e2e

# Enable live API testing
gh workflow run test-suite.yml -f run_live_tests=true
```

## 📋 Test Maintenance

### Adding New Tests

1. **For new features:** Add tests in appropriate test file
2. **For new components:** Create new test file following naming pattern
3. **For E2E workflows:** Add to `test_e2e_playwright.py`

### Updating Test Data

1. **Mock responses:** Update in `playwright.config.py`
2. **Test tweets:** Add to test file constants
3. **Expected scores:** Update based on algorithm changes

### Performance Considerations

- ✅ Mock external APIs to avoid rate limits
- ✅ Use `test_mode=True` for bot initialization
- ✅ Implement proper cleanup in tearDown methods
- ✅ Parallel test execution where possible
- ✅ Reasonable timeouts for CI/CD environments

## 🎯 Testing Best Practices

### 1. Test Isolation
- Each test should be independent
- Use proper setup/teardown methods
- Mock external dependencies

### 2. Comprehensive Coverage
- Test both success and failure scenarios
- Include edge cases and boundary conditions
- Verify error handling and recovery

### 3. Maintainable Tests
- Clear test names and descriptions
- Proper test data management
- Regular test maintenance and updates

### 4. Performance Testing
- Monitor test execution time
- Use benchmarking for critical algorithms
- Optimize slow tests

## 🚨 Test Quality Gates

Before deployment, all tests must:

- ✅ **Pass all unit tests** (viral prediction, bot components)
- ✅ **Pass integration tests** (component interactions)
- ✅ **Pass E2E tests** (complete workflows)
- ✅ **Achieve >80% code coverage** on critical paths
- ✅ **Pass security analysis** (no high-severity issues)
- ✅ **Meet performance benchmarks** (response times)

## 📞 Support and Troubleshooting

For test-related issues:

1. **Check test logs** in `test-results/` directory
2. **Review GitHub Actions** workflow runs
3. **Examine Playwright traces** for E2E failures
4. **Verify environment variables** are properly set
5. **Update dependencies** if tests are failing

---

**Remember:** Tests are your safety net! Keep them updated, comprehensive, and reliable. 🛡️

Happy testing! 🧪✨