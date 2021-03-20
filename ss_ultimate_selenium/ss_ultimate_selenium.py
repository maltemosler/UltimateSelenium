import datetime
import os
import pickle
import time

from random import randint

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from ss_notification_service.ss_notification_service import NotificationService


class UltimateSeleniumError(Exception):
    pass


def get_driver(chrome_options):
    try:
        return webdriver.Chrome(options=chrome_options)
    except:
        pass

    cfg_paths = [
        "/home/mmosler/",
        "/home/scripts/",
        #f"../{os.path.dirname(os.path.abspath(__file__))}",
        #f"{os.path.dirname(os.path.abspath(__file__))}",
    ]

    # go through every parent directory and search for path
    whole_path = os.path.abspath(os.getcwd()).replace("\\", "/")
    splitted_path = whole_path.split("/")
    tmp = ""
    for path in splitted_path:
        tmp += f"{path}/"
        cfg_paths.append(tmp)

    for path in cfg_paths:
        print(path)
        try:
            return webdriver.Chrome(f"{path}chromedriver", options=chrome_options)
        except:
            try:
                return webdriver.Chrome(f"{path}chromedriver.exe", options=chrome_options)
            except:
                continue

    raise(UltimateSeleniumError("NO DRIVER FOUND"))


class UltimateSelenium:
    driver = None
    notification_service = None

    def __init__(self, chrome_options=None):
        if not chrome_options:
            chrome_options = webdriver.ChromeOptions()
        self.driver = get_driver(chrome_options)

        self.notification_service = NotificationService()

    def get(self, url: str):
        try:
            self.driver.get(url)
        except:
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

    def save_cookies(self, path: str, file: str):
        pickle.dump(self.driver.get_cookies(), open(f"{path}/{file}-{datetime.datetime.now().strftime('%m%d%Y%H%M%S')}.pkl", "wb"))

    def load_cookies(self, path: str, days_to_store: int):
        load_store = datetime.datetime.now() - datetime.timedelta(days=days_to_store)

        for path, directories, files in os.walk(f"{os.getcwd()}/{path}"):
            for file in files:
                if "-" in file and ".pkl" in file:
                    if int(load_store.strftime("%m%d%Y%H%M%S")) < int(file.replace(".pkl", "").split("-")[1]):
                        for cookie in pickle.load(open(f"{path}/{file}", "rb")):
                            self.driver.add_cookie(cookie)
                        return True
        return False

    def execute_script(self, script: str):
        self.driver.execute_script(script)  # "window.history.go(-1)"

    def close(self):
        self.driver.close()
