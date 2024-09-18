import pytest
from project import add_task, delete_task, list_tasks, save_tasks

def test_add_task():
    save_tasks([])  # Reset tasks
    task = add_task("Test Task", "2024-12-31")
    assert task in list_tasks()

def test_list_tasks():
    save_tasks([])  # Reset tasks
    add_task("Test Task 1", "2024-12-31")
    add_task("Test Task 2", "2024-11-30")
    tasks = list_tasks()
    assert len(tasks) == 2

def test_delete_task():
    save_tasks([])  # Reset tasks
    add_task("Test Task", "2024-12-31")
    tasks = list_tasks()
    assert len(tasks) == 1
    deleted_task = delete_task("Test Task", 0)
    tasks = list_tasks()
    assert deleted_task['task_description'] == "Test Task"
    assert len(tasks) == 0

if __name__ == "__main__":
    pytest.main()
