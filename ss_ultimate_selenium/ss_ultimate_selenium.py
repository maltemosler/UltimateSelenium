import time
from random import randint


class UltimateSelenium:
    driver = None

    def __init__(self, driver):
        self.driver = driver

    def get(self, url: str):
        try:
            self.driver.get(url)
        except:
            return

    def p(self):

        time.sleep(randint(1, 3))
        element = self.driver.find_element_by_xpath('//*[@id="username"]')
        return element