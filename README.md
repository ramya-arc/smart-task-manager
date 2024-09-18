# Smart Task Manager

#### Description:
The Smart Task Manager is a Python-based application designed to help users manage their tasks efficiently. This project includes both a command-line interface and a web application built using Flask. The application allows users to add, list, and delete tasks, as well as send email reminders for tasks due today.

## Features:
- **Task Management:** Add, edit, delete, and view tasks.
- **Task Status:** Mark tasks as completed or pending.
- **Reminders:** Schedule email reminders for tasks.
- **User Interface:** Aesthetic and user-friendly design with Bootstrap.

## Requirements:
- Python 3.x
- Flask
- smtplib
- email
- datetime

## Setup:
1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`

## Testing:
- Run `pytest` to execute the tests in `test_project.py`.

## How to Use:
### Command-Line Interface:
1. Run the application: `python project.py`
2. Follow the on-screen prompts to add, list, or delete tasks.

### Web Interface:
1. Run the application: `python app.py`
2. Open your web browser and go to `http://127.0.0.1:5000/`
3. Use the interface to add, list, or delete tasks.

## Acknowledgements:
This project was created as part of the CS50P final project. Special thanks to the CS50 team for their excellent course.
