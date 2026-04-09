from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QHeaderView)
from ui.project_create_window import ProjectCreationWindow

class DashboardWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.setWindowTitle('Project Workflow Manager - Dashboard')

        self.resize(1000, 700)
        self.setMinimumSize(900, 600)

        self.project_window = None

        # Layouts
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Header
        self.title_label = QLabel('Project Workflow Manager')
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.logout_button = QPushButton('Logout')
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.logout_button)

        # Buttons
        self.create_project_button = QPushButton('Create Project')
        self.view_project_list_button = QPushButton('View Project List')

        self.create_project_button.clicked.connect(self.open_create_project_window)

        button_layout.addWidget(self.create_project_button)
        button_layout.addWidget(self.view_project_list_button)
        button_layout.addStretch()

        # Calendar Table
        self.calendar_label = QLabel('Calendar')
        self.calendar_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.calendar_table = QTableWidget()
        self.calendar_table.setColumnCount(7)
        self.calendar_table.setRowCount(6)
        self.calendar_table.setHorizontalHeaderLabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        self.calendar_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.calendar_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.calendar_table.verticalHeader().setVisible(False)

        # Add layouts to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.calendar_label)
        main_layout.addWidget(self.calendar_table)

        self.setLayout(main_layout)

    def open_create_project_window(self):
        self.project_window = ProjectCreationWindow()
        self.project_window.show()
        self.project_window.raise_()
        self.project_window.activateWindow()