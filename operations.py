import json
from datetime import datetime
from pathlib import Path
from textwrap import wrap

def search_by_desc(description: str, data: list) -> bool:
    for dic in data:
        if dic["description"] == description:
            return True
    return False

def search_by_id(id: int, data: list) -> int:
    for i in range(len(data)):
        if data[i]["id"] == id:
            return i
    return -1

def add_task(description: str):
    """ This function adds a new task.
    - The task is created by giving its description.
    - The default status is todo. """
    try:
        with open('db.json', 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        with open('db.json', 'w+') as file:
            json.dump([], file)
            data = json.load(file)
    
    # Check if the task exists
    if search_by_desc(description, data):
        return False
    id = len(data) + 1
    data.append({
        "id": id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
        "updatedAt": None,
    })
    try:
        with open('db.json', 'w') as file:
            json.dump(data, file, indent=4)
            print(f"Task added successfully (ID: {id})")
    except Exception as e:
        print(f"An error occurs! {e}")
    return True

def update_task(id: int, description: str) -> None:
    file_path = "db.json"
    p = Path(file_path)
    if p.exists():
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        print(f"file: {file_path} doesn't exist!")
    index = search_by_id(id, data)
    if index == -1:
        print(f"Task Id: {id} doesn't exists!")
    else:
        if search_by_desc(description, data):
            print(f"Task: {description} already exist!")
        else:
            data[index]["description"] = description
            data[index]["updatedAt"] = datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S")
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

def delete_task(id: int):
    data = []
    with open("db.json", 'r') as file:
        data = json.load(file)
    
    if not data:
        print("File is empty or not found!")
    else:
        index = search_by_id(id, data)
        if index == -1:
            print(f"Task id {id} does not exist!")
        else:
            del data[index]
            with open('db.json', 'w') as file:
                json.dump(data, file, indent=4)

def mark_in_progress(id: int):
    data = []
    with open('db.json', 'r') as file:
        data = json.load(file)
    if not data:
        print("File is empty or not found!")
    else:
        index = search_by_id(id, data)
        if index == -1:
            print(f"Task id {id} does not exist!")
        elif data[index]["status"] == "in-progress":
            print(f"Task {id} already in progress!")
        else:
            data[index]["status"] = "in-progress"
            data[index]["updatedAt"] = datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S")
            with open('db.json', 'w') as file:
                json.dump(data, file, indent=4)

def mark_done(id: int):
    data = []
    with open('db.json', 'r') as file:
        data = json.load(file)
    if not data:
        print("File is empty or not found!")
    else:
        index = search_by_id(id, data)
        if index == -1:
            print(f"Task id {id} does not exist!")
        elif data[index]["status"] == "done":
            print(f"Task {id} already done!")
        else:
            data[index]["status"] = "done"
            data[index]["updatedAt"] = datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S")
            with open('db.json', 'w') as file:
                json.dump(data, file, indent=4)

def list_task(key: str=None):
    data = []
    with open('db.json', 'r') as file:
        data = json.load(file)
    if not data:
        print("File is empty or not found!")
    
    print("-" * 81)
    headers = ["id", "description", "status", "createdAt", "updatedAt"]
    print(f"| {headers[0]:<2} | {headers[1]:<15} | {headers[2]:<10} | {headers[3]:<19} | {headers[4]:<19} |")
    print("-" * 81)
    
    if not key:
        for task in data:
            print(f"| {task['id']:<2} | {task["description"]:<15} | {task["status"]:<10} | {task["createdAt"]:<19} | {str(task["updatedAt"]):<19} |")
    else:
        for task in data:
            if key.lower() == task["status"]:
                print(f"| {task['id']:<2} | {task["description"]:<15} | {task["status"]:<10} | {task["createdAt"]:<19} | {str(task["updatedAt"]):<19} |")

