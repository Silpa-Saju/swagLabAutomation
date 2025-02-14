import allure
import re

from playwright.sync_api import Page
from tests.page_objects.cart_item import CartItem

class CheckoutFinalizePage:
  PATH = "/checkout-step-two.html"

  def __init__(self, page: Page):
    self.page = page

    self.finish_button = page.locator('[data-test="finish"]')
    self.cancel_button = page.locator('[data-test="cancel"]')
    self.cart_item = page.locator('[data-test="inventory-item"]')

    self.sub_total_price_label = page.locator('[data-test="subtotal-label"]')
    self.tax_label = page.locator('[data-test="tax-label"]')
    self.total_label = page.locator('[data-test="total-label"]')

  @allure.step("Getting sub total price")
  def get_sub_total_price(self):
    return float(re.sub(r'[^\d\.]', '', self.sub_total_price_label.inner_text()))
  
  @allure.step("Getting tax")
  def get_tax(self):
    return float(re.sub(r'[^\d\.]', '', self.tax_label.inner_text()))
  
  @allure.step("Getting total")
  def get_total(self):
    return float(re.sub(r'[^\d\.]', '', self.total_label.inner_text()))

  @allure.step("Getting cart items")
  def get_cart_items(self) -> list[CartItem]:
    cart_items = self.cart_item.all()
    cart_li = []
    for item in cart_items:
      item_node = CartItem(item)
      cart_li.append(item_node)

    return cart_li

  @allure.step("Clicking finish button")
  def click_finish(self):
    self.finish_button.click() 
  
  @allure.step("Clicking cancel button")
  def click_cancel(self):
    self.cancel_button.click()