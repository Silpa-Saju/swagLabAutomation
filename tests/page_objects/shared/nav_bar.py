import allure
class NavBar:
  def __init__(self, page):
    self.page = page

    self.shopping_cart_link = page.locator("[data-test='shopping-cart-link']")
    self.shopping_cart_badge = page.locator("[data-test='shopping-cart-badge']")

    self.burger_menu = page.locator('#react-burger-menu-btn')
  
  @allure.step("Clicking burger menu")
  def click_burger_menu(self):
    self.burger_menu.click()
  
  @allure.step("Clicking shopping cart link")
  def click_shopping_cart_link(self):
    self.shopping_cart_link.click()

  @allure.step("Getting item count")
  def get_item_count(self):
    if not self.shopping_cart_badge.is_visible():
      return 0

    return int(self.shopping_cart_badge.text_content())