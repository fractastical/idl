import json
import datetime
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

# Path to the JSON file
TODO_FILE = 'todo_list.json'

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return {"subcategories": {"default": []}}

def process_data(todos, subcategory):
    time_spent_per_task = {}
    tasks_completed_over_time = defaultdict(int)
    tasks = todos["subcategories"].get(subcategory, [])
    
    for task in tasks:
        if task.get("completed"):
            completed_date = datetime.datetime.fromisoformat(task["completed"]).date()
            tasks_completed_over_time[completed_date] += 1
        if task.get("time_spent"):
            time_spent_per_task[task["task"]] = task["time_spent"]
    
    return time_spent_per_task, tasks_completed_over_time

def plot_time_spent(time_spent_per_task, subcategory):
    tasks = list(time_spent_per_task.keys())
    times = list(time_spent_per_task.values())
    plt.figure(figsize=(10, 5))
    plt.barh(tasks, times)
    plt.xlabel('Time Spent (seconds)')
    plt.ylabel('Task')
    plt.title(f'Time Spent per Task in {subcategory}')
    plt.tight_layout()
    plt.show()

def plot_tasks_completed(tasks_completed_over_time, subcategory):
    dates = sorted(tasks_completed_over_time.keys())
    completed_tasks = [tasks_completed_over_time[date] for date in dates]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, completed_tasks, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Tasks Completed')
    plt.title(f'Tasks Completed Over Time in {subcategory}')
    plt.grid(True)
    plt.show()

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <subcategory>")
        sys.exit(1)
    
    subcategory = sys.argv[1]
    todos = load_todos()
    
    if subcategory not in todos["subcategories"]:
        print(f"Subcategory '{subcategory}' not found in the todo list.")
        sys.exit(1)
    
    time_spent_per_task, tasks_completed_over_time = process_data(todos, subcategory)
    
    print(f"\nTime Spent per Task in {subcategory}:")
    for task, time_spent in time_spent_per_task.items():
        print(f"{task}: {time_spent / 3600:.2f} hours")
    
    print(f"\nTasks Completed Over Time in {subcategory}:")
    for date, count in tasks_completed_over_time.items():
        print(f"{date}: {count} tasks")
    
    plot_time_spent(time_spent_per_task, subcategory)
    plot_tasks_completed(tasks_completed_over_time, subcategory)

if __name__ == "__main__":
    main()