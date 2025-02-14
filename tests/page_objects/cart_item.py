import allure
import re

from playwright.sync_api import Locator

class CartItem:
  def __init__(self, item_node: Locator):
    self.item_node = item_node
    self.name = item_node.locator("[data-test='inventory-item-name']")
    self.price = item_node.locator("[data-test='inventory-item-price']")
    self.quantity = item_node.locator("[data-test='item-quantity']")
    self.remove = item_node.locator('[data-test^="remove-"]')

  @allure.step("Clicking remove button")
  def click_remove(self):
    self.remove.click()

  @allure.step("Verifying item is visible")
  def is_visible(self):
    try:
      assert self.item_node.is_visible()
      assert self.name.is_visible()
      assert self.price.is_visible()
      assert self.quantity.is_visible()
    except:
      return False
    return True

  @allure.step("Getting price")
  def get_price(self):
    return float(re.sub(r'[^\d\.]', '', self.price.inner_text()))

  @allure.step("Getting quantity")  
  def get_quantity(self):
    return int(self.quantity.inner_text())

  @allure.step("Getting name")
  def get_name(self):
    return self.name.inner_text()
  
  @allure.step("Getting total price")
  def total_price(self):
    return self.get_price() * self.get_quantity()

  @allure.step("Serializing item")
  def serialize(self):
    return {
      "name": self.name.inner_text(),
      "price": self.get_price(),
      "quantity": self.get_quantity()
    }
  
  