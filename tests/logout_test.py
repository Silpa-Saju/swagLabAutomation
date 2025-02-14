import allure
import re
import pytest
from urllib.parse import urljoin

from playwright.sync_api import BrowserContext, Page, expect

from tests.page_objects.login_page import LoginPage
from tests.page_objects.shared.nav_bar import NavBar
from tests.page_objects.shared.side_bar import SideBar

@pytest.fixture(scope="function")
def home_page(context: BrowserContext, env):
  """
  Fixture to log in to the application and return a Playwright page object.
  """
  with context.new_page() as page, allure.step("Setup login"):
    page.goto(urljoin(env["base_url"], LoginPage.PATH))
    login_page = LoginPage(page)
    login_page.perform_login(env["username"], env["password"])
    assert login_page.has_logged_in()
    yield page

def test_logout(home_page: Page):
  """
  Test case for verifying the logout functionality.
  """
  nav_bar = NavBar(home_page)
  nav_bar.click_burger_menu()
  side_bar = SideBar(home_page)

  side_bar.logout()

  with allure.step("Waiting for home page to load"):
    expect(home_page).to_have_url(re.compile(".*" + LoginPage.PATH))
    assert not LoginPage.is_logged_in(home_page.context)
