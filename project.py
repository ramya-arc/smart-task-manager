import json
import os

DATA_FILE = 'data/tasks.json'

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def main():
    while True:
        print("\nSmart Task Manager")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Delete Task")
        print("4. Edit Task")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            task_description = input("Enter Task Description: ")
            task_due_date = input("Enter due date of your Task: ")
            add_task(task_description, task_due_date)
            print(f"Your task '{task_description}' is added.")
        elif choice == "2":
            tasks = list_tasks()
            if tasks:
                for i, task in enumerate(tasks):
                    print(f"{i}: {task['task_description']} (Due: {task['task_due_date']})")
            else:
                print("No tasks found.")
        elif choice == '3':
            task_description = input("Enter the task to delete: ")
            task = delete_task(task_description)
            if task:
                print(f"Task deleted: {task}")
            else:
                print("Task not found or invalid index.")
        elif choice == '4':
            task_description = input("Enter the task to edit: ")
            task = edit_task(task_description)
            if task:
                print(f"Task edited: {task}")
            else:
                print("Task not found or invalid index.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def load_tasks():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(task_description, task_due_date=None):
    tasks = load_tasks()
    task = {"task_description": task_description, "task_due_date": task_due_date}
    tasks.append(task)
    save_tasks(tasks)
    return task

def list_tasks():
    return load_tasks()

def delete_task(task_description, index=None):
    tasks = load_tasks()
    matching_tasks = [task for task in tasks if task_description.lower() in task['task_description'].lower()]
    if matching_tasks:
        if index is None:
            for i, task in enumerate(matching_tasks):
                print(f"{i}: {task['task_description']} (Due: {task['task_due_date']})")
            index = int(input("Enter the index of the task to delete: "))
        if 0 <= index < len(matching_tasks):
            task_to_delete = matching_tasks[index]
            tasks.remove(task_to_delete)
            save_tasks(tasks)
            return task_to_delete
    return None

def edit_task(task_description, index=None):
    tasks = load_tasks()
    matching_tasks = [task for task in tasks if task_description.lower() in task['task_description'].lower()]
    if matching_tasks:
        if index is None:
            for i, task in enumerate(matching_tasks):
                print(f"{i}: {task['task_description']} (Due: {task['task_due_date']})")
            index = int(input("Enter the index of the task to edit: "))
        if 0 <= index < len(matching_tasks):
            task_to_edit = matching_tasks[index]
            new_description = input("Enter new task description: ")
            new_due_date = input("Enter new task due date: ")
            task_to_edit['task_description'] = new_description
            task_to_edit['task_due_date'] = new_due_date
            save_tasks(tasks)
            return task_to_edit
    return None

if __name__ == "__main__":
    main()
