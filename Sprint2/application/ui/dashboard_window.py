from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
)
from PyQt6.QtCore import Qt
from ui.project_create_window import ProjectCreationWindow
from ui.project_details_window import ProjectDetailsWindow
from services.project_retriever import get_projects_for_user
from services.phase_retriever import get_phases_for_project

class DashboardWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.setWindowTitle('Project Workflow Manager - Dashboard')

        self.resize(1000, 700)
        self.setMinimumSize(900, 600)

        self.project_window = None
        self.details_window = None  # Keep a reference to the details window

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
        # self.view_project_list_button.clicked.connect(self.open_project_list_window)

        button_layout.addWidget(self.create_project_button)
        button_layout.addWidget(self.view_project_list_button)
        button_layout.addStretch()

        # Calendar Table
        self.calendar_label = QLabel('Calendar')
        self.calendar_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.calendar_table = QTableWidget()
        self.calendar_table.setColumnCount(7)
        self.calendar_table.setRowCount(6)
        self.calendar_table.setHorizontalHeaderLabels(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        )
        self.calendar_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.calendar_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.calendar_table.verticalHeader().setVisible(False)

        # Add layouts to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.calendar_label)
        main_layout.addWidget(self.calendar_table)

        self.setLayout(main_layout)

        self.load_projects()

    def open_create_project_window(self):
        self.project_window = ProjectCreationWindow(self.user_id)
        self.project_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.project_window.destroyed.connect(self.load_projects)
        self.project_window.show()
        self.project_window.raise_()
        self.project_window.activateWindow()

    def add_project_button(self, project, row, col):
        """
        Creates a clickable calendar button for a project.
        """
        button = QPushButton(project.title)
        button.setStyleSheet("font-size: 12px; text-align: left; padding: 4px;")

        # Store the object inside the button
        button.setProperty("stored_project", project)

        # Connect click -> open details
        button.clicked.connect(self.handle_project_click)

        # Put the button directly into the cell
        self.calendar_table.setCellWidget(row, col, button)

    def handle_project_click(self):
        """
        Opens the project details window for the clicked project.
        """
        button = self.sender()
        project = button.property("stored_project")

        if project is None:
            return

        self.details_window = ProjectDetailsWindow(project.project_id, refresh_callback=self.load_projects)
        self.details_window.show()

    def load_projects(self):
        # Clear existing cell widgets
        for row in range(self.calendar_table.rowCount()):
            for col in range(self.calendar_table.columnCount()):
                self.calendar_table.removeCellWidget(row, col)

        project_list = get_projects_for_user(self.user_id)

        col = 0

        for project in project_list:
            if col >= self.calendar_table.columnCount():
                break

            # Put the project in the top row of its column
            self.add_project_button(project, 0, col)

            # Get and place phases underneath
            phase_list = get_phases_for_project(project.project_id)

            phase_row = 1
            for phase in phase_list:
                if phase_row >= self.calendar_table.rowCount():
                    break

                self.add_phase_button(phase, phase_row, col)
                phase_row += 1

            col += 1

    def add_phase_button(self, phase, row, col):
        """
        Creates a button for a phase underneath its project.
        """
        button = QPushButton(phase[2])  # phaseTitle
        button.setStyleSheet("font-size: 11px; text-align: left; padding: 4px;")

        self.calendar_table.setCellWidget(row, col, button)