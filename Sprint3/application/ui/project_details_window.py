
import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from ui.phase_create_window import PhaseCreationWindow
from ui.assign_workers_window import AssignWorkerWindow
from PyQt6.QtCore import Qt
from ui.project_modify_window import ProjectModifyWindow

class ProjectDetailsWindow(QWidget):
    """
    A window to display the details of a project.

    This window shows the project title, due date, project manager, and a list of project phases.
    It also provides buttons to archive or modify the project.

    Owen: To integrate this window, you'll need to instantiate it and call the show() method.
    For example:
    
    self.details_window = ProjectDetailsWindow(project_id)
    self.details_window.show()
    """
    def __init__(self, project_id, refresh_callback=None, parent=None):
        """
        Initializes the ProjectDetailsWindow.

        Args:
            project_id (int): The ID of the project to display.
        """
        super().__init__(parent)
        self.project_id = project_id
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Project Details")
        self.resize(400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.project_title_label = QLabel("Project Title: [LOADING...]")
        self.due_date_label = QLabel("Due Date: [LOADING...]")
        self.project_manager_label = QLabel("Project Manager: [LOADING...]")
        self.description_label = QLabel("Project Description:")
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        
        self.phases_label = QLabel("Project Steps:")
        self.phases_text = QTextEdit()
        self.phases_text.setReadOnly(True)

        self.archive_button = QPushButton("Archive Project")
        self.modify_button = QPushButton("Modify Project")
        self.add_phase_button = QPushButton("Add Phase")
        self.assign_workers_button = QPushButton("Assign Workers")

        self.layout.addWidget(self.project_title_label)
        self.layout.addWidget(self.due_date_label)
        self.layout.addWidget(self.project_manager_label)
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.description_text)
        self.layout.addWidget(self.phases_label)
        self.layout.addWidget(self.phases_text)
        self.layout.addWidget(self.archive_button)
        self.layout.addWidget(self.modify_button)
        self.layout.addWidget(self.add_phase_button)
        self.layout.addWidget(self.assign_workers_button)

        # Connect buttons to their functions
        self.archive_button.clicked.connect(self.archive_project)
        self.modify_button.clicked.connect(self.modify_project)
        self.add_phase_button.clicked.connect(self.open_add_phase_window)
        self.assign_workers_button.clicked.connect(self.open_assign_worker_window)  # Put connection to that page here

        # Load project details
        self.load_project_details()

    def load_project_details(self):
        """
        Loads project details from the database and updates the UI.

        Owen: This is the method you'll need to modify or connect
        to your function to get the actual project data.
        """

        
        conn = sqlite3.connect('data/workflow_manager.db')
        cursor = conn.cursor()

        # Fetch project details
        cursor.execute("SELECT projTitle, projDueDate, projManagerID, projDescription FROM Projects WHERE projID = ?", (self.project_id,))
        project = cursor.fetchone()

        if project:
            proj_title, proj_due_date, proj_manager_id, proj_description = project

            # Fetch project manager email
            cursor.execute("SELECT email FROM Users WHERE id = ?", (proj_manager_id,))
            manager_result = cursor.fetchone()
            manager_email = manager_result[0] if manager_result else "Not assigned"

            self.project_title_label.setText(f"Project Title: {proj_title}")
            self.due_date_label.setText(f"Due Date: {proj_due_date}")
            self.project_manager_label.setText(f"Project Manager: {manager_email}")
            self.description_text.setText(proj_description)

            # Fetch project phases
            cursor.execute("SELECT phaseTitle FROM Phases WHERE projID = ?", (self.project_id,))
            phases = cursor.fetchall()
            phase_text = "\n".join([phase[0] for phase in phases])
            self.phases_text.setText(phase_text)
        else:
            self.project_title_label.setText("Project not found.")

        conn.close()
        

    def archive_project(self):
        """
        (Placeholder) Archives the project.
        """
        pass

    def modify_project(self):
        def full_refresh():
            self.load_project_details()
            if self.refresh_callback:
                self.refresh_callback()

        self.modify_window = ProjectModifyWindow(
            self.project_id,
            refresh_callback=full_refresh
        )
        self.modify_window.show()

    def open_add_phase_window(self):
        self.phase_window = PhaseCreationWindow(self.project_id)
        self.phase_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        if self.refresh_callback is not None:
            self.phase_window.destroyed.connect(self.refresh_callback)
        self.phase_window.destroyed.connect(self.close)
        self.phase_window.show()

    def open_assign_worker_window(self):
        self.assign_window = AssignWorkerWindow(self.project_id)
        self.assign_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        if self.refresh_callback is not None:
            self.assign_window.destroyed.connect(self.refresh_callback)
        self.assign_window.destroyed.connect(self.close)
        self.assign_window.show()

