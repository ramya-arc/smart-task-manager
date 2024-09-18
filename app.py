import json
import os
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from dotenv import load_dotenv  

load_dotenv()

app = Flask(__name__)

DATA_FILE = 'data/tasks.json'

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

EMAIL_ADDRESS = os.getenv('GMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

def load_tasks():
    try:
        with open(DATA_FILE, 'r') as file:
            tasks = json.load(file)
            for task in tasks:
                if 'status' not in task:
                    task['status'] = 'pending'
                if 'email' not in task:
                    task['email'] = ''  
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(task_description, task_due_date=None, email=None):
    tasks = load_tasks()
    task = {"task_description": task_description, "task_due_date": task_due_date, "email": email, "status": "pending"}
    tasks.append(task)
    save_tasks(tasks)
    return task

def delete_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        task_to_delete = tasks.pop(task_index)
        save_tasks(tasks)
        return task_to_delete
    return None

def categorize_task(task_description):
    categories = {
        "work": ["meeting", "email", "report", "project"],
        "personal": ["groceries", "doctor", "appointment", "call"],
        "other": []
    }
    
    for category, keywords in categories.items():
        if any(keyword in task_description.lower() for keyword in keywords):
            return category
    return "other"

@app.context_processor
def utility_processor():
    def enumerate_wrapper(sequence):
        return enumerate(sequence)
    return dict(enumerate=enumerate_wrapper)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        task_description = request.form['task_description']
        task_due_date = request.form['task_due_date']
        email = request.form['email']
        category = categorize_task(task_description)
        add_task(task_description, task_due_date, email)
        return redirect(url_for('list_tasks'))
    return render_template('add.html')

@app.route('/list')
def list_tasks():
    tasks = load_tasks()
    return render_template('list.html', tasks=tasks)

@app.route('/delete/<int:task_index>', methods=['POST'])
def delete(task_index):
    delete_task(task_index)
    return redirect(url_for('list_tasks'))

def send_email_reminder(task):
    if not task['email']:
        return  

    subject = "Task Reminder"
    body = f"Reminder: Your task '{task['task_description']}' is due on {task['task_due_date']}."
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = task['email']
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, task['email'], text)
            print(f"Email sent to {task['email']}")  
    except Exception as e:
        print(f"Failed to send email: {e}")  


@app.route('/reminders')
def send_reminders():
    tasks = load_tasks()
    today = datetime.date.today().isoformat()
    print(f"Today's date: {today}")  # Debugging line
    for task in tasks:
        print(f"Checking task: {task}")  # Debugging line
        if task['task_due_date'] == today and task['email']:
            send_email_reminder(task)
    return redirect(url_for('list_tasks'))


@app.route('/stats')
def stats():
    tasks = load_tasks()
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task.get('status') == 'completed'])
    pending_tasks = total_tasks - completed_tasks
    return render_template('stats.html', total_tasks=total_tasks, completed_tasks=completed_tasks, pending_tasks=pending_tasks)

@app.route('/complete/<int:task_index>', methods=['POST'])
def complete_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        task = tasks[task_index]
        task['status'] = 'completed' if task['status'] == 'pending' else 'pending'
        save_tasks(tasks)
    return redirect(url_for('list_tasks'))

@app.route('/edit/<int:task_index>', methods=['GET', 'POST'])
def edit(task_index):
    tasks = load_tasks()
    if request.method == 'POST':
        task_description = request.form['task_description']
        task_due_date = request.form['task_due_date']
        tasks[task_index]['task_description'] = task_description
        tasks[task_index]['task_due_date'] = task_due_date
        save_tasks(tasks)
        return redirect(url_for('list_tasks'))
    task = tasks[task_index]
    return render_template('edit.html', task=task, task_index=task_index)

if __name__ == "__main__":
    app.run(debug=True)
