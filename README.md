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

## Creating a Project (Owen)

## Viewing/Modifying a Project (Pedro)

## Creating a Phase (Steven)

After creating a project and viewing its details, you can add phases
to organize work and track progress.

From the **Project Details** window, click the **"Add Phase"** button
to open the phase creation window.

<p align="center">
  <img src="documents/Images/Project_Details_for_Phase.png" width="500">
</p>

In the phase creation window, enter the following information:
- Phase Title
- Due Date (formatted as YYYY-MM-DD)
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
- Green  -> Over a month away
- Yellow -> Between a week and a month
- Red    -> Less than a week or past due

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
-**Error: Phase title and due date are required.**
  - Cause: Either Phase title or Due Date is empty.
  - Solution: Fill in both required fields and click **"Submit"**
- **Error: A phase with this title already exists for that project.**
  - Cause: The selected project already has a phase with the same name.
  - Solution: Verify the phase you are creating has not already been made.
              Choose a new Phase title and click **"Submit"**

## Assigning Users to Phases (Owen)
