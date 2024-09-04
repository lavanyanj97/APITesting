import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import configparser
from cryptography.fernet import Fernet
from webdriver_manager.chrome import ChromeDriverManager

# Load encryption key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Load and decrypt configuration
config = configparser.ConfigParser()
config.read('config.ini')
encrypted_email = config.get('credentials', 'email')
encrypted_password = config.get('credentials', 'password')
email = fernet.decrypt(encrypted_email.encode()).decode()
password = fernet.decrypt(encrypted_password.encode()).decode()

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
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

@pytest.mark.order(1)
def test_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://login.microsoftonline.com/")

    # Check if the user is already logged in
    try:
        profile_icon = wait.until(EC.presence_of_element_located((By.ID, "mectrl_headerPicture")))
        print("User is already logged in. Proceeding to check other applications.")
    except TimeoutException:
        print("User is not logged in. Proceeding with login.")

    email_field = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
    email_field.send_keys(email)

    next_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    next_button.click()

    password_field = wait.until(EC.presence_of_element_located((By.ID, "i0118")))
    password_field.send_keys(password)

    click_element(wait, (By.ID, "idSIButton9"))

    print("Proceeding...")
    time.sleep(30)

    click_element(wait, (By.ID, "idSIButton9"))

    urls = [
        ("https://login.microsoftonline.com/", "//*[contains(text(), 'Welcome to Microsoft 365')]"),
        ("https://teams.microsoft.com/", "//*[contains(text(), 'Calendar')]"),
        ("https://dev.azure.com/SignaTechServicesIndia/", "//*[contains(text(), 'Projects')]")
    ]

    # Check login status for each URL
    all_logged_in = True
    for url, check_element in urls:
        driver.execute_script(f"window.open('{url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        try:
            if "teams.microsoft.com" in url:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, check_element)))
            else:
                wait.until(EC.presence_of_element_located((By.XPATH, check_element)))
            print(f"Successfully logged into {url}")
        except TimeoutException:
            print(f"Failed to log into {url}")
            all_logged_in = False

    assert all_logged_in, "Some URLs failed to log in"
