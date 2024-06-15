import json
import datetime
import os

# Path to the JSON file
TODO_FILE = 'todo_list.json'

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as file:
        json.dump(todos, file, indent=4)

def display_todos(todos):
    print("\nTo-Do List:")
    for idx, todo in enumerate(todos):
        if not todo.get('completed'):
            status = "Benched" if todo.get('benched') else "Pending"
            bench_info = f" (Benched: {todo['benched']})" if todo.get('benched') else ""
            print(f"{idx + 1}. {todo['task']} (Created: {todo['created']}){bench_info} - Status: {status}")
    print()

def add_todo(task):
    todos = load_todos()
    new_todo = {
        "task": task,
        "created": datetime.datetime.now().isoformat(),
        "completed": None,
        "benched": None
    }
    todos.append(new_todo)  # Append at the end
    save_todos(todos)

def mark_todo_complete(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        if todos[index].get('completed') is None:
            todos[index]['completed'] = datetime.datetime.now().isoformat()
            save_todos(todos)
            print(f"Marked item {index + 1} as complete.")
        else:
            print("This item is already marked as complete.")
    else:
        print("Invalid index.")

def bench_todo_item(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        if todos[index].get('completed') is None:
            todos[index]['benched'] = datetime.datetime.now().isoformat()
            save_todos(todos)
            print(f"Benched item {index + 1}.")
        else:
            print("This item is already marked as complete.")
    else:
        print("Invalid index.")

def main():
    while True:
        todos = load_todos()
        display_todos(todos)
        user_input = input("Enter a new to-do item, the number of an item to mark it as complete, or 'b' followed by the number of an item to bench it (or 'q' to quit): ")

        if user_input.lower() == 'q':
            break
        elif user_input.isdigit():
            mark_todo_complete(int(user_input) - 1)
        elif user_input.lower().startswith('b'):
            try:
                index = int(user_input[1:]) - 1
                bench_todo_item(index)
            except ValueError:
                print("Invalid input for benching an item.")
        else:
            add_todo(user_input)
            display_todos(load_todos())  # Display the updated list after adding a new item

if __name__ == "__main__":
    main()
