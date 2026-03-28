"""
account_creation_ui.py

This module defines the user interface for account creation using PyQt6.

Responsibilities:
    - Display dialog for user account creation
    - Collect user input (email and password)
    - Perform basic input validation
    - Communicate with account creation service
    - Provide user feedback (error/success confirmations)

"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QMessageBox
)
from services.account_creator import create_account

"""
class: CreateAccountUI

Represents a dialog window for creating a new user account.

This class handles UI layout, user input collection, and
interaction with the backend account creation service.
"""
class CreateAccountUI(QDialog):

    """
    __init__

    constructor

    PRE:
        - PyQt6 environment is properly installed and configured

    POST:
        - A dialog window is created with input fields for email and password
        - UI elements are initialized and displayed
        - Event handlers are connected to their respective UI controls
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Account")
        self.setFixedSize(350, 220)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        #Single-line field for email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")

        #Single-line field for password, dots for security
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        #Single-line field for confirming password, dots as above
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)

        self.message_label = QLabel("")

        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Create")
        self.cancel_button = QPushButton("Cancel")

        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.message_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        #Event handlers
        self.create_button.clicked.connect(self.handle_create_account)
        self.cancel_button.clicked.connect(self.reject)

    """
    handle_create_account

    PRE:
        - The user has interacted with the dialog and provided values
        - UI input fields are accessible

    POST:
        - If input validation fails, an error message is displayed and
          the dialog remains open
        - If account creation fails, an error message is displayed and
          the dialog remains open
        - If account creation succeeds, a confirmation message is shown
          and the dialog is closed.

    Returns:
        - None
    """
    def handle_create_account(self):
        self.message_label.setText("")
        
        #Input from fields
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        #Error messages
        if not email or not password or not confirm_password:
            self.message_label.setText("All fields are required.")
            return
        
        if password != confirm_password:
            self.message_label.setText("Passwords do not match.")
            return
        
        #Tuple for success determination
        success, message = create_account(email, password)

        if not success:
            self.message_label.setText(message)
            return
        
        QMessageBox.information(self, "Success", "Account created successfully.")
        
        self.accept()
