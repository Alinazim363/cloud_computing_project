# RESTful API with numeric IDs for stable delete/mark operations
from flask import Flask, g, request, jsonify, Response
import sqlite3
import json

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/api/items")  # GET all items
def get_items():
    db = get_db()
    cur = db.execute('SELECT id, what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [
        dict(id=row[0], what_to_do=row[1], due_date=row[2], status=row[3])
        for row in entries
    ]
    return jsonify(tdlist)


@app.route("/api/items", methods=['POST'])  # POST to add
def add_item():
    db = get_db()
    db.execute(
        'INSERT INTO entries (what_to_do, due_date) VALUES (?, ?)',
        [request.json['what_to_do'], request.json['due_date']]
    )
    db.commit()
    return jsonify({"result": True})


@app.route("/api/items/<int:item_id>", methods=['DELETE'])  # DELETE by ID
def delete_item(item_id):
    db = get_db()
    db.execute("DELETE FROM entries WHERE id=?", [item_id])
    db.commit()
    return jsonify({"result": True})


@app.route("/api/items/<int:item_id>", methods=['PUT'])  # PUT to mark done
def update_item(item_id):
    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE id=?", [item_id])
    db.commit()
    return jsonify({"result": True})


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)
