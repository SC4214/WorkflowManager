import sys
from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.dashboard_window import DashboardWindow

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow(self.show_dashboard)
        self.dashboard_window = DashboardWindow()

    def run(self):
        self.login_window.show()
        sys.exit(self.app.exec())

    def show_dashboard(self):
        self.login_window.close()
        self.dashboard_window.show()

if __name__ == '__main__':
    main_app = MainApp()
    main_app.run()
