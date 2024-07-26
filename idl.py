import json
import datetime
import os

# Path to the JSON file
TODO_FILE = 'todo_list.json'
IDEAS_FILE = 'ideas_list.json'

def migrate_todo_data():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            data = json.load(file)
        if isinstance(data, list):
            # Old format detected, migrate to new format
            new_data = {"subcategories": {"default": data}}
            save_todos(new_data)
            print("Migrated old to-do list format to new subcategory format.")
        elif isinstance(data, dict) and "subcategories" in data:
            print("To-do list is already in the new format.")
        else:
            print("Unknown format, please check the data manually.")
    else:
        # No existing file, create a new structure
        save_todos({"subcategories": {"default": []}})
        print("Initialized new to-do list structure.")

def initialize_task_fields(todos):
    for subcategory in todos["subcategories"]:
        for task in todos["subcategories"][subcategory]:
            if "in_progress" not in task:
                task["in_progress"] = False
            if "start_time" not in task:
                task["start_time"] = None
            if "time_spent" not in task:
                task["time_spent"] = 0
    return todos

def load_todos():
    migrate_todo_data()  # Ensure data is migrated before loading
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            todos = json.load(file)
        todos = initialize_task_fields(todos)
        return todos
    return initialize_task_fields({"subcategories": {"default": []}})

def load_ideas():
    if os.path.exists(IDEAS_FILE):
        with open(IDEAS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'w') as file:
        json.dump(todos, file, indent=4)

def save_ideas(ideas):
    with open(IDEAS_FILE, 'w') as file:
        json.dump(ideas, file, indent=4)

def display_subcategories(todos):
    print("\nSubcategories:")
    subcategories = list(todos["subcategories"].keys())
    for idx, subcategory in enumerate(subcategories):
        print(f"{idx + 1}. {subcategory}")
    print()
    return subcategories

def display_todos(todos, subcategory, show_benched=False):
    print(f"\nTo-Do List ({subcategory}):" if not show_benched else f"\nBenched Items ({subcategory}):")
    count = 1
    displayed_todos = []
    for idx, todo in enumerate(todos["subcategories"][subcategory]):
        if show_benched:
            if todo.get('benched') and not todo.get('completed'):
                print(f"{count}. {todo['task']} (Created: {todo['created']}, Benched: {todo['benched']})")
                displayed_todos.append(idx)
                count += 1
        else:
            status = "In Progress" if todo.get('in_progress') else "Not Started"
            if not todo.get('completed') and not todo.get('benched'):
                print(f"{count}. {todo['task']} (Created: {todo['created']}, Status: {status})")
                displayed_todos.append(idx)
                count += 1
            elif not todo.get('completed') and todo.get('unbenched'):
                print(f"{count}. {todo['task']} (Created: {todo['created']}, Benched: {todo['benched']}, Unbenched: {todo['unbenched']}, Status: {status})")
                displayed_todos.append(idx)
                count += 1
    print()
    return displayed_todos

def display_ideas(ideas):
    print("\nIdeas:")
    for idx, idea in enumerate(ideas):
        print(f"{idx + 1}. {idea['task']} (Created: {idea['created']})")
    print()

def add_todo(task, subcategory):
    todos = load_todos()
    new_todo = {
        "task": task,
        "created": datetime.datetime.now().isoformat(),
        "completed": None,
        "benched": None,
        "unbenched": None,
        "in_progress": False,
        "start_time": None,
        "time_spent": 0  # In seconds
    }
    todos["subcategories"][subcategory].append(new_todo)
    save_todos(todos)

def add_idea(task):
    ideas = load_ideas()
    new_idea = {
        "task": task,
        "created": datetime.datetime.now().isoformat()
    }
    ideas.append(new_idea)
    save_ideas(ideas)

def move_idea_to_todo(index, subcategory):
    ideas = load_ideas()
    if 0 <= index < len(ideas):
        idea = ideas.pop(index)
        add_todo(idea['task'], subcategory)
        save_ideas(ideas)
        print(f"Moved idea {index + 1} to to-do list under {subcategory}.")
    else:
        print("Invalid index.")

def mark_todo_complete(index, displayed_todos, subcategory):
    todos = load_todos()
    if 0 <= index < len(displayed_todos):
        todo_index = displayed_todos[index]
        todos["subcategories"][subcategory][todo_index]['completed'] = datetime.datetime.now().isoformat()
        if todos["subcategories"][subcategory][todo_index]['in_progress']:
            todos["subcategories"][subcategory][todo_index]['in_progress'] = False
            time_spent = (datetime.datetime.now() - datetime.datetime.fromisoformat(todos["subcategories"][subcategory][todo_index]['start_time'])).total_seconds()
            todos["subcategories"][subcategory][todo_index]['time_spent'] += time_spent
            todos["subcategories"][subcategory][todo_index]['start_time'] = None
        save_todos(todos)
        print(f"Marked item {index + 1} as complete.")
    else:
        print("Invalid index.")

def bench_todo_item(index, displayed_todos, subcategory):
    todos = load_todos()
    if 0 <= index < len(displayed_todos):
        todo_index = displayed_todos[index]
        todos["subcategories"][subcategory][todo_index]['benched'] = datetime.datetime.now().isoformat()
        save_todos(todos)
        print(f"Benched item {index + 1}.")
    else:
        print("Invalid index.")

def unbench_todo_item(index, displayed_todos, subcategory):
    todos = load_todos()
    if 0 <= index < len(displayed_todos):
        todo_index = displayed_todos[index]
        todos["subcategories"][subcategory][todo_index]['unbenched'] = datetime.datetime.now().isoformat()
        todos["subcategories"][subcategory][todo_index]['benched'] = None
        save_todos(todos)
        print(f"Unbenched item {index + 1}.")
    else:
        print("Invalid index.")

def create_subcategory(subcategory):
    todos = load_todos()
    if subcategory not in todos["subcategories"]:
        todos["subcategories"][subcategory] = []
        save_todos(todos)
        print(f"Created subcategory '{subcategory}'.")
    else:
        print(f"Subcategory '{subcategory}' already exists.")

def move_todo_to_subcategory(index, displayed_todos, from_subcategory, to_subcategory):
    todos = load_todos()
    if 0 <= index < len(displayed_todos):
        todo_index = displayed_todos[index]
        todo_item = todos["subcategories"][from_subcategory].pop(todo_index)
        todos["subcategories"][to_subcategory].append(todo_item)
        save_todos(todos)
        print(f"Moved item {index + 1} from '{from_subcategory}' to '{to_subcategory}'.")
    else:
        print("Invalid index.")

def start_todo_in_progress(index, displayed_todos, subcategory):
    todos = load_todos()
    # Ensure no other item is in progress
    for subcat, tasks in todos["subcategories"].items():
        for task in tasks:
            if task['in_progress']:
                print("Another task is already in progress. Complete or stop that task before starting a new one.")
                return
    if 0 <= index < len(displayed_todos):
        todo_index = displayed_todos[index]
        todos["subcategories"][subcategory][todo_index]['in_progress'] = True
        todos["subcategories"][subcategory][todo_index]['start_time'] = datetime.datetime.now().isoformat()
        save_todos(todos)
        print(f"Started item {index + 1} as in progress.")
    else:
        print("Invalid index.")

def stop_todo_in_progress():
    todos = load_todos()
    found = False
    for subcat, tasks in todos["subcategories"].items():
        for task in tasks:
            if task['in_progress']:
                found = True
                task['in_progress'] = False
                time_spent = (datetime.datetime.now() - datetime.datetime.fromisoformat(task['start_time'])).total_seconds()
                task['time_spent'] += time_spent
                task['start_time'] = None
                save_todos(todos)
                print(f"Stopped task '{task['task']}' in progress.")
                break
        if found:
            break
    if not found:
        print("No task is currently in progress.")

def main():
    show_benched = False
    in_ideas = False
    current_subcategory = None
    
    while True:
        if current_subcategory is None:
            todos = load_todos()
            subcategories = display_subcategories(todos)
            user_input = input("Enter the number of a subcategory to view its to-do list, 'create' followed by subcategory name to create a new subcategory, or 'q' to quit: ")
        else:
            if in_ideas:
                ideas = load_ideas()
                display_ideas(ideas)
                user_input = input("Ideas view - Enter the number of an idea to move it to the to-do list, or 'i' to return to main list (or 'q' to quit): ")
            else:
                todos = load_todos()
                displayed_todos = display_todos(todos, current_subcategory, show_benched)
                if show_benched:
                    user_input = input("Benched view - Enter the number of an item to unbench it, or 'v' to view main list (or 'q' to quit): ")
                else:
                    user_input = input(f"Enter a new to-do item, the number of an item to mark it as complete, 'b' followed by the number of an item to bench it, 'i' to view ideas, 'v' to view benched items, 'move' followed by the number and subcategory to move an item (e.g., 'move 3 ia'), 'start' followed by the number to start an item in progress, 'stop' to stop the current in progress item, or 'back' to go back to subcategories (or 'q' to quit): ")

        if user_input.lower() == 'q':
            break
        elif user_input.lower().startswith('create') and current_subcategory is None:
            _, subcategory = user_input.split(' ', 1)
            create_subcategory(subcategory)
        elif user_input.lower() == 'back' and current_subcategory is not None:
            current_subcategory = None
        elif user_input.lower() == 'v' and not in_ideas:
            show_benched = not show_benched
        elif user_input.lower() == 'i':
            in_ideas = not in_ideas
        elif user_input.isdigit():
            index = int(user_input) - 1
            if current_subcategory is None:
                if 0 <= index < len(subcategories):
                    current_subcategory = subcategories[index]
                else:
                    print("Invalid index.")
            else:
                if in_ideas:
                    move_idea_to_todo(index, current_subcategory)
                elif show_benched:
                    unbench_todo_item(index, displayed_todos, current_subcategory)
                else:
                    mark_todo_complete(index, displayed_todos, current_subcategory)
        elif user_input.lower().startswith('b') and not in_ideas:
            try:
                index = int(user_input[1:]) - 1
                bench_todo_item(index, displayed_todos, current_subcategory)
            except ValueError:
                print("Invalid input for benching an item.")
        elif user_input.lower().startswith('move') and not in_ideas:
            try:
                _, index_str, to_subcategory = user_input.split(' ', 2)
                index = int(index_str) - 1
                move_todo_to_subcategory(index, displayed_todos, current_subcategory, to_subcategory)
            except ValueError:
                print("Invalid input for moving an item.")
        elif user_input.lower().startswith('start') and not in_ideas:
            try:
                index = int(user_input[6:]) - 1
                start_todo_in_progress(index, displayed_todos, current_subcategory)
            except ValueError:
                print("Invalid input for starting an item in progress.")
        elif user_input.lower() == 'stop' and not in_ideas:
            stop_todo_in_progress()
        elif not in_ideas:
            add_todo(user_input, current_subcategory)
            displayed_todos = display_todos(load_todos(), current_subcategory, show_benched)  # Display the updated list after adding a new item
        else:
            add_idea(user_input)
            display_ideas(load_ideas())  # Display the updated list after adding a new idea

if __name__ == "__main__":
    main()
