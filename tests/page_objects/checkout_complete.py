import allure
from playwright.sync_api import Page, expect

class CheckoutCompletePage:
    PATH = "/checkout-complete.html"

    def __init__(self, page: Page):
      self.page = page

      self._back_home_button = self.page.locator("#back-to-products")  # Using the ID, which is best practice
      self._complete_header = self.page.locator("[data-test='complete-header']") # Better selector
      self._complete_text = self.page.locator("[data-test='complete-text']") # Added for more thorough checking

    @allure.step("Clicking back home button")
    def click_back_home(self):
        self._back_home_button.click()

    @allure.step("Verifying order completion")
    def verify_order_completion(self):
      """
        Verifies the order completion message and other elements on the page.
      """
      with allure.step("Verifying back home button is visible"):
        expect(self._complete_header).to_be_visible()
      with allure.step("Verifying complete header text"):
        expect(self._complete_header).to_have_text("Thank you for your order!") # More specific check
      with allure.step("Verifying complete text is visible"):
        expect(self._complete_text).to_be_visible()
      with allure.step("Verifying complete text text"):
        expect(self._complete_text).to_have_text("Your order has been dispatched, and will arrive just as fast as the pony can get there!") # More specific check
      with allure.step("Verifying back home button is visible"):
        expect(self._back_home_button).to_be_visible()  # Ensure button is present
