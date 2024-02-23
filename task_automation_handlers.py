import time

from task_automation import (LoginPage, TaskUpdater, TimeSheetHandler,
                             WorkspaceSwitcher)


class SBITaskUpdater(TaskUpdater):
    def handle_login(self, username, otp):
        self.login_page = LoginPage(self)
        self.login_page.login(username, otp)
        time.sleep(5)

    def handle_workspace(self, workplace):
        self.workspace_switcher = WorkspaceSwitcher(self)
        self.workspace_switcher.switch_workspace(workplace)
        self.refresh()

    def handle_time_sheet(self, task_list):
        self.time_sheet_handler = TimeSheetHandler(self)
        self.time_sheet_handler.switch_to_timesheet()
        self.refresh()

        self.time_sheet_handler.submit_time_block(task_list)
        time.sleep(5)

    def perform_task(self, workplace, task_list):
        self.handle_workspace(workplace)
        self.handle_time_sheet(task_list)

    def __exit__(self, exc_type, exc, traceback):
        self.quit()


