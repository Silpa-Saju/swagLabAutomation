import re
import allure
import pytest
from urllib.parse import urljoin
from playwright.sync_api import BrowserContext, Page, expect

from tests.page_objects.shared.nav_bar import NavBar
from tests.page_objects.inventory_page import InventoryPage

def test_inventory_items_are_displayed(inventory_page: Page, env):
  """Ensures that all inventory items have visible and non-empty properties, and their images load correctly."""
  inventory = InventoryPage(inventory_page)
  items = inventory.get_inventory_items()

  if len(items) == 0:
    pytest.skip("No items present in inventory")

  for idx, item in zip(range(len(items)), items):
    with allure.step(f"Verifying item {idx}"):
      for key, prop in [ ('name', item.name), ('price', item.price), ('description', item.description) ]:
        with allure.step(f"Verifying {key} is visible and non-empty"):
          assert prop.is_visible() and len(prop.text_content()) > 0, f"{prop} is not visible or empty"

      with allure.step(f"Verifying image {item.image.get_attribute('src')} loads correctly"):
        img_src = item.image.get_attribute('src')
        img_url = urljoin(env["base_url"], img_src)
        res = inventory_page.request.get(img_url)
        assert res.status == 200, f"Image {img_url} failed to load with status {res.status}"

@pytest.mark.parametrize("sort,key,order", [
  ('az', 'name', 'asc'),
  ('za', 'name', 'desc'),
  ('lohi', 'price', 'asc'),
  ('hilo', 'price', 'desc')
])
def test_sort_by(inventory_page: Page, sort, key, order):
  """Verifies that sorting functionality works correctly for different criteria."""
  inventory = InventoryPage(inventory_page)
  items = inventory.get_inventory_items()
  if len(items) == 0:
    pytest.skip("No items present in inventory")

  with allure.step("Sorting items"):
    li = [item.serialize() for item in items]
    li = sorted(li, key=lambda x: x[key], reverse=order == 'desc')
  
  inventory.set_sort_by(sort)
  sorted_li = [item.serialize() for item in inventory.get_inventory_items()]
  
  with allure.step("Verifying sorting results"):
    for i in range(len(li)):
      assert li[i]['name'] == sorted_li[i]['name'], f"Sorting mismatch at index {i}: Expected {li[i]['name']}, got {sorted_li[i]['name']}"
      assert li[i]['price'] == sorted_li[i]['price'], f"Price mismatch at index {i}: Expected {li[i]['price']}, got {sorted_li[i]['price']}"

