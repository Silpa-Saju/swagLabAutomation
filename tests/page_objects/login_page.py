import allure

from playwright.sync_api import Page, BrowserContext

class LoginPage:
  PATH = "/"
  def __init__(self, page: Page):
    self.page = page

    self.username_field = page.locator("[data-test='username']")
    self.password_field = page.locator("[data-test='password']")
    self.login_button = page.locator("[data-test='login-button']")
    self.error_message = page.locator("[data-test='error']")

    # helper selector to wait for the login action to complete
    self.error_or_success = page.locator('[data-test="logout-sidebar-link"],[data-test="error"]')
  
  @allure.step("Setting username")
  def set_username(self, username: str):
    self.username_field.fill(username)

  @allure.step("Getting username field")
  def get_username_field(self):
    return self.username_field.text_content()

  @allure.step("Getting error message")
  def get_error_message(self):
    if not self.error_message.is_visible():
      return None
    return self.error_message.text_content()

  @allure.step("Setting password")
  def set_password(self, password: str):
    self.password_field.fill(password) 

  @allure.step("Clicking login button")
  def click_login(self):
    self.login_button.click() 
  
  def is_logged_in(context: BrowserContext):
    cookies = context.cookies()
    for cookie in cookies:
      if cookie['name'] == 'session-username':
        return True
    return False
  
  @allure.step("Verifying login")
  def has_logged_in(self):
    return LoginPage.is_logged_in(self.page.context)

  @allure.step("Performing login")
  def perform_login(self, username: str, password: str): 
    self.set_username(username)
    self.set_password(password)
    self.click_login()

    # wait for either the logout sidebar link or the error message to appear
    self.error_or_success.wait_for(state='visible')

