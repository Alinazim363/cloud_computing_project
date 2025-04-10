from flask import Flask, render_template, redirect, g, request, url_for, jsonify, json
import urllib
import requests
import os

app = Flask(__name__)
TODO_API_URL = os.getenv("TODO_API_URL", "http://34.135.80.40:5001")



@app.route("/")
def show_list():
    resp = requests.get(TODO_API_URL+"/api/items")
    resp = resp.json()
    return render_template('index.html', todolist=resp)


@app.route("/add", methods=['POST'])
def add_entry():
    requests.post(TODO_API_URL+"/api/items", json={
                  "what_to_do": request.form['what_to_do'], "due_date": request.form['due_date']})
    return redirect(url_for('show_list'))


@app.route("/delete/<item>")
def delete_entry(item):
    item = urllib.parse.quote(item) 
    url = TODO_API_URL + "/api/items/" + item
    requests.delete(url)
    return redirect(url_for('show_list'))


@app.route("/mark/<item>")
def mark_as_done(item):
    url = TODO_API_URL + "/api/items/" + item
    requests.put(url)
    return redirect(url_for('show_list'))


if __name__ == "__main__":
    app.run("0.0.0.0", port = 5002)
