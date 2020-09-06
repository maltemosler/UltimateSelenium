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
            return False

    def find_element(self, paths: list):
        for i in range(3):
            for path in paths:
                try:
                    return self.driver.find_element_by_xpath(path)
                # except ProxyError:
                #     return
                except Exception as e:
                    # todo: notify
                    time.sleep(randint(2, 3))
