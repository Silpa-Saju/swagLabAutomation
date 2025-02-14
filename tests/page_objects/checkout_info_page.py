import allure
from playwright.sync_api import Page

class CheckoutInfoPage:
  PATH = "/checkout-step-one.html"

  def __init__(self, page: Page):
    self.page = page

    self.first_name = page.locator('[data-test="firstName"]')
    self.last_name = page.locator('[data-test="lastName"]')
    self.zip_code = page.locator('[data-test="postalCode"]')

    self.continue_button = page.locator('[data-test="continue"]')
    self.error_message = page.locator('.error-message-container')

  @allure.step("Getting error message")
  def get_error_message(self):
    if not self.error_message.is_visible():
      return None
    return self.error_message.text_content()

  @allure.step("Setting first name")
  def set_first_name(self, first_name: str):
    self.first_name.fill(first_name)

  @allure.step("Setting last name")
  def set_last_name(self, last_name: str):
    self.last_name.fill(last_name)

  @allure.step("Setting zip code")
  def set_zip_code(self, zip_code: str):
    self.zip_code.fill(zip_code)

  @allure.step("Getting first name")
  def get_first_name(self):
    return self.first_name.input_value()

  @allure.step("Getting last name")
  def get_last_name(self):
    return self.last_name.input_value()

  @allure.step("Getting zip code")
  def get_zip_code(self):
    return self.zip_code.input_value()

  @allure.step("Clicking continue button")
  def continue_button_click(self):
    self.continue_button.click()