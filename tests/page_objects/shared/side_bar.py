import allure

from playwright.sync_api import Page

class SideBar:
  def __init__(self, page: Page):
    self.page = page
    self._logout_link = page.locator("#logout_sidebar_link")
    self._inventory_link = page.locator("#inventory_sidebar_link")
    self._about_link = page.locator("#about_sidebar_link")
  
  @allure.step("Clicking on the logout button")
  def logout(self):
    self._logout_link.click()