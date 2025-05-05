from flask import Flask, g, request, jsonify
import sqlite3
import json

DATABASE = 'todolist.db'
app = Flask(__name__)
app.config.from_object(__name__)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/api/items")
def get_items():
    db = get_db()
    cur = db.execute(
        'SELECT id, what_to_do, due_date, status, category FROM entries'
    )
    entries = cur.fetchall()
    result = [
        dict(
            id=row[0],
            what_to_do=row[1],
            due_date=row[2],
            status=row[3],
            category=row[4]
        )
        for row in entries
    ]
    return jsonify(result)


@app.route("/api/items", methods=['POST'])
def add_item():
    data = request.json
    db = get_db()
    db.execute(
        'INSERT INTO entries (what_to_do, due_date, category) VALUES (?, ?, ?)',
        [data['what_to_do'], data['due_date'], data.get('category', 'miscellaneous')]
    )
    db.commit()
    return jsonify({"result": True})


@app.route("/api/items/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    db = get_db()
    db.execute('DELETE FROM entries WHERE id=?', [item_id])
    db.commit()
    return jsonify({"result": True})


@app.route("/api/items/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE id=?", [item_id])
    db.commit()
    return jsonify({"result": True})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001)