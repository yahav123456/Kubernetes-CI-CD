import pytest
from flask import url_for
from app import create_app
from pymongo import MongoClient, errors
import os
import time

@pytest.fixture
def app():
    app = create_app()
    app.config['MONGO_URI'] = os.getenv('MONGO_URL', 'mongodb://root:mongoDB@mongodb:27017/mymongodb?authSource=admin')
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'  # Add SERVER_NAME configuration
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    mongo_uri = app.config['MONGO_URI']
    for _ in range(5):  # Try 5 times to connect with a delay
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            client.server_info()  # Force connection
            db = client.get_database('mymongodb')
            print("Databases before insertion:")
            print(client.list_database_names())
            yield db
            print("Databases after insertion:")
            print(client.list_database_names())
            return
        except errors.ServerSelectionTimeoutError as err:
            print(f"Connection failed, retrying... ({err})")
            time.sleep(2)
    raise Exception("Failed to connect to MongoDB")

def test_uncompleted_tasks(app, client, init_db):
    with app.app_context():
        response = client.get(url_for('tasks'))
        assert response.status_code == 200
        assert "TODO Reminder with Flask and MongoDB" in response.data.decode()

def test_add_task(app, client, init_db):
    with app.app_context():
        task_data = {
            "name": "Test Task",
            "desc": "Test Description",
            "date": "2024-06-30",
            "pr": "High",
            "assignee": "Tester"
        }
        response = client.post(url_for('action'), data=task_data)
        assert response.status_code == 302

        response = client.get(url_for('lists'))
        assert response.status_code == 200
        assert "Test Task" in response.data.decode()

def test_complete_task(app, client, init_db):
    with app.app_context():
        task_data = {
            "name": "Complete Task",
            "desc": "Complete Description",
            "date": "2024-07-01",
            "pr": "Medium",
            "assignee": "Tester"
        }
        client.post(url_for('action'), data=task_data)

        # Print the database names and collections for debugging
        print("Debug: Listing databases after adding task:")
        print(init_db.client.list_database_names())

        print("Debug: Listing collections in 'mymongodb':")
        print(init_db.list_collection_names())

        task = init_db.todo.find_one({"name": "Complete Task"})
        print(f"Debug: Task found in DB: {task}")
        assert task is not None

        client.get(url_for('done', _id=task['_id']))
        task = init_db.todo.find_one({"_id": task['_id']})
        assert task['done'] == "yes"

def test_remove_task(app, client, init_db):
    with app.app_context():
        task_data = {
            "name": "Remove Task",
            "desc": "Remove Description",
            "date": "2024-07-02",
            "pr": "Low",
            "assignee": "Tester"
        }
        client.post(url_for('action'), data=task_data)
        task = init_db.todo.find_one({"name": "Remove Task"})
        assert task is not None

        client.get(url_for('remove', _id=task['_id']))
        task = init_db.todo.find_one({"name": "Remove Task"})
        assert task is None

def test_update_task(app, client, init_db):
    with app.app_context():
        task_data = {
            "name": "Update Task",
            "desc": "Update Description",
            "date": "2024-07-03",
            "pr": "High",
            "assignee": "Tester"
        }
        client.post(url_for('action'), data=task_data)
        task = init_db.todo.find_one({"name": "Update Task"})
        assert task is not None

        update_data = {
            "name": "Updated Task",
            "desc": "Updated Description",
            "date": "2024-07-03",
            "pr": "High",
            "assignee": "Tester",
            "_id": str(task['_id'])
        }
        client.post(url_for('action3'), data=update_data)
        updated_task = init_db.todo.find_one({"_id": task['_id']})
        assert updated_task['name'] == "Updated Task"
        assert updated_task['desc'] == "Updated Description"

def test_search_task(app, client, init_db):
    with app.app_context():
        task_data = {
            "name": "Search Task",
            "desc": "Search Description",
            "date": "2024-07-04",
            "pr": "Low",
            "assignee": "Tester"
        }
        client.post(url_for('action'), data=task_data)

        response = client.get(url_for('search'), query_string={"key": "Search Task", "refer": "name"})
        assert response.status_code == 200
        assert "Search Task" in response.data.decode()

def test_drop_database(init_db):
    print("Debug: Dropping the 'mymongodb' database")
    init_db.client.drop_database('mymongodb')
    remaining_dbs = init_db.client.list_database_names()
    print(f"Remaining databases: {remaining_dbs}")
    assert 'mymongodb' not in remaining_dbs
