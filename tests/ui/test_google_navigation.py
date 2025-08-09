import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.ui
def test_google_search(driver, test_data):
    keyword = test_data["google_search"]["keyword"]

    driver.get("https://www.google.com")

    # Accept cookies if shown (Google sometimes prompts in EU/US)
    try:
        agree_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='I agree']]"))
        )
        agree_button.click()
    except:
        pass  # No cookie banner shown

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(keyword)
    search_box.submit()

    # Wait for title to contain the keyword
    WebDriverWait(driver, 10).until(EC.title_contains(keyword))

    assert keyword.lower() in driver.title.lower(), f"Expected '{keyword}' in title but got '{driver.title}'"
