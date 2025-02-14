import allure
import pytest

from playwright.sync_api import Page
from tests.page_objects.cart_item import CartItem

class CartPage:
  PATH = "/cart.html"

  def __init__(self, page: Page):
    self.page = page

    self.cart_items = page.locator('[data-test="inventory-item"]')
    self.checkout_button = page.locator('[data-test="checkout"]')
    self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

  @allure.step("Getting cart items")
  def get_cart_items(self) -> list[CartItem]:
    cart_items = self.cart_items.all()
    cart_li = []
    for item in cart_items:
      item_node = CartItem(item)
      cart_li.append(item_node)

    return cart_li