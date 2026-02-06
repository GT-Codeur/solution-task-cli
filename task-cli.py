#!/usr/bin/env python3
import sys
from operations import (
    add_task,
    update_task,
    delete_task,
    mark_in_progress,
    mark_done,
    list_task
)

args = sys.argv
operations = ["add", "update", "delete", "mark-in-progress", "mark-done", "list"]
if __name__ == "__main__":
    try:
        if args[1].lower() == "-h" or args[1].lower() == "--help" or args[1] == "help":
            print(
                """
    Usage: task-cli operation [argument(s)]\n
    Differents operations:\n
        1- add: to add a task. It takes 1 argument, the task description\n
        2- update: to update a task. It takes 2 argument, the task id and the task description\n
        3- delete: to delete a task. It takes 1 argument, the task id\n
        4- mark-in-progress: to update a task status from "todo" to "in-progress". It takes 1 argument, the task id\n
        5- mark-done: to update a task status to "done". It takes 1 argument, the task id\n
        6- list: ** task-cli list : lists all tasks\n
                 ** task-cli list [status] lists all tasks of a particular status.
                """
            )
        
        elif args[1].lower() == operations[0] and len(args) < 4:
            add_task(args[2])
        elif args[1].lower() == operations[1] and len(args) < 5:
            update_task(int(args[2]), args[3])
        elif args[1].lower() == operations[2] and len(args) < 4:
            delete_task(int(args[2]))
        elif args[1].lower() == operations[3] and len(args) < 4:
            mark_in_progress(int(args[2]))
        elif args[1].lower() == operations[4] and len(args) < 4:
            mark_done(int(args[2]))
        elif args[1].lower() == operations[5] and len(args) < 3:
            list_task()
        elif args[1].lower() == operations[5] and len(args) < 4:
            list_task(args[2])
        elif args[1].lower() not in operations:
            print(f"Error: We can't find \"{args[1]}\"!", "list of commands: ", operations, sep=" ")
        else:
            print("Error: The number of commands doesn't match. Run command \"task-cli --help\" to learn how to use it.")  
            
    except IndexError:
        print("Error: 1 or more argument is missing! Type main -h or main --help")
    except ValueError:
        print(f"Error: the argument {args[2]} should be an integer")