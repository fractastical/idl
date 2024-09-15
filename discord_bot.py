import discord
from discord.ext import commands
import json
import datetime
import os
from idl import load_todos, save_todos, add_todo, mark_todo_complete

# Set up the Discord bot with minimal intents
intents = discord.Intents.default()
intents.message_content = False  # Disable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

# Specify the subcategory to use
SUBCATEGORY = 'ia'

# Specify the channel name where the bot should work
CHANNEL_NAME = 'feedback'

# Function to check if the command is used in the correct channel
def check_channel(ctx):
    return ctx.channel.name == CHANNEL_NAME

# Function to read the bot token from file
def read_bot_token():
    token_file = '.discord_bot_token'
    if not os.path.exists(token_file):
        raise FileNotFoundError(f"Bot token file '{token_file}' not found. Please create this file with your bot token.")
    with open(token_file, 'r') as file:
        return file.read().strip()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Ensure the Discord subcategory exists
    todos = load_todos()
    if SUBCATEGORY not in todos["subcategories"]:
        todos["subcategories"][SUBCATEGORY] = []
        save_todos(todos)

@bot.command(name='todos')
@commands.check(check_channel)
async def list_todos(ctx):
    todos = load_todos()
    todo_list = todos["subcategories"][SUBCATEGORY]
    
    if not todo_list:
        await ctx.send("The todo list is empty.")
        return
    
    response = "To-Do List:\n"
    for idx, todo in enumerate(todo_list):
        if not todo.get('completed') and not todo.get('benched'):
            status = "In Progress" if todo.get('in_progress') else "Not Started"
            response += f"{idx + 1}. {todo['task']} (Status: {status})\n"
    
    await ctx.send(response)

@bot.command(name='add')
@commands.check(check_channel)
async def add_todo_item(ctx, *, task):
    add_todo(task, SUBCATEGORY)
    await ctx.send(f"Added a new task to the todo list.")

@bot.command(name='complete')
@commands.check(check_channel)
async def complete_todo(ctx, index: int):
    todos = load_todos()
    todo_list = todos["subcategories"][SUBCATEGORY]
    
    if 0 < index <= len(todo_list):
        todo = todo_list[index - 1]
        if not todo.get('completed'):
            todo['completed'] = datetime.datetime.now().isoformat()
            save_todos(todos)
            await ctx.send(f"Marked item {index} as complete.")
        else:
            await ctx.send(f"Item {index} is already completed.")
    else:
        await ctx.send("Invalid index.")

@bot.command(name='start')
@commands.check(check_channel)
async def start_todo(ctx, index: int):
    todos = load_todos()
    todo_list = todos["subcategories"][SUBCATEGORY]
    
    if 0 < index <= len(todo_list):
        todo = todo_list[index - 1]
        if not todo.get('completed') and not todo.get('in_progress'):
            todo['in_progress'] = True
            todo['start_time'] = datetime.datetime.now().isoformat()
            save_todos(todos)
            await ctx.send(f"Started item {index}.")
        elif todo.get('completed'):
            await ctx.send(f"Item {index} is already completed.")
        else:
            await ctx.send(f"Item {index} is already in progress.")
    else:
        await ctx.send("Invalid index.")

@bot.command(name='stop')
@commands.check(check_channel)
async def stop_todo(ctx):
    todos = load_todos()
    todo_list = todos["subcategories"][SUBCATEGORY]
    stopped = False
    
    for task in todo_list:
        if task.get('in_progress'):
            task['in_progress'] = False
            time_spent = (datetime.datetime.now() - datetime.datetime.fromisoformat(task['start_time'])).total_seconds()
            task['time_spent'] += time_spent
            task['start_time'] = None
            save_todos(todos)
            await ctx.send(f"Stopped the in-progress task.")
            stopped = True
            break
    
    if not stopped:
        await ctx.send("No task is currently in progress.")

@bot.command(name='todohelp')
@commands.check(check_channel)
async def show_todo_help(ctx):
    help_text = """
    Available commands:
    !todos - List all todos
    !add <task> - Add a new todo
    !complete <index> - Mark a todo as complete
    !start <index> - Start working on a todo
    !stop - Stop working on the current todo
    !todohelp - Show this help message
    """
    await ctx.send(help_text)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"This command can only be used in the #{CHANNEL_NAME} channel.")

if __name__ == "__main__":
    try:
        bot_token = read_bot_token()
        bot.run(bot_token)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")