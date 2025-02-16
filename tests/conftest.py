import pytest
import allure
import datetime
import os
import re

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, Playwright, expect

from tests.page_objects.login_page import LoginPage
from urllib.parse import urljoin

from tests.page_objects.inventory_page import InventoryPage


@pytest.fixture(scope="session", autouse=True)
def setup_session_dirs():
  os.makedirs("screenshots", exist_ok=True)

  yield

  if os.path.exists(".auth/storagestate.json"):
    os.remove(".auth/storagestate.json")

@pytest.fixture(scope='session')
def env():
  load_dotenv()
  return {
    "headless": os.getenv("HEADLESS").lower() == "true",
    "base_url": os.getenv("BASE_URL"),
    "username": os.getenv("USERNAME"),
    "password": os.getenv("PASSWORD")
  }

@pytest.fixture(scope="session")
def playwright():
  with sync_playwright() as p:
    yield p

@pytest.fixture(scope='session')
def browser(playwright: Playwright, env):
  with playwright.chromium.launch(headless=env['headless']) as browser:
    yield browser

@pytest.fixture(scope='function')
def context(browser: Browser):
  with browser.new_context() as context:
    yield context

@pytest.fixture(scope='function')
def context_with_auth(browser: Browser, env):
  # if we already have a session, don't create a new one
  # load the existing session from disk
  if os.path.exists('.auth/storagestate.json'):
    with browser.new_context(storage_state='.auth/storagestate.json') as context:
      yield context
    return

  # if we don't have a session, create a new one
  # and save it to disk
  with browser.new_context() as context:
    with context.new_page() as page:
      page.goto(env["base_url"])
      login = LoginPage(page)
      login.perform_login(env["username"], env["password"])
      assert login.has_logged_in()

    context.storage_state(path='.auth/storagestate.json')
    yield context

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
  outcome = yield
  report = outcome.get_result()

  if report.when != "call" or report.outcome != "failed":
    return

  for arg in item.funcargs:
    if not isinstance(item.funcargs[arg], Page):
      continue

    page = item.funcargs[arg]
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    path = f"screenshots/{item.name}_{timestamp}.png"
    page.screenshot(path=path)
    allure.attach.file(path, "image/png")

@pytest.fixture(scope='function')
def inventory_page(context_with_auth: BrowserContext, env):
  """Navigates to the inventory page and ensures it is ready for testing."""
  with context_with_auth.new_page() as page, allure.step("Navigate to inventory page"):
    page.goto(urljoin(env["base_url"], "/inventory.html"))
    page.wait_for_load_state('domcontentloaded')
    expect(page).to_have_url(re.compile(".*" + InventoryPage.PATH))
    yield page