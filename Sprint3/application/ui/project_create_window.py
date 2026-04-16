from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QTextEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox
)
from PyQt6.QtCore import QDate
import sys
from services.project_creator import create_project


class ProjectCreationWindow(QWidget):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)

        self.user_id = user_id

        self.setWindowTitle('Project Workflow Manager - Create Project')
        self.resize(500, 350)

        # --- Create widgets ---
        self.title_input = QLineEdit()

        # Date stored as text, so we use a simple QLineEdit
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")

        self.description_input = QTextEdit()
        self.message_label = QLabel("")

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)

        # --- Layout ---
        form_layout = QFormLayout()
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("Description:", self.description_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.submit_button)

        self.setLayout(main_layout)

    def on_submit(self):
        title_text = self.title_input.text()
        date_text = self.date_input.text()
        description_text = self.description_input.toPlainText()

        success, message = create_project(
            title_text,
            date_text,
            self.user_id,
            description_text,
            )

        if not success:
            self.message_label.setText(message)
            return
        
        QMessageBox.information(self, "Success", "Project created successfully.")
        
        self.close()

