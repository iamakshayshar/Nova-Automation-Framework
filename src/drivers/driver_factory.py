import os
import platform
import shutil
import tempfile
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from src.utils.logger import logger

CHROME_DRIVER_URL_ARM = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/138.0.7204.184/mac-arm64/chromedriver-mac-arm64.zip"

# Track temp profile dirs for cleanup
_created_profiles = []

def _build_driver(browser, headless):
    system = platform.system().lower()
    machine = platform.machine().lower()

    if browser.lower() == "chrome":
        options = Options()

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        # Fix parallel Chrome profile conflict
        user_data_dir = tempfile.mkdtemp(prefix="chrome-profile-")
        _created_profiles.append(user_data_dir)
        options.add_argument(f"--user-data-dir={user_data_dir}")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        # Try to log Chrome version
        try:
            chrome_version = subprocess.check_output(
                ["google-chrome", "--version"], text=True
            ).strip()
        except Exception:
            chrome_version = "Unknown"

        logger.info(f"Detected system: {system}, arch: {machine}")
        logger.info(f"Using Chrome version: {chrome_version}")
        logger.info(f"Temporary Chrome profile path: {user_data_dir}")

        driver = webdriver.Chrome(options=options)
        return driver

    raise ValueError(f"Browser '{browser}' is not supported on {system}/{machine}")

def cleanup_profiles():
    """Remove all temp Chrome profile dirs created during the session."""
    for profile_dir in _created_profiles:
        try:
            shutil.rmtree(profile_dir, ignore_errors=True)
            logger.info(f"Deleted temp Chrome profile: {profile_dir}")
        except Exception as e:
            logger.warning(f"Could not delete {profile_dir}: {e}")


def _download_arm64_chromedriver():
    cache_dir = os.path.expanduser("~/.wdm/arm64")
    os.makedirs(cache_dir, exist_ok=True)
    driver_zip = os.path.join(cache_dir, "chromedriver.zip")

    # Download if not exists
    if not os.path.exists(os.path.join(cache_dir, "chromedriver")):
        logger.info("Downloading ARM64 ChromeDriver for Apple Silicon...")
        r = requests.get(CHROME_DRIVER_URL_ARM, stream=True)
        with open(driver_zip, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract
        with zipfile.ZipFile(driver_zip, "r") as zip_ref:
            zip_ref.extractall(cache_dir)

        # Find the driver file inside extracted folders
        for root, _, files in os.walk(cache_dir):
            if "chromedriver" in files:
                driver_bin = os.path.join(root, "chromedriver")
                os.chmod(driver_bin, 0o755)
                return driver_bin

    # Already downloaded
    for root, _, files in os.walk(cache_dir):
        if "chromedriver" in files:
            return os.path.join(root, "chromedriver")

    raise RuntimeError("ARM64 ChromeDriver could not be downloaded")
