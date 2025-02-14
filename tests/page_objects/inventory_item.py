import allure
import re

from playwright.sync_api import Locator

class InventoryItem:
  def __init__(self, item_node: Locator):
    self.item_node = item_node

    self.name = item_node.locator("[data-test='inventory-item-name']")
    self.price = item_node.locator("[data-test='inventory-item-price']")
    self.description = item_node.locator("[data-test='inventory-item-description']")
    self.image = item_node.locator("img.inventory_item_img")

    self.add_to_cart_btn = item_node.locator('[data-test^="add-to-cart"]')
    self.remove_from_cart_btn = item_node.locator('[data-test^="remove-"]')
  
  @allure.step("Removing item from cart")
  def remove_from_cart(self):
    self.remove_from_cart_btn.click()
  
  @allure.step("Adding item to cart")
  def add_to_cart(self):
    self.add_to_cart_btn.click()

  @allure.step("Serializing item")
  def serialize(self):
    with allure.step("Getting name"):
      name = self.name.inner_text()
    
    with allure.step("Getting price"):
      price = float(re.sub(r'[^\d\.]', '', self.price.inner_text()))
    
    with allure.step("Getting description"):
      description = self.description.inner_text()
    
    with allure.step("Getting image"):
      image = self.image.get_attribute('src')
    
    return {
      "name": name ,
      "price": price,
      "description": description,
      "image": image
    }
  
  @allure.step("Verifying item is in cart")
  def in_cart(self):
    return self.remove_from_cart_btn.is_visible()