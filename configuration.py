import os
from configparser import ConfigParser

from selenium.webdriver.chrome.options import Options


class ChromeOptionsConfigurator:
    @staticmethod
    def configure(driver_path):
        options = Options()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_argument("--headless=new")
        options.add_experimental_option("prefs", prefs)
        os.environ['PATH'] += driver_path
        return options
    

class ConfigReader:
    @staticmethod
    def read_config(file_path):
        config_parser = ConfigParser()
        config_parser.read(file_path)
        return dict(config_parser['Credentials'])