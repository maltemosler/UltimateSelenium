import time
from random import randint


class UltimateSeleniumError(Exception):
    pass


class UltimateSelenium:
    driver = None

    def __init__(self, driver):
        self.driver = driver

    def get(self, url: str):
        try:
            self.driver.get(url)
        except:
            return False

    def find_element(self, paths: list, require=True):
        for i in range(3):
            for path in paths:
                try:
                    return self.driver.find_element_by_xpath(path)
                # except ProxyError:
                #     raise UltimateSeleniumError("US-restart")
                except Exception as e:
                    if i == 2:
                        print(e)  # todo: notify
                        # d = self.driver.get_screenshot_as_base64
                    time.sleep(randint(2, 3))
        if require:
            raise UltimateSeleniumError("US-restart")
