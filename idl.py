import json
import datetime
import os

# Path to the JSON file
TODO_FILE = 'ipm_todo_list.json'

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as file:
        json.dump(todos, file, indent=4)

def display_todos(todos, show_benched=False):
    print("\nTo-Do List:" if not show_benched else "\nBenched Items:")
    count = 1
    displayed_todos = []
    for idx, todo in enumerate(todos):
        if show_benched:
            if todo.get('benched') and not todo.get('completed'):
                print(f"{count}. {todo['task']} (Created: {todo['created']}, Benched: {todo['benched']})")
                displayed_todos.append(idx)
                count += 1
        else:
            if not todo.get('completed') and not todo.get('benched'):
                print(f"{count}. {todo['task']} (Created: {todo['created']})")
                displayed_todos.append(idx)
                count += 1
            elif not todo.get('completed') and todo.get('unbenched'):
                print(f"{count}. {todo['task']} (Created: {todo['created']}, Benched: {todo['benched']}, Unbenched: {todo['unbenched']})")
                displayed_todos.append(idx)
                count += 1
    print()
    return displayed_todos

def add_todo(task):
    todos = load_todos()
    new_todo = {
        "task": task,
        "created": datetime.datetime.now().isoformat(),
        "completed": None,
        "benched": None,
        "unbenched": None
    }
    todos.append(new_todo)  # Append at the end
    save_todos(todos)

def mark_todo_complete(index, displayed_todos):
    todos = load_todos()
    if 0 <= index < len(displayed_todos):
        todo_index = displayed_todos[index]
        todos[todo_index]['completed'] = datetime.datetime.now().isoformat()
        save_todos(todos)
        print(f"Marked item {index + 1} as complete.")
    else:
        print("Invalid index.")

def bench_todo_item(index, displayed_todos):
    todos = load_todos()
    if 0 <= index < len(displayed_todos):
        todo_index = displayed_todos[index]
        todos[todo_index]['benched'] = datetime.datetime.now().isoformat()
        save_todos(todos)
        print(f"Benched item {index + 1}.")
    else:
        print("Invalid index.")

def unbench_todo_item(index, displayed_todos):
    todos = load_todos()
    if 0 <= index < len(displayed_todos):
        todo_index = displayed_todos[index]
        todos[todo_index]['unbenched'] = datetime.datetime.now().isoformat()
        todos[todo_index]['benched'] = None
        save_todos(todos)
        print(f"Unbenched item {index + 1}.")
    else:
        print("Invalid index.")

def main():
    show_benched = False
    while True:
        todos = load_todos()
        displayed_todos = display_todos(todos, show_benched)
        if show_benched:
            user_input = input("Benched view - Enter the number of an item to unbench it, or 'v' to view main list (or 'q' to quit): ")
        else:
            user_input = input("Enter a new to-do item, the number of an item to mark it as complete, 'b' followed by the number of an item to bench it, or 'v' to view benched items (or 'q' to quit): ")

        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'v':
            show_benched = not show_benched
        elif user_input.isdigit():
            index = int(user_input) - 1
            mark_todo_complete(index, displayed_todos)
        elif user_input.lower().startswith('b'):
            try:
                index = int(user_input[1:]) - 1
                bench_todo_item(index, displayed_todos)
            except ValueError:
                print("Invalid input for benching an item.")
        else:
            add_todo(user_input)
            displayed_todos = display_todos(load_todos(), show_benched)  # Display the updated list after adding a new item

if __name__ == "__main__":
    main()
