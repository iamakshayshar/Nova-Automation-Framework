import os
import platform
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

from src.utils.logger import logger

CHROME_DRIVER_URL_ARM = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/138.0.7204.184/mac-arm64/chromedriver-mac-arm64.zip"

def _build_driver(browser, headless):
    system = platform.system().lower()
    machine = platform.machine().lower()

    if browser.lower() == "chrome":
        logger.info(f"Detected system: {system}, arch: {machine}")

        # Special handling for Apple Silicon
        if system == "darwin" and machine == "arm64":
            driver_path = _download_arm64_chromedriver()
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            driver_path = ChromeDriverManager().install()

        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=options)

    # ... keep Firefox code as before ...


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
