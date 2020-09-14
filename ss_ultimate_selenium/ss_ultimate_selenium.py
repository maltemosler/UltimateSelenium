import base64
import time
from io import BytesIO
from random import randint

from ss_notification_service.ss_notification_service import NotificationService


class UltimateSeleniumError(Exception):
    pass


class UltimateSelenium:
    driver = None
    notification_service = None

    def __init__(self, cfg, driver):
        self.driver = driver
        self.notification_service = NotificationService(cfg)

    def get(self, url: str):
        try:
            self.driver.get(url)
        except:
            return False

    def find_element(self, paths: list, require=True):
        for i in range(5):
            for path in paths:
                try:
                    return self.driver.find_element_by_xpath(path)
                # except ProxyError:
                #     raise UltimateSeleniumError("US-restart")
                except Exception as e:
                    if i == 2 and require:
                        base64_data = self.driver.get_screenshot_as_base64()
                        self.notification_service.post_email("Finding element failed!", f"{paths} \n\n require: {require} \n\n {e} \n\n {base64_data}")
                    time.sleep(randint(2, 3))
        if require:
            raise UltimateSeleniumError("US-restart")

    def close(self):
        self.driver.close()
