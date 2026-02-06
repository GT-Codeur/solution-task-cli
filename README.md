# task-cli

A minimal command-line task manager written in Python. Tasks are stored in a local JSON file (`db.json`) and can be added, updated, deleted and marked with simple statuses (todo, in-progress, done).

## Requirements

- Python 3.8+
- pytest (for running tests)

## Installation

Clone or copy the project files into a folder.

## Files

- `task-cli.py` - main CLI entrypoint
- `operations.py` - task operations (add, update, delete, mark-in-progress, mark-done, list)
- `db.json` - local JSON datastore that holds tasks
- `test_operations.py` - unit tests for operations

## Usage in linux or MacOS

To run it like:
```bash
task-cli <command> [arguments]
```
- Make task-cli executable:
```bash
chmod +x task-cli.py
```
- Change the name of task-cli.py to task-cli
```bash
mv task-cli.py task-cli
```
- Copy the python files and the db.json in `~/.local/bin/` (create it not created)
- Make sure `~/.local/bin/` is in your $PATH
- If not add it to `~/.bashrc` or `~/.zshrc`
```bash
export PATH="$HOME/.local/bin:$PATH"
```
- Reload: 
```bash 
source ~/.bashrc
``` 
Or/and restart the computer.

Run the CLI with Python:

python3 task-cli.py <command> [arguments]

Commands

- add: add a new task. Takes 1 argument: the task description
  - Example: 
  ```bash
  task-cli add "Buy milk"
  ```

- update: update an existing task. Takes 2 arguments: task id and new description
  - Example: 
  ```bash
  task-cli update 1 "Buy almond milk"
  ```

- delete: delete a task by id
  - Example: 
  ```bash
  task-cli delete 1
  ```

- mark-in-progress: set a task status to "in-progress" by id
  - Example: 
  ```bash 
  task-cli mark-in-progress 1
  ```

- mark-done: set a task status to "done" by id
  - Example:
  ```bash 
  task-cli mark-done 1
  ```

- list: list tasks
  - Example: 
  ```bash 
  task-cli list      # lists all tasks
  ```
  - Example: 
  ```bash 
  task-cli list todo  # lists tasks with status "todo"
  ```

Help

- Run: python3 task-cli.py -h
  or: python3 task-cli.py --help

Errors and validation

- Commands expect specific argument counts and types. Passing wrong arguments will print an error message.
- Task IDs are integers; non-integer IDs will trigger a helpful error.
