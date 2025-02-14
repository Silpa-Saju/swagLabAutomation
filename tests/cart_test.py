import allure
import pytest
from urllib.parse import urljoin
from playwright.sync_api import BrowserContext, Page
from tests.page_objects.shared.nav_bar import NavBar
from tests.page_objects.inventory_page import InventoryPage
from tests.page_objects.cart_page import CartPage

def test_add_to_cart(inventory_page: Page):
  """
  Test to verify that items can be added to the cart and the cart count updates correctly.
  """
  inventory = InventoryPage(inventory_page)
  navbar = NavBar(inventory_page)
  items = inventory.get_inventory_items()

  if len(items) == 0:
    pytest.skip("No items to add to cart")
    return

  assert navbar.get_item_count() == 0
  total_items_in_cart = 0

  for item in items:
    item.add_to_cart()
    total_items_in_cart += 1
    assert navbar.get_item_count() == total_items_in_cart

def test_cart_persistence_across_navigation(inventory_page: Page, env):
  """
  Test to ensure that items added to the cart persist across page navigation.
  """
  inventory = InventoryPage(inventory_page)
  navbar = NavBar(inventory_page)
  items = inventory.get_inventory_items()

  if len(items) == 0:
    pytest.skip("No items to add to cart")
    return

  if len(items) > 0:
    items[0].add_to_cart()
  
  base_url = env['base_url']
  with allure.step("Navigating away from inventory page"):
    inventory_page.goto(base_url)  # Navigate away
    inventory_page.goto(urljoin(base_url, InventoryPage.PATH))  # Return to inventory
    inventory_page.wait_for_load_state('domcontentloaded')
  
  assert navbar.get_item_count() == 1

def test_remove_from_cart(inventory_page: Page):
  """
  Test to verify that items can be removed from the cart and the cart count updates correctly.
  """
  inventory = InventoryPage(inventory_page)
  navbar = NavBar(inventory_page)
  items = inventory.get_inventory_items()

  if len(items) == 0:
    pytest.skip("No items to add to cart")
    return

  # Add all items to the cart
  for item in items:
    if item.in_cart():
      continue
    item.add_to_cart()

  total_items_in_cart = len(items)
  assert navbar.get_item_count() == total_items_in_cart

  # Remove items from the cart
  for item in items:
    item.remove_from_cart()
    total_items_in_cart -= 1
    assert navbar.get_item_count() == total_items_in_cart

  assert navbar.get_item_count() == 0

def test_ensure_cart_page_has_items(inventory_page: Page):
  """
  Test to verify that the cart page correctly displays the items added from the inventory page.
  """
  inventory = InventoryPage(inventory_page)
  navbar = NavBar(inventory_page)
  items = inventory.get_inventory_items()

  if len(items) == 0:
    pytest.skip("No items to add to cart")
    return

  # Add all items to the cart
  for item in items:
    if item.in_cart():
      continue
    item.add_to_cart()
  
  serialized_items = [item.serialize() for item in items]
  items_map = {item['name']: item for item in serialized_items}

  # Navigate to the cart page
  navbar.click_shopping_cart_link()
  cart_page = CartPage(inventory_page)
  cart_items = cart_page.get_cart_items()

  assert len(cart_items) == len(serialized_items)

  for item in cart_items:
    assert item.get_name() in items_map
    assert item.get_quantity() > 0
    assert item.get_price() == items_map[item.get_name()]['price']

def test_cart_page_remove_item(inventory_page: Page):
  """
  Test to verify that items can be removed from the cart page,
  and that the inventory page reflects the updated cart count after navigation.
  """
  inventory = InventoryPage(inventory_page)
  navbar = NavBar(inventory_page)
  items = inventory.get_inventory_items()

  if len(items) == 0:
    pytest.skip("No items to add to cart")

  # Add all items to the cart
  for item in items:
    item.add_to_cart()

  navbar.click_shopping_cart_link()
  cart_page = CartPage(inventory_page)
  cart_items = cart_page.get_cart_items()
  initial_cart_count = len(cart_items)

  if initial_cart_count > 0:
    cart_items[0].click_remove()
    assert len(cart_page.get_cart_items()) == initial_cart_count - 1

    # Go back to inventory and check count
    inventory_page.go_back()
    inventory_page.wait_for_load_state('domcontentloaded')
    assert navbar.get_item_count() == initial_cart_count - 1
