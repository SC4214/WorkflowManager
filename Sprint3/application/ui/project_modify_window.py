from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QDateEdit, QFormLayout, QMessageBox
from PyQt6.QtCore import QDate
from services.project_retriever import get_project_by_id
from services.project_modifier import update_project_details

class ProjectModifyWindow(QWidget):
    def __init__(self, project_id, refresh_callback=None, parent=None):
        super().__init__(parent)
        self.project_id = project_id
        self.refresh_callback = refresh_callback

        self.setWindowTitle("Modify Project")
        self.setMinimumWidth(400)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
            }
            QTextEdit, QDateEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                color: #f0f0f0;
            }
            QDateEdit::drop-down {
                border: 0px;
            }
            QPushButton {
                background-color: #4a6fa5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5b82bb;
            }
            QPushButton:pressed {
                background-color: #3e5f8d;
            }
        """)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.description_edit = QTextEdit()

        form_layout.addRow("Due Date:", self.due_date_edit)
        form_layout.addRow("Description:", self.description_edit)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)

        self.load_project_data()

    def load_project_data(self):
        project = get_project_by_id(self.project_id)
        if project:
            try:
                due_date = QDate.fromString(project.date.strip(), "yyyy-MM-dd")
                self.due_date_edit.setDate(due_date)
            except Exception as e:
                print(f"Error parsing date: {e}")
                self.due_date_edit.setDate(QDate.currentDate())

            self.description_edit.setText(project.description)

    def save_changes(self):
        due_date = self.due_date_edit.date().toString("yyyy-MM-dd")
        description = self.description_edit.toPlainText()

        if update_project_details(self.project_id, due_date, description):
            QMessageBox.information(self, "Success", "Project updated successfully.")
            if self.refresh_callback:
                self.refresh_callback()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to update project.")
