# 🚀 Nova Automation Framework

[![CI Build](https://github.com/iamakshayshar/Nova-Automation-Framework/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/iamakshayshar/Nova-Automation-Framework/actions/workflows/tests.yml)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/github/license/iamakshayshar/Nova-Automation-Framework?color=green)
![Last Commit](https://img.shields.io/github/last-commit/iamakshayshar/Nova-Automation-Framework)
![Open Issues](https://img.shields.io/github/issues/iamakshayshar/Nova-Automation-Framework)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

Nova is an **end-to-end automation testing framework** for both **UI** and **API** testing — optimized for speed, reliability, and CI/CD pipelines.  
It’s built using `pytest`, `selenium`, and `requests`, with parallel execution, retry logic, and screenshot capture baked in.

---

## ✨ Features
- 🖥 **UI Testing** — Selenium WebDriver (Chrome, headless & headed)
- 🔌 **API Testing** — Requests-based testing
- 📸 **Automatic Screenshots** on UI failures
- 🔁 **Retry Logic** for flaky tests
- ⚡ **Parallel Execution** with pytest-xdist
- 🧪 **Environment-Specific Test Data** via YAML
- ☁ **CI/CD Ready** with GitHub Actions integration
- 📊 **Easy Reporting** (Allure/ReportPortal ready)

---

## 📂 Structure
```text
Nova-Automation-Framework/
│
├── src/
│   ├── drivers/         # WebDriver factory
│   ├── pages/           # Page Object Models
│   ├── utils/           # Logger, config reader, helpers
│
├── tests/
│   ├── ui/              # UI test cases
│   ├── api/             # API test cases
│
├── testdata.yaml        # QA & Staging data
├── requirements.txt     # Python dependencies
├── conftest.py          # Pytest fixtures/hooks
└── .github/workflows/   # GitHub Actions workflows
```

⚙️ Setup

1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/Nova-Automation-Framework.git
cd Nova-Automation-Framework
```
2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```


🖥 Running UI Tests
```bash
pytest tests/ui/test_google_navigation.py --env=qa --headed
--env → Choose qa or staging
--headed → Shows browser (omit for headless)
```
🔌 Running API Tests
```bash
pytest tests/api/test_sample_api.py --env=qa
```
🤖 CI/CD Integration

- Fully integrated with GitHub Actions
- Runs on every push or pull request
- Installs Chrome + Chromedriver 
- Executes UI & API tests in one pipeline 
- Uploads screenshots & reports as artifacts

🛠 Tech Stack

1. Pytest 
2. Selenium 
3. Requests 
4. PyYAML 
5. Pytest-xdist 
6. Pytest-rerunfailures 
7. GitHub Actions

📜 License
This project is licensed under the MIT License — see LICENSE.

