
#--------- STAGE 1 — Python Core Foundations----------
    # Goal: Think in Python

# What you’ll build
    # A Task & Habit Tracker (CLI)

# Features
    # Add tasks
    # View tasks
    # Mark tasks as completed
    # Simple statistics (tasks done today, this week)

# Concepts you’ll learn
    # Variables & data types
    # Lists & dictionaries
    # Functions
    # Loops
    # Conditionals
    # Input/output
    # Basic error handling

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

#----------- STAGE 2—Files & Data Persistence-------------

    # Goal: Make data survive program restarts

# New Features  
    # Save tasks to a file 
    # Load tasks on startup
    # Export reports

# Concepts
    # File handling (open)
    # JSON
    # with statements
    # Error handling (try/except)

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

#-------- STAGE 3 — Object-Oriented Programming (OOP)

# Goal: Write professional-quality code

# Upgrade
    # Convert tasks into classes

# Concepts
    # Classes & objects
    # __init__
    # Methods
    # Encapsulation

class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

    def complete(self):
        self.completed = True
