# Allure Report Setup Guide

## Quick Reference

After running tests with `pytest`, generate and view the Allure report:

```bash
allure serve reports/allure
```

This single command will:
- ✅ Generate HTML report from test results
- ✅ Start a local web server
- ✅ Automatically open the report in your browser

---

## Installation

### Prerequisites

- **Java 8 or higher** (required for Allure)
  ```bash
  java -version
  ```

### Install Allure Command-Line Tool

#### macOS (Homebrew)

```bash
brew install allure
```

Verify installation:
```bash
allure --version
```

#### Linux

**Option 1: Using Package Manager (Debian/Ubuntu)**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**Option 2: Manual Installation**
```bash
# Download Allure
wget https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz

# Extract
tar -zxvf allure-2.24.0.tgz

# Move to /opt
sudo mv allure-2.24.0 /opt/allure

# Create symlink
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure

# Verify
allure --version
```

#### Windows

**Option 1: Using Scoop**
```bash
scoop install allure
```

**Option 2: Using Chocolatey**
```bash
choco install allure
```

**Option 3: Manual Installation**
1. Download from: https://github.com/allure-framework/allure2/releases
2. Extract to `C:\allure`
3. Add `C:\allure\bin` to PATH environment variable
4. Verify: `allure --version`

---

## Working with Allure Reports

### Generate and View Report (Recommended)

**Single command** - Generate report and open in browser:
```bash
allure serve reports/allure
```

This is the **easiest** way to view reports!

### Generate Static Report

Generate HTML report to a specific directory:

```bash
allure generate reports/allure -o reports/allure-report --clean
```

Options:
- `-o` : Output directory for HTML report
- `--clean` : Clean output directory before generation

### Open Existing Report

If you've already generated a static report:

```bash
allure open reports/allure-report
```

### Clear Old Results

Before running new tests, you may want to clear old results:

```bash
rm -rf reports/allure/*
```

Then run tests again:
```bash
pytest
```

---

## Allure Report Features

### 📊 Overview Dashboard

The main page shows:
- Total tests executed
- Pass/fail statistics
- Test execution duration
- Trend graphs (when multiple runs available)
- Success rate percentage

### 📈 Behaviors

Tests organized by:
- **Epic** → **Feature** → **Story** hierarchy
- Example: JSONPlaceholder API → Posts Management → Get All Posts

### 📦 Suites

Traditional test suite organization:
- By test classes
- By test packages
- By test modules

### 📉 Graphs

Visual analytics:
- Status chart (passed/failed/broken)
- Severity distribution
- Duration chart
- Test execution timeline

### 🏷️ Tags

Filter tests by custom tags:
- `API`, `GET`, `POST`, `PUT`, `DELETE`
- `Negative`, `Validation`
- Custom categories

### ⏱️ Timeline

Visual timeline showing:
- Test execution sequence
- Parallel execution (if any)
- Duration of each test

### 📎 Attachments

Automatically includes:
- Console output (stdout/stderr)
- Logs
- Request/response data
- Screenshots (if added)

### 📋 Categorization

Tests organized by:
- **Severity**: Critical, Normal, Minor, Trivial
- **Status**: Passed, Failed, Broken, Skipped
- **Tags**: Custom categorization

---

## Continuous Integration

### GitHub Actions

The CI workflow automatically:
1. Runs tests with pytest
2. Generates Allure results
3. Creates HTML report
4. Uploads artifacts

**Viewing CI Reports:**

1. Go to **Actions** tab in GitHub
2. Click on workflow run
3. Download **allure-report** artifact
4. Extract and open `index.html`

---

## Advanced Usage

### Running Specific Test Subsets

**Smoke tests only:**
```bash
pytest -m smoke
allure serve reports/allure
```

**Regression tests only:**
```bash
pytest -m regression
allure serve reports/allure
```

### Adding History Trends

To see test trends across multiple runs:

```bash
# First run
pytest
allure generate reports/allure -o reports/allure-report

# Copy history for next run
cp -r reports/allure-report/history reports/allure/

# Second run
pytest
allure generate reports/allure -o reports/allure-report

# Now you'll see trends!
```

### Environment Information

Add environment details to reports by creating `environment.properties`:

```bash
cat > reports/allure/environment.properties << EOF
Browser=Chrome
OS=macOS 14.0
Python=3.11
Environment=QA
API.Base.URL=https://jsonplaceholder.typicode.com
EOF
```

Then generate report:
```bash
allure generate reports/allure -o reports/allure-report --clean
allure open reports/allure-report
```

### Custom Categories

Create `categories.json` for test categorization:

```bash
cat > reports/allure/categories.json << EOF
[
  {
    "name": "API Failures",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*API.*"
  },
  {
    "name": "Validation Errors",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*validation.*"
  }
]
EOF
```

---

## Troubleshooting

### "Command not found: allure"

**Solution:**
- Verify Java is installed: `java -version`
- Install Allure (see Installation section above)
- Check PATH: `echo $PATH` (should include Allure bin directory)

### "No results found"

**Solution:**
- Ensure tests have run: `pytest`
- Check results exist: `ls -la reports/allure/`
- Verify pytest.ini configuration

### Report shows no data

**Solution:**
- Ensure allure-pytest is installed: `pip list | grep allure`
- Check pytest plugins: `pytest --version` (should show allure-pytest)
- Verify pytest.ini has correct alluredir setting

### Browser doesn't open automatically

**Solution:**
- Manually open URL shown in console (usually `http://localhost:PORT`)
- Or generate static report: `allure generate ...` and open index.html

---

## Allure Report Structure

```
reports/
├── allure/                          # Raw test results (JSON)
│   ├── *-result.json               # Test case results
│   ├── *-container.json            # Test containers/fixtures
│   ├── *-attachment.txt            # Logs and attachments
│   └── environment.properties      # Environment info (optional)
│
└── allure-report/                  # Generated HTML report
    ├── index.html                  # Main report page
    ├── data/                       # Report data
    ├── history/                    # Historical trends
    ├── styles.css                  # Styling
    └── ...                         # Other assets
```

---

## Reference Links

- **Allure Documentation**: https://allurereport.org/docs/pytest/
- **Allure GitHub**: https://github.com/allure-framework/allure-python
- **Allure Examples**: https://github.com/allure-examples/pytest-pip
- **Allure Releases**: https://github.com/allure-framework/allure2/releases

---

## Quick Commands Cheat Sheet

```bash
# Install Allure (macOS)
brew install allure

# Run tests
pytest

# View report (easiest)
allure serve reports/allure

# Generate static report
allure generate reports/allure -o reports/allure-report --clean

# Open existing report
allure open reports/allure-report

# Clear old results
rm -rf reports/allure/*

# Run smoke tests only
pytest -m smoke

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_posts_api.py::TestPostsAPI::test_get_all_posts
```

---

## Tips & Best Practices

✅ **Use `allure serve`** for quick report viewing  
✅ **Keep test results** across runs to see trends  
✅ **Add environment.properties** for better context  
✅ **Use Allure decorators** in tests for rich metadata  
✅ **Attach screenshots/logs** for debugging  
✅ **Categorize tests** with tags and severity  
✅ **Review timeline** to optimize test execution  

---

**Happy Testing! 🎉**

