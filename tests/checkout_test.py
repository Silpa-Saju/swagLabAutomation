import allure
import pytest
import re
from urllib.parse import urljoin
from playwright.sync_api import BrowserContext, Page, expect

from tests.page_objects.shared.nav_bar import NavBar
from tests.page_objects.inventory_page import InventoryPage
from tests.page_objects.cart_page import CartPage
from tests.page_objects.checkout_info_page import CheckoutInfoPage
from tests.page_objects.checkout_finalize_page import CheckoutFinalizePage
from tests.page_objects.checkout_complete import CheckoutCompletePage

@pytest.fixture(scope="function")
def inventory_items(inventory_page):
  """Adds all available inventory items to the cart and ensures they are removed after the test."""
  with allure.step("Adding all items to cart"):
    inv_page = InventoryPage(inventory_page)
    items = inv_page.get_inventory_items()
    for item in items:
      if item.in_cart():
        continue
      item.add_to_cart()
    
    yield [item.serialize() for item in items]

  for item in items:
    item.remove_from_cart()

@pytest.fixture(scope="function")
def cart_page(context_with_auth: BrowserContext, env):
  """Navigates to the cart page and ensures it is ready for testing."""
  with context_with_auth.new_page() as page, allure.step("Navigate to cart page"):
    page.goto(urljoin(env["base_url"], CartPage.PATH))
    page.wait_for_load_state('domcontentloaded')
    yield page

@pytest.fixture(scope="function")
def checkout_step_one_page(cart_page: Page, env):
  """Proceeds to the checkout step one page from the cart."""
  with allure.step("Navigate to checkout step one page"):
    cart_page.goto(urljoin(env["base_url"], CheckoutInfoPage.PATH))
    cart_page.wait_for_load_state('domcontentloaded')
    yield cart_page

@pytest.fixture(scope="function")
def checkout_finalize_page(context_with_auth: BrowserContext, env):
  """Loads the final checkout page."""
  with context_with_auth.new_page() as page, allure.step("Navigate to checkout finalize page"):
    page.goto(urljoin(env["base_url"], CheckoutFinalizePage.PATH))
    page.wait_for_load_state('domcontentloaded')
    yield page

def test_can_move_to_checkout(cart_page: Page, inventory_items):
  """Ensures that the checkout button is visible and functional."""
  cart = CartPage(cart_page)
  with allure.step("Verifying checkout button is visible"):
    assert cart.checkout_button.is_visible()
  cart.checkout_button.click()
  cart_page.wait_for_load_state('domcontentloaded')
  with allure.step("Verifying checkout info container is visible"):
    assert cart_page.locator('[data-test="checkout-info-container"]').is_visible()

def test_cannot_move_to_checkout_if_no_items_in_cart(cart_page: Page):
  """Checks that the checkout button is not available when the cart is empty."""
  cart = CartPage(cart_page)
  assert len(cart.get_cart_items()) == 0

  with allure.step("Verifying checkout button is not visible"):
    assert not cart.checkout_button.is_visible()

def test_validate_checkout_input(checkout_step_one_page: Page, inventory_items):
  """Validates that user input for checkout is correctly stored."""
  info_page = CheckoutInfoPage(checkout_step_one_page)
  info_page.set_first_name('John')
  info_page.set_last_name('Doe')
  info_page.set_zip_code('12345')
  
  assert info_page.get_first_name() == 'John'
  assert info_page.get_last_name() == 'Doe'
  assert info_page.get_zip_code() == '12345'

@pytest.mark.parametrize('firstname,lastname,zipcode,msg', [
  ('', '', '', 'First Name is required'),
  ('', 'Doe', '123', 'First Name is required'),
  ('John', '', '', 'Last Name is required'),
  ('John', '', '123', 'Last Name is required'),
  ('John', 'Doe', '', 'Postal Code is required'),
])
def test_checkout_info_has_validation_errors(inventory_items, checkout_step_one_page: Page, firstname, lastname, zipcode, msg):
  """Checks for proper validation errors when checkout information is incomplete."""
  info_page = CheckoutInfoPage(checkout_step_one_page)
  info_page.set_first_name(firstname)
  info_page.set_last_name(lastname)
  info_page.set_zip_code(zipcode)
  info_page.continue_button_click()
  
  assert msg in info_page.get_error_message()

def test_validate_finalize_checkout_details(inventory_items: [dict], checkout_finalize_page: Page):
  """Verifies that final checkout details match expected values."""
  finalize_page = CheckoutFinalizePage(checkout_finalize_page)
  item_map = {item['name']: item for item in inventory_items}

  with allure.step("Verifying labels are visible"):
    assert finalize_page.sub_total_price_label.is_visible()
    assert finalize_page.tax_label.is_visible()
    assert finalize_page.total_label.is_visible()
  
  cart_items = finalize_page.get_cart_items()
  assert len(cart_items) == len(inventory_items)

  with allure.step("Verifying cart items are visible"):
    for item in cart_items:
      with allure.step(f"Verifying item {item.get_name()} is visible"):
        assert item.is_visible()
        item_name = item.get_name()
        assert item_name in item_map
        assert item.get_price() == item_map[item_name]['price']
  
  total_expected_price = sum([item.get_price() for item in cart_items])
  total_expected_tax = round(total_expected_price * 0.08, 2)
  
  with allure.step("Verifying cart totals match"):
    assert finalize_page.get_sub_total_price() == total_expected_price
    assert finalize_page.get_tax() == total_expected_tax
    assert finalize_page.get_total() == total_expected_price + total_expected_tax

  with allure.step("Verifying finish button is visible"):
    assert finalize_page.finish_button.is_visible()

def test_can_finish_checkout(inventory_items: [dict], checkout_finalize_page: Page):
  """Completes the checkout process successfully."""
  finalize_page = CheckoutFinalizePage(checkout_finalize_page)
  finalize_page.click_finish()
  expect(checkout_finalize_page).to_have_url(re.compile(".*" + CheckoutCompletePage.PATH))
  complete_page = CheckoutCompletePage(checkout_finalize_page)
  complete_page.verify_order_completion()

def test_can_cancel_checkout(inventory_items: [dict], checkout_finalize_page: Page):
  """Ensures that canceling checkout redirects to the inventory page."""
  finalize_page = CheckoutFinalizePage(checkout_finalize_page)
  finalize_page.click_cancel()
  expect(checkout_finalize_page).to_have_url(re.compile(".*" + InventoryPage.PATH))
