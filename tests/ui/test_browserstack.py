import pytest

from src.pages.Homepage import Homepage
from src.pages.SignInPage import SignInPage


@pytest.mark.ui
def test_browserstack(driver, test_data):
    driver.get("https://bstackdemo.com/")

    homepage = Homepage(driver)
    sign_in_page = SignInPage(driver)

    homepage.click_sign_in()

    sign_in_page.select_username()
    sign_in_page.select_password()
    sign_in_page.click_login()
    homepage.get_username()
    driver.quit()
