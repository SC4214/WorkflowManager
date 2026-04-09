"""
phase_create_window.py

This module defines the user interface for phase creation using PyQt6.

Responsibilities:
    - Display a window for creating a new project phase
    - Collect user input (phase title, due date, description)
    - Perform basic input validation
    - Communicate with the phase creation service
    - Provide user feedback (error/success confirmations)
"""

from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QMessageBox,
    QLabel
)

from services.phase_creator import create_phase


"""
class: PhaseCreationWindow

Represents a window for creating a new phase associated with a project.

This class handles UI layout, user input collection, and
interaction with the backend phase creation service.
"""
class PhaseCreationWindow(QWidget):

    """
    __init__

    constructor

    PRE:
        - PyQt6 environment is properly installed and configured
        - A valid project ID is provided

    POST:
        - A window is created with input fields for phase title, due date, and description
        - UI elements are initialized and displayed
        - Event handlers are connected to their respective UI controls
    """
    def __init__(self, proj_id, parent=None):
        super().__init__(parent)

        self.proj_id = proj_id

        self.setWindowTitle("Project Workflow Manager - Create Phase")
        self.resize(500, 350)

        # --- Create widgets ---
        self.title_input = QLineEdit()

        # Date stored as text input
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")

        self.description_input = QTextEdit()

        self.message_label = QLabel("")

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)

        # --- Layout ---
        form_layout = QFormLayout()
        form_layout.addRow("Phase Title:", self.title_input)
        form_layout.addRow("Due Date:", self.date_input)
        form_layout.addRow("Description:", self.description_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.submit_button)

        self.setLayout(main_layout)


    """
    on_submit

    PRE:
        - The user has interacted with the window and provided values
        - UI input fields are accessible
        - A valid project ID is stored in the instance

    POST:
        - If input validation fails, an error message is displayed and
          the window remains open
        - If phase creation fails, an error message is displayed and
          the window remains open
        - If phase creation succeeds, a confirmation message is shown
          and the window is closed

    Returns:
        - None
    """
    def on_submit(self):
        self.message_label.setText("")

        # Input from fields
        title_text = self.title_input.text().strip()
        date_text = self.date_input.text().strip()
        description_text = self.description_input.toPlainText().strip()

        # Basic validation
        if not title_text or not date_text:
            self.message_label.setText("Phase title and due date are required.")
            return

        # Tuple for success determination
        success, message = create_phase(
            self.proj_id,
            title_text,
            date_text,
            description_text
        )

        if not success:
            self.message_label.setText(message)
            return

        QMessageBox.information(self, "Success", message)

        self.close()