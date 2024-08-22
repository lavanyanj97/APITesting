import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
email = config.get('credentials', 'email')
password = config.get('credentials', 'password')

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()

def click_element(wait, locator):
    while True:
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            break
        except StaleElementReferenceException:
            print("StaleElementReferenceException encountered. Retrying...")

def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://login.microsoftonline.com/")

    email_field = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
    email_field.send_keys(email)

    next_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    next_button.click()

    password_field = wait.until(EC.presence_of_element_located((By.ID, "i0118")))
    password_field.send_keys(password)

    click_element(wait, (By.ID, "idSIButton9"))
