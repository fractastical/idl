import json
import datetime
import os
import matplotlib.pyplot as plt
from collections import defaultdict

# Path to the JSON file
TODO_FILE = 'todo_list.json'

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return {"subcategories": {"default": []}}

def process_data(todos):
    time_spent_per_category = defaultdict(float)
    time_spent_per_task = {}
    tasks_completed_over_time = defaultdict(int)

    for subcategory, tasks in todos["subcategories"].items():
        for task in tasks:
            if task.get("completed"):
                completed_date = datetime.datetime.fromisoformat(task["completed"]).date()
                tasks_completed_over_time[completed_date] += 1

            if task.get("time_spent"):
                time_spent_per_category[subcategory] += task["time_spent"]
                time_spent_per_task[task["task"]] = task["time_spent"]

    return time_spent_per_category, time_spent_per_task, tasks_completed_over_time

def plot_time_spent(time_spent_per_category, time_spent_per_task):
    # Plot time spent per category
    categories = list(time_spent_per_category.keys())
    times = list(time_spent_per_category.values())

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(categories, times)
    plt.xlabel('Category')
    plt.ylabel('Time Spent (seconds)')
    plt.title('Time Spent per Category')

    # Plot time spent per task
    tasks = list(time_spent_per_task.keys())
    times = list(time_spent_per_task.values())

    plt.subplot(1, 2, 2)
    plt.barh(tasks, times)
    plt.xlabel('Time Spent (seconds)')
    plt.ylabel('Task')
    plt.title('Time Spent per Task')

    plt.tight_layout()
    plt.show()

def plot_tasks_completed(tasks_completed_over_time):
    dates = sorted(tasks_completed_over_time.keys())
    completed_tasks = [tasks_completed_over_time[date] for date in dates]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, completed_tasks, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Tasks Completed')
    plt.title('Tasks Completed Over Time')
    plt.grid(True)
    plt.show()

def main():
    todos = load_todos()
    time_spent_per_category, time_spent_per_task, tasks_completed_over_time = process_data(todos)

    print("Time Spent per Category:")
    for category, time_spent in time_spent_per_category.items():
        print(f"{category}: {time_spent / 3600:.2f} hours")

    print("\nTime Spent per Task:")
    for task, time_spent in time_spent_per_task.items():
        print(f"{task}: {time_spent / 3600:.2f} hours")

    print("\nTasks Completed Over Time:")
    for date, count in tasks_completed_over_time.items():
        print(f"{date}: {count} tasks")

    plot_time_spent(time_spent_per_category, time_spent_per_task)
    plot_tasks_completed(tasks_completed_over_time)

if __name__ == "__main__":
    main()
