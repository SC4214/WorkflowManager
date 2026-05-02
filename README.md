# *User Manual*

## Description

The Project Workflow Manager (PWFM) is a calendar application for users to
manage their projects, view dependencies, create project phases, and manage
assignment and visibility of phases to assigned workers.

## Creating an account (Steven)

When the application launches, the login screen is displayed. If you
do not have an account, click the **"Register"** button to create one.

<p align="center">
  <img src="documents/Images/Login_Window_Register.png" width="500">
</p>

The account creation window opens. The Email field accepts
either a username or an email address. Password requirements may vary
depending on system configuration. Type in both the desired username/email
and password, confirm your password in the **"Confirm Password"** field,
and click **"Create"**.

*Note: email/usernames are unique within the system.*

<p align="center">
  <img src="documents/Images/Acc_Creation_Window.png" width="500">
</p>

**Result:** A success confirmation appears. Click **"OK"** and proceed to Login.

<p align="center">
  <img src="documents/Images/Create_Success.png" width="400">
</p>

### Common Errors

Account creation may fail for multiple reasons. Here are some common
errors and how to resolve them:
- **Error: All fields are required**
  - Cause: One or more fields were left blank.
  - Solution: Complete all fields and click "Create".
- **Error: An account with that email already exists**
  - Cause: The entered username/email is already in use.
  - Solution:
    - If using a username: choose a different username.
    - If using an email: contact your organization.
- **Error: Passwords do not match**
  - Cause: Password and Confirm Password fields differ.
  - Solution: Re-enter both fields and click **Create**.

## Login (Pedro)


When you launch the application, the first screen you will see is the login window.

<p align="center">
  <img src="documents/Images/login_window.png" width="400">
</p>

To log in, follow these steps:

1.  **Email:** In the first field, enter the email address you registered with.
2.  **Password:** In the second field, enter your password.
3.  **"Login" Button:** Click the `Login` button.

If your credentials are correct, the application will grant you access to the main Dashboard. If there is an error (e.g., incorrect password or email), you will receive a notification and can try again.

## Creating a Project (Owen)

To create a project, first click on the **"Create Project"** button located in the upper left hand corner of the **Dashboard**. 

<p align="center">
  <img src="documents/Images/CreateProjectLocation.png" width="500">
</p>

This will bring you to the **"Create Project"** Window.

<p align="center">
  <img src="documents/Images/CreateProjectEmpty.png" width="500">
</p>

To create a new project, complete the following steps:


1.) Type the Name of your project into the Title field.

2.) Type the Due Date for your project into the Date field using the YYYY-MM-DD date format.

3.) Type the Description you want for your project into the descrioption box.

4.) Click Submit

*Note: Project Titles are unique within the system.*

<p align="center">
  <img src="documents/Images/CreaateProjectFilled.png" width="500">
</p>

Result: A success confirmation appears. Clicking "OK" will close the **Create Project** Window and return you to the **Dashboard**.

<p align="center">
  <img src="documents/Images/CreateProjectSuccess.png" width="500">
</p>

### Common Errors

Project Creation may fail for multiple reasons. Here are some common
errors and how to resolve them:
- **Error: All fields are required**
  - Cause: One or more fields were left blank.
  - Solution: Complete all fields and click "Submit".
- **Error: An project with that title already exists**
  - Cause: The entered title already exists for another project within the system.
  - Solution:
    - Choose a different title for the project.
    - Click "Submit".

## Modifying a Project (Pedro)

You can easily update a project's due date or description by following these three simple steps.

### Step 1: Select the Project

First, locate and click on the project you wish to modify. You can find your projects on the main **Dashboard** calendar or in the **Project List**. Clicking the project will open its **Project Details** window.

<p align="center">
  <img src="documents/Images/pic1.png" width="400">
</p>

### Step 2: Click the "Modify Project" Button

In the **Project Details** window, you will find a `Modify Project` button. Click this button to open the project modification screen, where the project's current details will be pre-filled and ready for editing.

<p align="center">
  <img src="documents/Images/pic2 (2).png" width="400">
</p>

### Step 3: Modify and Save Changes

You can now change the **Due Date** or update the **Description**. Once you are finished making your changes, click the `Save Changes` button to update the project.

<p align="center">
  <img src="documents/Images/pic3.png" width="400">
</p>

Your project is now updated. The new details will be reflected immediately on the main **Dashboard**.

## Creating a Phase (Steven)

After creating a project and viewing its details, you can add phases
to organize and track project work.

From the **Project Details** window, click the **"Add Phase"** button
to open the phase creation window.

<p align="center">
  <img src="documents/Images/Project_Details_for_Phase.png" width="500">
</p>

In the phase creation window, enter the following information:
- Phase Title
- Due Date (formatted as `YYYY-MM-DD`)
- Steps (description or list of tasks associated with the phase)

After entering the required information, click **"Submit"**.

<p align="center">
  <img src="documents/Images/Phase_Creation_Window.png" width="500">
</p>

**Result:** A confirmation message will appear indicating that the phase
was created successfully. Click **"OK"** to continue.

<p align="center">
  <img src="documents/Images/Phase_Success.png" width="400">
</p>

### Viewing a Phase

Once created, the phase will appear on the calendar under its assigned
due date.

Phases are color-coded based on their proximity to the current date:
- Green  → Over a month away
- Yellow → Between a week and a month
- Red    → Less than a week or past due

<p align="center">
  <img src="documents/Images/New_Phase_On_Calendar.png" width="400">
</p>

### Viewing Phase Details

Click on a phase within the calendar to view its details, including:
- Project Title
- Phase Title
- Due Date
- Steps / Description

<p align="center">
  <img src="documents/Images/Phase_Details_Window.png" width="500">
</p>

### Common Errors

Phase creation may fail for multiple reasons. Here are some common
errors and how to resolve them:
- **Error: Phase title and due date are required.**
  - Cause: Either Phase title or Due Date is empty.
  - Solution: Fill in both required fields and click **"Submit"**
- **Error: A phase with this title already exists for that project.**
  - Cause: The selected project already has a phase with the same name.
  - Solution: Verify the phase you are creating has not already been made.
              Choose a new Phase title and click **"Submit"**

## Assigning Users to Phases (Owen)

Once a phase has been created, you can assign other users to that phase.

First, locate the project of the phase you wish to assign a user to on your **Calendar**.

<p align="center">
  <img src="documents/Images/PhaseAssignLocate.png" width="500">
</p>

Open the **Project Details** window, and select the **"Assign Workers"** button. 

<p align="center">
  <img src="documents/Images/PhaseAssignWorkerButton.png" width="500">
</p>

This will bring you to the **"Assign Workers"** Page.

<p align="center">
  <img src="documents/Images/PhaseAssignEmpty.png" width="500">
</p>

To assign one or more users to a phase, complete the following steps:


1.) Select all of the users you with to assign from the left hand column. Clicking the --> button will transfer them to the right column to be assigned. Selecting users in the right column and clicking the <-- button will return them to the left column, removing them from the list of users to assign.

2.) Choose which phase you want to assign users to from the **"Select Phase"** dropdown box.

3.) Type the Role you want your selected users to have for this phase into the **"Select Role"** field.

4.) Click Submit

*Note: Each user may only be assigned to a phase once.*

<p align="center">
  <img src="documents/Images/PhaseassignFilled.png" width="500">
</p>

Result: A success confirmation appears. Clicking "OK" will close the **Assign Worker** Window and return you to the **Dashboard**.

<p align="center">
  <img src="documents/Images/PhaseAssignSuccess.png" width="500">
</p>

### Common Errors

Phase Assignment may fail for multiple reasons. Here are some common
errors and how to resolve them:
- **Error: Please enter a roll**
  - Cause: The Role field has been left blank.
  - Solution: Enter a role in the Role field and click "Submit".
- **Please assign at least one worker**
  - Cause: No user has been chosen to be assigned by moving them from the left to right column.
  - Solution: Choose at least one user to assign to the phase, and move them
    - Choose at least one user to assign to the phase, and move them from the left to right column using the arrow buttons.
    - Click "Submit".
- **One or more of the selected employees is already assigned to this phase**
  - Cause: One of the users you are attempting to assign as already been asigned to this phase.
  - Solution:
    - Remove the already assigned user from the right column.
    - If you do not know which user is already assigned, assign users one at a time.
