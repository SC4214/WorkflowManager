"""
assign_workers_window.py

This module defines the user interface for worker assignment using PyQt6.

Responsibilities:
    - Display a window for assigning workers to a project phase
    - Load available phases for the selected project
    - Load available users from the database
    - Perform basic input validation
    - Communicate with the worker assignment service
    - Provide user feedback (error/success confirmations)
"""
from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QLabel,
    QListWidget,
    QHBoxLayout,
    QComboBox
)
import sqlite3
from PyQt6.QtCore import Qt
from services.role_assigner import assign_role


"""
class: AssignWorkerWindow

Represents a window for assigning workers to a project phase.

This class handles UI layout, user input collection, and
interaction with the backend worker assignment service.
"""
class AssignWorkerWindow(QWidget):

    """
    __init__

    constructor

    PRE:
        - PyQt6 environment is properly installed and configured
        - A valid project ID is provided

    POST:
        - A window is created with input fields for choosing workers to assign
        - UI elements are initialized and displayed
        - Event handlers are connected to their respective UI controls
        - Available phases and workers are loaded from the database
    """
    def __init__(self, proj_id, parent=None):
        super().__init__(parent)

        self.proj_id = proj_id

        self.setWindowTitle("Assign Workers")
        self.resize(650, 420)

        # --- Title ---
        title_label = QLabel("Assign Workers to Project")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # --- Phase dropdown ---
        self.phase_dropdown = QComboBox()
        self.load_phases()

        # --- Role input ---
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Enter role (e.g., Developer)")

        # --- Available workers ---
        self.available_list = QListWidget()
        self.available_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        # --- Assigned workers ---
        self.assigned_list = QListWidget()
        self.assigned_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        # --- Move buttons ---
        self.add_button = QPushButton("→")
        self.remove_button = QPushButton("←")

        self.add_button.clicked.connect(self.move_to_assigned)
        self.remove_button.clicked.connect(self.move_to_available)

        button_layout = QVBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addStretch()

        # --- Two-column layout ---
        columns_layout = QHBoxLayout()
        columns_layout.addWidget(self.available_list)
        columns_layout.addLayout(button_layout)
        columns_layout.addWidget(self.assigned_list)

        # --- Submit button ---
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)

        # --- Main layout ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)

        main_layout.addWidget(QLabel("Select Phase:"))
        main_layout.addWidget(self.phase_dropdown)

        main_layout.addWidget(QLabel("Select Role:"))
        main_layout.addWidget(self.role_input)

        main_layout.addLayout(columns_layout)
        main_layout.addWidget(self.submit_button)

        self.setLayout(main_layout)

        # Load workers
        self.load_workers()

    # ---------------------------------------------------------
    # Load phases from DB
    # ---------------------------------------------------------
    def load_phases(self):
        """
        PRE:
            - The database file exists and is accessible
            - The Phases table exists in the database
            - self.proj_id contains a valid project ID

        POST:
            - The phase dropdown is cleared
            - All phases associated with the current project are loaded
              into the dropdown
        """
        conn = sqlite3.connect("data/workflow_manager.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT phaseID, phaseTitle FROM Phases WHERE projID = ?",
            (self.proj_id,)
        )
        phases = cursor.fetchall()

        self.phase_dropdown.clear()
        for pid, title in phases:
            self.phase_dropdown.addItem(title, pid)

        conn.close()

    # ---------------------------------------------------------
    # Load workers from DB
    # ---------------------------------------------------------
    def load_workers(self):
        """
        PRE:
            - The database file exists and is accessible
            - The Users table exists in the database

        POST:
            - The available workers list is cleared
            - All users are loaded into the available workers list
            - Each list item stores the corresponding user ID internally
        """
        conn = sqlite3.connect("data/workflow_manager.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, email FROM Users")
        workers_list = cursor.fetchall()

        self.available_list.clear()
        for user_id, email in workers_list:
            self.available_list.addItem(email)
            self.available_list.item(self.available_list.count() - 1).setData(
                Qt.ItemDataRole.UserRole,
                user_id
            )

        conn.close()

    # ---------------------------------------------------------
    # Move workers → assigned
    # ---------------------------------------------------------
    def move_to_assigned(self):
        """
        PRE:
            - One or more workers may be selected in the available list

        POST:
            - Selected workers are removed from the available list
            - Selected workers are added to the assigned list
            - Stored user ID metadata is preserved
        """
        for item in self.available_list.selectedItems():
            user_id = item.data(Qt.ItemDataRole.UserRole)
            self.available_list.takeItem(self.available_list.row(item))
            self.assigned_list.addItem(item.text())
            self.assigned_list.item(self.assigned_list.count() - 1).setData(
                Qt.ItemDataRole.UserRole,
                user_id
            )

    # ---------------------------------------------------------
    # Move workers ← available
    # ---------------------------------------------------------
    def move_to_available(self):
        """
        PRE:
            - One or more workers may be selected in the assigned list

        POST:
            - Selected workers are removed from the assigned list
            - Selected workers are returned to the available list
            - Stored user ID metadata is preserved
        """
        for item in self.assigned_list.selectedItems():
            user_id = item.data(Qt.ItemDataRole.UserRole)
            self.assigned_list.takeItem(self.assigned_list.row(item))
            self.available_list.addItem(item.text())
            self.available_list.item(self.available_list.count() - 1).setData(
                Qt.ItemDataRole.UserRole,
                user_id
            )

    # ---------------------------------------------------------
    # Submit assignments
    # ---------------------------------------------------------
    def on_submit(self):
        """
        PRE:
            - A phase should be selected
            - A role should be entered
            - At least one worker should be in the assigned list

        POST:
            - Validation errors are shown to the user if inputs are incomplete
            - Each assigned worker is submitted to the role assignment service
            - If all assignments succeed, a success message is shown
              and the window closes
            - If any assignment fails, an error message is shown
              and submission stops
        """
        phase_id = self.phase_dropdown.currentData()
        role = self.role_input.text().strip()

        if phase_id is None:
            QMessageBox.warning(self, "Error", "Please select a phase.")
            return

        if not role:
            QMessageBox.warning(self, "Error", "Please enter a role.")
            return

        if self.assigned_list.count() == 0:
            QMessageBox.warning(self, "Error", "Please assign at least one worker.")
            return

        for i in range(self.assigned_list.count()):
            item = self.assigned_list.item(i)
            user_id = item.data(Qt.ItemDataRole.UserRole)

            success, message = assign_role(user_id, phase_id, role)
            if not success:
                QMessageBox.warning(self, "Error", message)
                return

        QMessageBox.information(self, "Success", "Workers assigned successfully.")
        self.close()