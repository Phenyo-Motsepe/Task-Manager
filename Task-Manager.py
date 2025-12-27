tasks = []

def add_task(title):
    task = {
        "title": title,
        "completed": False
    }
    tasks.append(task)

def show_tasks():
    for index, task in enumerate(tasks):
        status = "✓" if task["completed"] else "✗"
        print(f"{index + 1}. {task['title']} [{status}]")

def complete_task(task_number):
    tasks[task_number - 1]["completed"] = True

while True:
    print("\n1. Add Task\n2. Show Tasks\n3. Complete Task\n4. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        title = input("Task title: ")
        add_task(title)
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        number = int(input("Task number: "))
        complete_task(number)
    elif choice == "4":
        break
import json

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

    def complete(self):
        self.completed = True
