import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import logging
import time
import configparser
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(filename="selenium_test.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

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

def log_error(step_name, exception):
    """Logs detailed error messages for each step."""
    logging.error(f"Error in step: {step_name}")
    logging.error(f"Exception: {type(exception).__name__} - {str(exception)}")
    logging.error("Traceback:", exc_info=True)

def click_element(wait, locator):
    while True:
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            break
        except StaleElementReferenceException as e:
            logging.warning(f"StaleElementReferenceException encountered in click_element: {str(e)}. Retrying...")
        except TimeoutException as e:
            log_error("click_element", e)
            raise

@pytest.fixture
def driver():
    """Fixture to initialize and quit the Selenium WebDriver."""
    driver = webdriver.Chrome()  # Make sure you have the correct driver installed
    yield driver
    driver.quit()

def test_login(driver):
    wait = WebDriverWait(driver, 15)  # Increased timeout to 15 seconds
    driver.get("https://login.microsoftonline.com/")

    try:
        # Check if the user is already logged in
        profile_icon = wait.until(EC.presence_of_element_located((By.ID, "mectrl_headerPicture")))
        logging.info("User is already logged in. Proceeding to check other applications.")
    except TimeoutException as e:
        logging.warning("User is not logged in. Proceeding with login.")
        log_error("check_logged_in", e)

    try:
        email_field = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
        email_field.send_keys(email)  # Using decrypted email
        logging.info("Email entered successfully.")

        next_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
        next_button.click()
        logging.info("Next button clicked.")
    except TimeoutException as e:
        log_error("email_entry_or_next_click", e)
        raise

    try:
        password_field = wait.until(EC.presence_of_element_located((By.ID, "i0118")))
        password_field.send_keys(password)  # Using decrypted password
        logging.info("Password entered successfully.")

        click_element(wait, (By.ID, "idSIButton9"))
        logging.info("Sign-in button clicked after entering password.")
    except TimeoutException as e:
        log_error("password_entry_or_signin_click", e)
        raise

    # Handle mobile authentication prompt
    logging.info("Waiting for mobile authentication approval...")
    try:
        time.sleep(30)  # Wait for manual approval on mobile device
        click_element(wait, (By.ID, "idSIButton9"))
        logging.info("Sign-in button clicked after mobile authentication.")
    except TimeoutException as e:
        log_error("mobile_authentication_or_final_signin_click", e)
        raise

    # Check login status for each URL
    urls = [
        ("https://login.microsoftonline.com/", "//*[contains(text(), 'Welcome to Microsoft 365')]"),
        ("https://teams.microsoft.com/", "//*[contains(text(), 'Calendar')]"),
        ("https://dev.azure.com/SignaTechServicesIndia/", "//*[contains(text(), 'Projects')]")
    ]

    all_logged_in = True
    for url, check_element in urls:
        try:
            logging.info(f"Checking login for: {url}")
            driver.execute_script(f"window.open('{url}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            wait.until(EC.presence_of_element_located((By.XPATH, check_element)))
            logging.info(f"Successfully logged into {url}")
        except TimeoutException as e:
            log_error(f"login_status_check_{url}", e)
            all_logged_in = False

    assert all_logged_in, "Some URLs failed to log in"
