from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QMessageBox, QSpacerItem, QSizePolicy)
from services.auth_service import check_user
from ui.account_creation_ui import CreateAccountUI

class LoginWindow(QWidget):
    def __init__(self, switch_to_dashboard):
        super().__init__()
        self.setWindowTitle('Project Workflow Manager - Login')
        self.switch_to_dashboard = switch_to_dashboard
        self.setFixedSize(500, 300)

        # Layouts
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        title_label = QLabel("Login")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(12)
        form_layout.setVerticalSpacing(12)

        # Widgets
        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Add widgets to grid layout
        form_layout.addWidget(self.email_label, 0, 0)
        form_layout.addWidget(self.email_input, 0, 1)
        form_layout.addWidget(self.password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.open_register_window)

        # Button layout
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        # Add layouts to main layout
        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )
        main_layout.addWidget(title_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        self.setLayout(main_layout)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter email and password")
            return

        user_id = check_user(email, password)

        if user_id is not None:
            self.switch_to_dashboard(user_id)
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials')

    def open_register_window(self):
        self.register_window = CreateAccountUI(self)
        self.register_window.exec()