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
from webdriver_manager.chrome import ChromeDriverManager

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
email = config.get('credentials', 'email')
password = config.get('credentials', 'password')


@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()


def click_element(driver, wait, locator):
    while True:
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            break
        except StaleElementReferenceException:
            print("StaleElementReferenceException encountered. Retrying...")
            element = driver.find_element(*locator)


@pytest.mark.order(1)
def test_login(driver):
    wait = WebDriverWait(driver, 30)  # Increased timeout
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

    click_element(driver, wait, (By.ID, "idSIButton9"))

    print("Proceeding...")
    time.sleep(30)

    click_element(driver, wait, (By.ID, "idSIButton9"))

    # Open the URL in a new tab
    driver.execute_script("window.open('https://dev.azure.com/SignaTechServicesIndia/', '_blank');")

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    # Wait for the elements and perform the clicks
    click_element(driver, wait, (By.ID, 'mectrl_headerPicture'))

    # Debugging: Print page source
    print(driver.page_source)

    # Attempt to click sign out
    try:
        click_element(driver, wait, (By.ID, 'mectrl_body_signOut'))
    except TimeoutException:
        print("TimeoutException: Unable to click sign out button.")
        driver.save_screenshot('screenshot.png')

    time.sleep(15)

    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()

    urls = [
        ("https://teams.microsoft.com/", "//*[contains(text(), 'Sign in')]"),
        ("https://dev.azure.com/SignaTechServicesIndia/", "//*[contains(text(), 'Sign in')]"),
        ("https://sharepoint.com/sites/Communication", "//*[contains(text(), 'Sign in')]")
    ]

    all_logged_out = True
    for url, check_element in urls:
        driver.execute_script(f"window.open('{url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, check_element)))
            print(f"Successfully logged out from {url}")
        except TimeoutException:
            print(f"Failed to log out from {url}")
            all_logged_out = False

    assert all_logged_out, "Not all URLs were successfully logged out"
