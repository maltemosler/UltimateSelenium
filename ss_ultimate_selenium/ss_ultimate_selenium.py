import time
from random import randint

from selenium.common.exceptions import NoSuchElementException, WebDriverException
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
        except WebDriverException:
            self.driver.close()
            raise UltimateSeleniumError("US-restart")

    def find_element(self, paths: list, require=True):
        for i in range(3):
            for path in paths:
                try:
                    return self.driver.find_element_by_xpath(path)
                except NoSuchElementException as e:
                    if i == 2 and require:
                        base64_data = self.driver.get_screenshot_as_base64()
                        self.notification_service.post_email(subject="Finding element failed!",
                                                             message=f"Paths: {paths} \n\n"
                                                                     f"require: {require} \n\n"
                                                                     f"{e}",
                                                             images={"error_msg.png": base64_data})
                    time.sleep(randint(2, 3))
                except Exception as e:
                    if i == 2:
                        base64_data = self.driver.get_screenshot_as_base64()
                        self.notification_service.post_email(subject="Unexpected error!",
                                                             message=f"Paths: {paths} \n\n"
                                                                     f"require: {require} \n\n"
                                                                     f"{e}",
                                                             images={"error_msg.png": base64_data})
                        raise UltimateSeleniumError("US-restart")
                    time.sleep(randint(2, 3))
        if require:
            raise UltimateSeleniumError("US-restart")

    def close(self):
        self.driver.close()
