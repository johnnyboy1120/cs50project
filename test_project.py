import pytest
from datetime import datetime
from project import tasks, completed, add_task, complete_task, show_tasks, view_completed

# Fixture to clear tasks before each test
@pytest.fixture(autouse=True)
def clear_tasks():
    tasks.clear()
    completed.clear()

def test_add_task(monkeypatch):
    inputs = iter(["Test Task", "30 minutes", "2", "12/31", "y"])  # Added "y" to return to menu
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    add_task()

    assert len(tasks) == 1
    assert tasks[0]['description'] == "Test Task"
    assert tasks[0]['time'] == "30 minutes"
    assert tasks[0]['priority'] == 2
    assert tasks[0]['date'] == datetime(datetime.today().year, 12, 31).date()

def test_complete_task(monkeypatch):
    # First, add a task
    tasks.append({
        'description': 'Test Task',
        'time': '30 minutes',
        'priority': 2,
        'date': datetime(datetime.today().year, 12, 31).date(),
        'completed': 'no'
    })

    inputs = iter(["1", "y"])  # Added "y" to return to menu
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    complete_task()

    assert len(tasks) == 0
    assert len(completed) == 1
    assert completed[0]['description'] == "Test Task"
    assert completed[0]['completed'] == "yes"

def test_view_completed(monkeypatch, capsys):
    completed.append({
        'description': 'Completed Task',
        'time': '1 hour',
        'priority': 1,
        'date': '12/31 12:00pm',
        'completed': 'yes'
    })

    inputs = iter(["y"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    view_completed()

    captured = capsys.readouterr()
    assert "Completed Task" in captured.out
    assert "1 hour" in captured.out

def test_show_tasks(monkeypatch, capsys):
    tasks.append({
        'description': 'Test Task 1',
        'time': '30 minutes',
        'priority': 2,
        'date': datetime(datetime.today().year, 12, 31).date(),
        'completed': 'no'
    })

    show_tasks()

    captured = capsys.readouterr()
    assert "Test Task 1" in captured.out
    assert "30 minutes" in captured.out
