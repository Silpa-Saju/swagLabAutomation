import pytest
import time
from playwright.sync_api import BrowserContext, Page
from tests.page_objects.login_page import LoginPage

@pytest.fixture(scope="function")
def login_page(context: BrowserContext, env):
  """Navigates to the login page and ensures it is ready for testing."""
  with context.new_page() as page:
    page.goto(env["base_url"])
    yield page

def test_login_should_succeed(login_page: Page, env):
  """Verify successful login with valid credentials."""
  page = LoginPage(login_page)
  page.perform_login(env["username"], env["password"])
  assert page.has_logged_in()

@pytest.mark.parametrize("username,password,error_txt", [
  ('', '', 'Username is required'),
  ('wrong_user', '', 'Password is required'),
  ('wrong', 'wrong', "do not match any user")
])
def test_login_field_validation(login_page: Page, username, password, error_txt):
  """Check validation messages for invalid credentials."""
  login = LoginPage(login_page)
  login.perform_login(username, password)

  assert not login.has_logged_in()
  error_message = login.get_error_message()
  assert error_message is not None and error_txt in error_message

def test_login_ui_elements_present(login_page: Page):
  """Ensure login page has required UI elements."""
  login = LoginPage(login_page)
  
  assert login.login_button.is_visible()
  assert login.username_field.is_visible()
  assert login.password_field.is_visible()
