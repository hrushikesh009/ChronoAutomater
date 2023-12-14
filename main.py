import json
import os
import time
from configparser import ConfigParser

from AutomateTaskUpdater import AutomateTaskUpdater
from helper.helper import load_cookies, save_cookies
from LocalStorage import LocalStorage


class ConfigReader:
    @staticmethod
    def read_config(file_path):
        config_parser = ConfigParser()
        config_parser.read(file_path)
        return dict(config_parser['Credentials'])

class AutomatedTaskUpdater:
    def __init__(self, driver:AutomateTaskUpdater):
        self.driver = driver

    def landing_page(self,page_url):
        self.driver.landing_page(page_url)

    def handle_login(self, username, otp):
        print("Currently on the login page.")
        self.driver.login_page.login(username, otp)
        time.sleep(5)

        if "home" in self.driver.current_url:
            local_storage_data = LocalStorage(self.driver)
            save_cookies(local_storage_data.items(), "local_storage_data.json")
            print("Successfully! Logged In.")
        else:
            print("Login failed. Please check your credentials.")
            exit(1)

    def process_task_update(self,workplace,task_list):
        self.driver.workspace_switcher.switch_workspace(workplace)
        self.driver.refresh()

        self.driver.time_sheet_handler.switch_to_timesheet()
        self.driver.refresh()

        self.driver.time_sheet_handler.submit_time_block(task_list)
        time.sleep(5)

def main():
    # import pdb; pdb.set_trace();
    config_reader = ConfigReader()
    global config
    config = config_reader.read_config("login-credentials.ini")

    try:
        with AutomateTaskUpdater() as atu:
            updater = AutomatedTaskUpdater(atu)
            updater.landing_page(config["landing_page"])
            cookies_file_exists = os.path.isfile('local_storage_data.json')

            if cookies_file_exists:
                data = json.loads(load_cookies("local_storage_data.json"))
                local_storage = LocalStorage(atu)

                for key, value in data.items():
                    local_storage.set(key, value)
                
                # Reinitialize the landing page after inserting the authentication token
                # to ensure proper navigation and functionality with the updated session.
                updater.landing_page(config["landing_page"])

                if "login" in atu.current_url:
                    updater.handle_login(config["username"], config["otp"])
                else:
                    print("Skipping! User is already Logged in.")
            else:
                updater.handle_login(config["username"], config["otp"])

            time.sleep(5)
            updater.process_task_update(config["workplace"],config["tasklist"])

    except Exception as e:
        print(e)
        print("Something Went Wrong! Please check your TimeSheet!")

if __name__ == "__main__":
    main()
