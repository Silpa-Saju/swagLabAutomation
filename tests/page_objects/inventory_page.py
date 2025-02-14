import allure

from playwright.sync_api import Page
from tests.page_objects.inventory_item import InventoryItem

class InventoryPage:
  PATH = "/inventory.html"

  def __init__(self, page: Page):
    self.page = page

    self.inventory_list = page.locator('[data-test="inventory-item"]')
    self.inventory_item = page.locator('[data-test="inventory-item"]')
    self.sort_by = page.locator('[data-test="product-sort-container"]')
 
  @allure.step("Setting sort by")
  def set_sort_by(self, sort):
    with allure.step("Finding available sort options"):
      all_options = self.sort_by.locator('option').all()

    with allure.step("Verifying sort option is available"):
      available_options = [option.get_attribute('value') for option in all_options ]
      assert sort in available_options

    with allure.step("Selecting sort option"):
      self.sort_by.select_option(sort)
  
  @allure.step("Getting inventory items")
  def get_inventory_items(self) -> list[InventoryItem]:
    with allure.step("Getting inventory items"):
      inventory_items = self.inventory_list.all()

    inventory_li = []
    for item in inventory_items:
      item_node = InventoryItem(item)
      inventory_li.append(item_node)

    return inventory_li
  