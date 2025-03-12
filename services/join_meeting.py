import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from logger import Log

log = Log()


def join_meeting(meeting_url: str):
    driver = build_selenium_driver()

    log.info('Joining meeting initial page...')
    driver.get(meeting_url)

    log.info('Waiting for page to load...')
    time.sleep(15)

    try:
        log.info('Joining meeting...')
        join_button = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Participar agora')]]")

        join_button.click()
    except NoSuchElementException:
        log.error('Join button not found')

    return driver


def build_selenium_driver():
    log.info('Building Selenium driver')

    options = webdriver.ChromeOptions()

    # options.add_argument("--use-fake-ui-for-media-stream")
    options.add_argument("--use-fake-device-for-media-stream")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_argument("user-data-dir=/Users/gabriel/Library/Application Support/Google/Chrome/Default")
    options.add_argument("--profile-directory=Default")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver
