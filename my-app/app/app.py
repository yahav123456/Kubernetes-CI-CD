from flask import Flask, render_template, request, redirect, url_for, jsonify
from bson import ObjectId
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    title = "TODO sample application with Flask and MongoDB"
    heading = "TODO Reminder with Flask and MongoDB"

    mongo_url = os.getenv("MONGO_URL", "mongodb://root:mongoDB@host.docker.internal:31728/mymongodb?authSource=admin")
    client = MongoClient(mongo_url)
    db = client.mymongodb  # Select the database
    todos = db.todo  # Select the collection name

    def redirect_url():
        return request.args.get('next') or request.referrer or url_for('lists')
        
    @app.route("/list")
    def lists():
        todos_l = todos.find()
        a1 = "active"
        return render_template('index.html', a1=a1, todos=todos_l, t=title, h=heading)

    @app.route("/")
    @app.route("/uncompleted")
    def tasks():
        todos_l = todos.find({"done": "no"})
        a2 = "active"
        return render_template('index.html', a2=a2, todos=todos_l, t=title, h=heading)

    @app.route("/completed")
    def completed():
        todos_l = todos.find({"done": "yes"})
        a3 = "active"
        return render_template('index.html', a3=a3, todos=todos_l, t=title, h=heading)

    @app.route("/done")
    def done():
        id = request.values.get("_id")
        print(f"Received ID: {id}")
        try:
            task = todos.find_one({"_id": ObjectId(id)})
            print(f"Task found: {task}")
            if task and task["done"] == "yes":
                todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": "no"}})
            else:
                todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": "yes"}})
            updated_task = todos.find_one({"_id": ObjectId(id)})
            print(f"Updated task: {updated_task}")
            return redirect(redirect_url())
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/action", methods=['POST'])
    def action():
        name = request.values.get("name")
        desc = request.values.get("desc")
        date = request.values.get("date")
        pr = request.values.get("pr")
        assignee = request.values.get("assignee")
        todos.insert_one({"name": name, "desc": desc, "date": date, "pr": pr, "assignee": assignee, "done": "no"})
        return redirect("/list")

    @app.route("/remove")
    def remove():
        key = request.values.get("_id")
        todos.delete_one({"_id": ObjectId(key)})
        return redirect("/")

    @app.route("/update")
    def update():
        id = request.values.get("_id")
        task = todos.find_one({"_id": ObjectId(id)})
        return render_template('update.html', tasks=task, h=heading, t=title)

    @app.route("/action3", methods=['POST'])
    def action3():
        name = request.values.get("name")
        desc = request.values.get("desc")
        date = request.values.get("date")
        pr = request.values.get("pr")
        assignee = request.values.get("assignee")
        id = request.values.get("_id")
        todos.update_one({"_id": ObjectId(id)}, {'$set': {"name": name, "desc": desc, "date": date, "pr": pr, "assignee": assignee}})
        return redirect("/")

    @app.route("/search", methods=['GET'])
    def search():
        key = request.values.get("key")
        refer = request.values.get("refer")
        if key == "_id":
            todos_l = todos.find({refer: ObjectId(key)})
        else:
            todos_l = todos.find({refer: key})
        return render_template('searchlist.html', todos=todos_l, t=title, h=heading)

    @app.route("/collections")
    def collections():
        collections = db.list_collection_names()
        return render_template('collections.html', collections=collections, t=title, h=heading)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
