import pytest
import json
from datetime import datetime
from operations import (
    search_by_desc,
    search_by_id,
    add_task,
    update_task,
    delete_task,
    mark_in_progress,
    mark_done
)

@pytest.fixture
def sample_data():
    return [
        {
            "id": 1,
            "description": "cook pizza",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        },
        {
            "id": 2,
            "description": "read a book",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]

def test_search_by_desc(sample_data):
    assert search_by_desc("cook pizza", sample_data)
    assert not search_by_desc("cook", sample_data)

def test_search_by_id(sample_data):
    assert search_by_id(1, sample_data) == 0
    assert search_by_id(3, sample_data) == -1
    assert search_by_id(2, sample_data) == 1

def test_add_task_sucess(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/"db.json"
    db_file.write_text("[]")
    
    monkeypatch.setattr("operations.search_by_desc", lambda desc, data: False)

    fixed_time = datetime(2026, 1, 29, 12, 0, 0)
    monkeypatch.setattr("operations.datetime", type("MockDatetime", (), {"now": lambda: fixed_time}))

    add_task("task test")
    captured_output = capsys.readouterr()

    assert "Task added successfully (ID: 1)" in captured_output.out

    data = json.loads(db_file.read_text())
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["description"] == "task test"
    assert data[0]["status"] == "todo"
    assert data[0]["createdAt"] == "2026/01/29 12:00:00"
    assert data[0]["updatedAt"] is None

def test_add_task_already_exist(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/"db.json"
    db_file.write_text("[]")

    monkeypatch.setattr(
        "operations.search_by_desc", 
        lambda desc, data: True
        )
    data = json.loads(db_file.read_text())
    assert data == []

def test_update_task_sucess(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/"db.json"
    db_file.write_text(json.dumps([{
            "id": 1,
            "description": "cook pizza",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }]))

    monkeypatch.setattr(
        "operations.search_by_id", 
        lambda id, data: 0
    )

    monkeypatch.setattr(
        "operations.search_by_desc",
        lambda desc, data: False
    )
    monkeypatch.chdir(tmp_path)
    update_task(1, "cook ndole")
    data = json.loads(db_file.read_text())
    assert data[0]["description"] == "cook ndole"
    assert data[0]['updatedAt']
    
    

def test_update_task_id_not_exist(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/"db.json"
    db_file.write_text(json.dumps([{
            "id": 1,
            "description": "cook pizza",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }]))
    
    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: -1
    )

    update_task(2, "cook ndole")

    capture_output = capsys.readouterr()
    assert capture_output.out[:-1] == "Task Id: 2 doesn't exists!"

def test_update_task_description_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/"db.json"
    db_file.write_text(json.dumps([{
            "id": 1,
            "description": "cook pizza",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }]))
    
    monkeypatch.setattr(
        "operations.search_by_desc",
        lambda desc, data: True
    )

    update_task(1, "cook pizza")

    capture_output = capsys.readouterr()
    assert capture_output.out[:-1] == "Task: cook pizza already exist!"

def test_delete_task_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([
        {
            "id": 1,
            "description": "cook pizza",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]))

    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: 0
    )

    delete_task(1)
    data = json.loads(db_file.read_text())
    assert not data

def test_delete_task_file_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text('[]')

    delete_task(1)
    captured_output = capsys.readouterr()
    assert "File is empty or not found!" in captured_output.out

def test_delete_task_id_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([
        {
            "id": 1,
            "description": "cook pizza",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]))
    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: -1
    )

    delete_task(2)
    captured_output = capsys.readouterr()
    assert "Task id 2 does not exist!" in captured_output.out

def test_mark_in_progress_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([
        {
            "id": 1,
            "description": "cook pizza",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]))

    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: 0
    )
    mark_in_progress(1)
    data = json.loads(db_file.read_text())
    assert data[0]['status'] == "in-progress"
    assert data[0]['updatedAt']

def test_mark_in_progress_file_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([]))

    mark_in_progress(1)
    captured_output = capsys.readouterr()
    assert "File is empty or not found!" in captured_output.out

def test_mark_in_progress_id_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([
        {
            "id": 1,
            "description": "cook pizza",
            "status": "todo",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]))
    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: -1
    )

    mark_in_progress(2)
    captured_output = capsys.readouterr()
    assert "Task id 2 does not exist!" in captured_output.out

def test_mark_in_progress_already_in_progress(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([
        {
            "id": 1,
            "description": "cook pizza",
            "status": "in-progress",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]))
    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: 0
    )

    mark_in_progress(1)
    captured_output = capsys.readouterr()
    assert "Task 1 already in progress!" in captured_output.out

def test_mark_done_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([
        {
            "id": 1,
            "description": "cook pizza",
            "status": "in-progress",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]))

    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: 0
    )
    mark_done(1)
    data = json.loads(db_file.read_text())
    assert data[0]['status'] == "done"
    assert data[0]['updatedAt']

def test_mark_done_file_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([]))

    mark_done(1)
    captured_output = capsys.readouterr()
    assert "File is empty or not found!" in captured_output.out

def test_mark_done_id_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([
        {
            "id": 1,
            "description": "cook pizza",
            "status": "in-progress",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]))
    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: -1
    )

    mark_done(2)
    captured_output = capsys.readouterr()
    assert "Task id 2 does not exist!" in captured_output.out

def test_mark_done_already_done(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    db_file = tmp_path/'db.json'
    db_file.write_text(json.dumps([
        {
            "id": 1,
            "description": "cook pizza",
            "status": "done",
            "createdAt": datetime.now().replace(microsecond=0).strftime("%Y/%m/%d %H:%M:%S"),
            "updatedAt": None,
        }
    ]))
    monkeypatch.setattr(
        "operations.search_by_id",
        lambda id, data: 0
    )

    mark_done(1)
    captured_output = capsys.readouterr()
    assert "Task 1 already done!" in captured_output.out

