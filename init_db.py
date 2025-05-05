import sqlite3

def init_db():
    with sqlite3.connect('todolist.db') as db:
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
    print("Rebuilt todolist.db with category column.")

if __name__ == '__main__':
    init_db()