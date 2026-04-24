"""
dashboard_window.py

This module defines the main dashboard user interface for the
Project Workflow Manager application using PyQt6.

Responsibilities:
    - Display the main dashboard after user login
    - Render a weekly calendar view for projects and phases
    - Allow navigation between calendar weeks
    - Display projects and phases on their respective due dates
    - Open project creation and project detail windows
    - Refresh the dashboard when project data changes

"""

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QHeaderView,
    QFrame,
)
from PyQt6.QtCore import Qt, QDate
from ui.project_create_window import ProjectCreationWindow
from ui.project_details_window import ProjectDetailsWindow
from ui.phase_details_window import PhaseDetailsWindow
from services.project_retriever import get_projects_for_user,get_project_by_id, get_project_by_phase_id
from services.phase_retriever import get_phases_for_project
from services.assigned_phase_retriever import get_assigned_phases_for_user
from services.phase_color_service import get_due_date_colors



"""
class: DayCellWidget

Represents a single day cell in the weekly dashboard calendar.

This class handles the visual structure of each day in the calendar,
including the day header and the content area where project and phase
nodes are displayed.
"""
class DayCellWidget(QWidget):

    """
    __init__

    constructor

    PRE:
        - A valid QDate object is provided for the day cell
        - PyQt6 environment is properly installed and configured

    POST:
        - A styled day cell widget is created
        - The day header displays the weekday and date
        - A content area is initialized for calendar nodes
    """
    def __init__(self, day_date, parent=None):
        super().__init__(parent)

        self.day_date = day_date

        self.setObjectName("dayCell")
        self.setStyleSheet("""
            QWidget#dayCell {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
            }
        """)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header area
        self.header_frame = QFrame()
        self.header_frame.setStyleSheet("""
            background-color: #3a3a3a;
            border-bottom: 1px solid #666666;
        """)

        self.header_layout = QVBoxLayout()
        self.header_layout.setContentsMargins(6, 6, 6, 6)
        self.header_layout.setSpacing(2)

        day_name = QLabel(day_date.toString("ddd"))
        day_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        day_name.setStyleSheet("""
            color: white;
            font-size: 13px;
            font-weight: bold;
            border: none;
        """)

        day_number = QLabel(day_date.toString("MMM d"))
        day_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        day_number.setStyleSheet("""
            color: #dddddd;
            font-size: 11px;
            border: none;
        """)

        self.header_layout.addWidget(day_name)
        self.header_layout.addWidget(day_number)
        self.header_frame.setLayout(self.header_layout)

        # Content area
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("border: none; background-color: #2b2b2b;")

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(6, 6, 6, 6)
        self.content_layout.setSpacing(12)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.content_widget.setLayout(self.content_layout)

        self.main_layout.addWidget(self.header_frame, 0)
        self.main_layout.addWidget(self.content_widget, 1)

        self.setLayout(self.main_layout)

    """
    add_node

    PRE:
        - A valid PyQt widget is provided
        - The day cell content layout has been initialized

    POST:
        - The provided widget is added to the content area of the day cell

    Returns:
        - None
    """
    def add_node(self, widget):
        self.content_layout.addWidget(widget)


"""
class: DashboardWindow

Represents the main dashboard window for the Project Workflow Manager.

This class handles the weekly calendar display, project and phase
placement, week navigation, and interaction with project creation
and project details windows.
"""
class DashboardWindow(QWidget):

    """
    __init__

    constructor

    PRE:
        - A valid user ID is provided
        - PyQt6 environment is properly installed and configured

    POST:
        - The dashboard window is created and displayed
        - The weekly calendar interface is initialized
        - Event handlers are connected to their respective UI controls
        - Project and phase data for the current week are loaded
    """
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.setWindowTitle('Project Workflow Manager - Dashboard')

        self.resize(1200, 700)
        self.setMinimumSize(1000, 600)

        self.project_window = None
        self.details_window = None

        # Track currently displayed week (always Monday)
        today = QDate.currentDate()
        self.current_week_start = today.addDays(-(today.dayOfWeek() - 1))

        self.day_cells = {}

        # Layouts
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        week_nav_layout = QHBoxLayout()

        # Header
        self.title_label = QLabel('Project Workflow Manager')
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.logout_button = QPushButton('Logout')
        legend_container = QWidget()
        legend_layout = QHBoxLayout(legend_container)
        legend_layout.setContentsMargins(0, 0, 0, 0)
        legend_layout.setSpacing(15)

        for color, text in [
            ("#c94c4c", "< 1 week"),
            ("#e89f28", "1 week - 1 month"),
            ("#5a9a5a", "> 1 month"),
        ]:
            item_layout = QHBoxLayout()
            item_layout.setSpacing(5)

            color_label = QLabel()
            color_label.setFixedSize(12, 12)
            color_label.setStyleSheet(f"background-color: {color}; border-radius: 6px;")

            text_label = QLabel(text)
            text_label.setStyleSheet("font-size: 11px; color: #cccccc;")

            item_layout.addWidget(color_label)
            item_layout.addWidget(text_label)
            legend_layout.addLayout(item_layout)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(legend_container)
        header_layout.addSpacing(20)
        header_layout.addWidget(self.logout_button)

        # Buttons
        self.create_project_button = QPushButton('Create Project')
        self.view_project_list_button = QPushButton('View Project List')

        self.create_project_button.clicked.connect(self.open_create_project_window)
        # self.view_project_list_button.clicked.connect(self.open_project_list_window)

        button_layout.addWidget(self.create_project_button)
        button_layout.addWidget(self.view_project_list_button)
        button_layout.addStretch()

        # Week navigation
        self.prev_week_button = QPushButton("<")
        self.next_week_button = QPushButton(">")
        self.week_label = QLabel()
        self.week_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.prev_week_button.clicked.connect(self.show_previous_week)
        self.next_week_button.clicked.connect(self.show_next_week)

        week_nav_layout.addWidget(self.prev_week_button)
        week_nav_layout.addWidget(self.week_label)
        week_nav_layout.addWidget(self.next_week_button)
        week_nav_layout.addStretch()

        # Weekly calendar table
        self.calendar_table = QTableWidget()
        self.calendar_table.setShowGrid(False)
        self.calendar_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.calendar_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #1e1e1e;
                border: none;
            }
        """)
        self.calendar_table.setRowCount(1)
        self.calendar_table.setRowHeight(0, 500)
        self.calendar_table.setMinimumHeight(600)
        self.calendar_table.setColumnCount(7)
        self.calendar_table.setHorizontalHeaderLabels(
            ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        )

        self.calendar_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.calendar_table.verticalHeader().setVisible(False)
        self.calendar_table.horizontalHeader().setVisible(False)
        self.calendar_table.setShowGrid(True)
        self.calendar_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.calendar_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(week_nav_layout)
        main_layout.addWidget(self.calendar_table)

        self.setLayout(main_layout)

        self.load_projects()

    """
    open_create_project_window

    PRE:
        - A valid user ID is stored in the dashboard instance
        - The project creation window class is available

    POST:
        - The project creation window is opened
        - The dashboard is refreshed when the project window is closed

    Returns:
        - None
    """
    def open_create_project_window(self):
        self.project_window = ProjectCreationWindow(self.user_id)
        self.project_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.project_window.destroyed.connect(self.load_projects)
        self.project_window.show()
        self.project_window.raise_()
        self.project_window.activateWindow()

    """
    show_previous_week

    PRE:
        - The current displayed week has been initialized

    POST:
        - The calendar is shifted backward by one week
        - The dashboard is refreshed to reflect the new week

    Returns:
        - None
    """
    def show_previous_week(self):
        self.current_week_start = self.current_week_start.addDays(-7)
        self.load_projects()

    """
    show_next_week

    PRE:
        - The current displayed week has been initialized

    POST:
        - The calendar is shifted forward by one week
        - The dashboard is refreshed to reflect the new week

    Returns:
        - None
    """
    def show_next_week(self):
        self.current_week_start = self.current_week_start.addDays(7)
        self.load_projects()

    """
    build_week_calendar

    PRE:
        - The current displayed week has been initialized
        - The weekly calendar table exists

    POST:
        - Existing calendar contents are cleared
        - A new set of day cells is created for the current week
        - The week range label is updated
        - Day cells are stored for later project/phase placement

    Returns:
        - None
    """
    def build_week_calendar(self):
        self.calendar_table.clearContents()
        self.day_cells.clear()

        week_end = self.current_week_start.addDays(6)
        self.week_label.setText(
            f"{self.current_week_start.toString('MMM d, yyyy')} - "
            f"{week_end.toString('MMM d, yyyy')}"
        )

        for col in range(7):
            day_date = self.current_week_start.addDays(col)
            day_cell = DayCellWidget(day_date)

            self.calendar_table.setCellWidget(0, col, day_cell)
            self.day_cells[day_date.toString("yyyy-MM-dd")] = day_cell

    """
    add_project_button

    PRE:
        - A valid project object is provided
        - day_key is a valid date string in yyyy-MM-dd format
        - The corresponding day cell may exist in the current week

    POST:
        - A styled project button is created
        - The project object is stored on the button
        - Clicking the button opens the project details window
        - If the day exists in the current week, the button is added to that day

    Returns:
        - None
    """
    def add_project_button(self, project, day_key):
        button = QPushButton(project.title)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setMinimumHeight(32)
        button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                text-align: left;
                padding: 6px;
                background-color: #4a6fa5;
                color: white;
                border: 1px solid #6f8fc0;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5b82bb;
            }
            QPushButton:pressed {
                background-color: #3e5f8d;
            }
        """)

        button.setProperty("stored_project", project)
        button.clicked.connect(self.handle_project_click)

        if day_key in self.day_cells:
            self.day_cells[day_key].add_node(button)

    """
    handle_project_click

    PRE:
        - The sender is a project button with a stored project object
        - The project details window class is available

    POST:
        - If a stored project exists, the project details window is opened
        - The dashboard can later be refreshed through the callback

    Returns:
        - None
    """
    def handle_project_click(self):
        button = self.sender()
        project = button.property("stored_project")

        if project is None:
            return

        self.details_window = ProjectDetailsWindow(
            project.project_id,
            refresh_callback=self.load_projects
        )
        self.details_window.show()

    def handle_phase_click(self):
        button = self.sender()
        phase = button.property("stored_phase")

        if phase is None:
            return

        phase_id = phase[0]
        self.phase_details_window = PhaseDetailsWindow(phase_id)
        self.phase_details_window.show()

    """
    load_projects

    PRE:
        - The dashboard has a valid user ID
        - Project and phase retrieval services are available
        - The weekly calendar can be built successfully

    POST:
        - The weekly calendar is rebuilt
        - Projects for the current user are retrieved
        - Projects due in the current week are displayed on their due date
        - Phases due in the current week are displayed on their due date

    Returns:
        - None
    """
    def load_projects(self):
        self.build_week_calendar()

        project_list = get_projects_for_user(self.user_id)

        for project in project_list:
            project_day = project.date.strip()

            # Put the project on its due date if it's in the current week
            if project_day in self.day_cells:
                self.add_project_button(project, project_day)

            # Put phases on their due dates if they're in the current week
            phase_list = get_phases_for_project(project.project_id)
            for phase in phase_list:
                phase_day = phase[3].strip()  # phaseDueDate
                if phase_day in self.day_cells:
                    self.add_phase_button(phase, phase_day)

        assigned_phases = get_assigned_phases_for_user(self.user_id)

        for phase in assigned_phases:
            phase_day = phase[3].strip()
            if phase_day in self.day_cells:
                self.add_phase_button(phase, phase_day)

    """
    add_phase_button

    PRE:
        - A valid phase tuple is provided
        - day_key is a valid date string in yyyy-MM-dd format
        - The corresponding day cell may exist in the current week

    POST:
        - A styled phase button is created
        - If the day exists in the current week, the button is added to that day

    Returns:
        - None
    """
    def add_phase_button(self, phase, day_key):
        project = get_project_by_phase_id(phase[0])
        project_title = project.title if project else "Unknown Project"

        button = QPushButton(f"{phase[2]}\nProject: {project_title}")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setMinimumHeight(42)

        due_date_str = phase[3]
        colors = get_due_date_colors(due_date_str)

        button.setStyleSheet(f"""
            QPushButton {{
                font-size: 11px;
                text-align: left;
                padding: 5px;
                background-color: {colors["background"]};
                color: white;
                border: 1px solid {colors["border"]};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {colors["hover"]};
            }}
            QPushButton:pressed {{
                background-color: {colors["pressed"]};
            }}
        """)

        button.setProperty("stored_phase", phase)
        button.clicked.connect(self.handle_phase_click)

        if day_key in self.day_cells:
            self.day_cells[day_key].add_node(button)