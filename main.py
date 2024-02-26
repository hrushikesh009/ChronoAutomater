import json
import os
import time

from configuration import ConfigReader
from helper.helper import load_cookies, save_cookies
from LocalStorage import LocalStorage
from task_automation_handlers import SBITaskUpdater


def initialize_local_storage(sbi_task_updater, data):
    local_storage = LocalStorage(sbi_task_updater)
    for key, value in data.items():
        local_storage.set(key, value)
    return local_storage


def handle_login_and_save_cookies(sbi_task_updater, username, otp):
    print("Currently on the login page.")
    sbi_task_updater.handle_login(username, otp)

    if "home" in sbi_task_updater.current_url:
        local_storage_data = LocalStorage(sbi_task_updater)
        save_cookies(local_storage_data.items(), "local_storage_data.json")
        print("Successfully! Logged In.")
    else:
        print("Login failed. Please check your credentials.")
        exit(1)


def main():
    config_reader = ConfigReader()
    global config
    config = config_reader.read_config("login-credentials.ini")

    try:
        with SBITaskUpdater() as sbi_task_updater:
            sbi_task_updater.landing_page(config["landing_page"])
            cookies_file_exists = os.path.isfile('local_storage_data.json')

            if cookies_file_exists:
                data = json.loads(load_cookies("local_storage_data.json"))
                local_storage = initialize_local_storage(sbi_task_updater, data)
                sbi_task_updater.landing_page(config["landing_page"])

                if "login" in sbi_task_updater.current_url:
                    handle_login_and_save_cookies(sbi_task_updater, config["username"], config["otp"])
                else:
                    print("Skipping! User is already Logged in.")
            else:
                handle_login_and_save_cookies(sbi_task_updater, config["username"], config["otp"])

            time.sleep(5)
            sbi_task_updater.perform_task(config["workplace"], config["tasklist"])

    except Exception as e:
        print("Something Went Wrong! Please check your TimeSheet!")

if __name__ == "__main__":
    main()
