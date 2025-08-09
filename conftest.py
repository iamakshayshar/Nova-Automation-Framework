import os
import shutil
import stat
import yaml
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime


# ---------- Utility Functions ----------
def ensure_executable(path):
    """Ensure a file is executable."""
    if not os.access(path, os.X_OK):
        try:
            os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
        except Exception as e:
            print(f"[!] Could not set execute permission for {path}: {e}")
            return False
    return True


def get_clean_driver_path(manager_class):
    """Force-select the actual driver binary, avoiding THIRD_PARTY_NOTICES issue."""
    driver_path = manager_class().install()

    if "THIRD_PARTY_NOTICES" in os.path.basename(driver_path) or not ensure_executable(driver_path):
        print(f"[!] webdriver-manager returned a bad path: {driver_path}")
        driver_dir = os.path.dirname(driver_path)

        # Look for a proper binary in the folder
        for file in os.listdir(driver_dir):
            if file == "chromedriver" and os.path.isfile(os.path.join(driver_dir, file)):
                correct_path = os.path.join(driver_dir, file)
                if ensure_executable(correct_path):
                    print(f"[+] Found valid driver binary: {correct_path}")
                    return correct_path

        # If still not found, clear cache and reinstall
        print("[!] No valid binary found, clearing cache and reinstalling...")
        shutil.rmtree(os.path.expanduser("~/.wdm"), ignore_errors=True)
        driver_path = manager_class().install()

    return driver_path


# ---------- Pytest Hooks ----------
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests against: qa or staging"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run UI tests: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )


@pytest.fixture(scope="session")
def config(request):
    return {
        "env": request.config.getoption("--env"),
        "browser": request.config.getoption("--browser"),
        "headless": request.config.getoption("--headless"),
    }


@pytest.fixture(scope="session")
def test_data(config):
    env = config["env"]
    yaml_path = os.path.join("data", "testdata.yaml")

    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"Test data file not found: {yaml_path}")

    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f) or {}

    if env not in data:
        raise ValueError(f"Environment '{env}' not found in testdata.yaml. Available: {list(data.keys())}")

    return data[env]


@pytest.fixture
def driver(config):
    browser = config["browser"].lower()
    headless = config["headless"]

    if browser == "chrome":
        driver_path = get_clean_driver_path(ChromeDriverManager)
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
        service = ChromeService(executable_path=driver_path)
        drv = webdriver.Chrome(service=service, options=options)
    else:
        raise ValueError(f"Browser '{browser}' not supported in this framework.")

    drv.maximize_window()
    yield drv
    drv.quit()


# ---------- Screenshot on Failure ----------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on UI test failure."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver_fixture = item.funcargs.get("driver", None)
        if driver_fixture:
            os.makedirs("reports/screenshots", exist_ok=True)
            screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = os.path.join("reports/screenshots", screenshot_name)
            driver_fixture.save_screenshot(path)
            print(f"\n[!] Screenshot saved to: {path}")
