from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QGridLayout
from PyQt6.QtCore import Qt
from services.phase_details_retriever import get_phase_details

class PhaseDetailsWindow(QWidget):
    def __init__(self, phase_id, parent=None):
        super().__init__(parent)
        self.phase_id = phase_id
        self.setWindowTitle("Phase Details")
        self.resize(450, 350)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #aaaaaa;
            }
            QLabel#valueLabel {
                color: white;
                font-weight: bold;
                font-size: 15px;
            }
            QTextEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                color: #f0f0f0;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        details_layout = QGridLayout()
        details_layout.setSpacing(15)

        self.project_title_value = QLabel("[LOADING...]")
        self.project_title_value.setObjectName("valueLabel")
        self.phase_title_value = QLabel("[LOADING...]")
        self.phase_title_value.setObjectName("valueLabel")
        self.due_date_value = QLabel("[LOADING...]")
        self.due_date_value.setObjectName("valueLabel")

        details_layout.addWidget(QLabel("Project Title:"), 0, 0)
        details_layout.addWidget(self.project_title_value, 0, 1)
        details_layout.addWidget(QLabel("Phase Title:"), 1, 0)
        details_layout.addWidget(self.phase_title_value, 1, 1)
        details_layout.addWidget(QLabel("Due Date:"), 2, 0)
        details_layout.addWidget(self.due_date_value, 2, 1)

        details_layout.setColumnStretch(1, 1)

        self.description_label = QLabel("Description:")
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)

        main_layout.addLayout(details_layout)
        main_layout.addWidget(self.description_label)
        main_layout.addWidget(self.description_text)

        self.load_phase_details()

    def load_phase_details(self):
        details = get_phase_details(self.phase_id)
        if details:
            self.project_title_value.setText(details['project_title'])
            self.phase_title_value.setText(details['phase_title'])
            self.due_date_value.setText(details['due_date'])
            self.description_text.setText(details['description'])
        else:
            self.project_title_value.setText("Phase details not found.")
            self.phase_title_value.setText("N/A")
            self.due_date_value.setText("N/A")
