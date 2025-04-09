# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask, render_template, redirect, g, request, url_for, jsonify, json
import urllib
import requests  # similar purpose to urllib.request, just more convenience
import os

app = Flask(__name__)
# make sure to replace localhost with the actual IP of the backend service after you deploy the backend service on Google Cloud
# for example, like this: TODO_API_URL = "http://123.456.789.123:5001"
TODO_API_URL = os.getenv("TODO_API_URL", "http://34.135.80.40:5001")



@app.route("/")
def show_list(): # this is the counterpart of show_list() from homework 3
    resp = requests.get(TODO_API_URL+"/api/items")
    resp = resp.json()
    return render_template('index.html', todolist=resp)


@app.route("/add", methods=['POST'])
def add_entry(): # this is the counterpart of add_entry() from homework 3
    requests.post(TODO_API_URL+"/api/items", json={
                  "what_to_do": request.form['what_to_do'], "due_date": request.form['due_date']})
    return redirect(url_for('show_list'))


@app.route("/delete/<item>")
def delete_entry(item): # this is the counterpart of delete_entry(...) from homework 3
    item = urllib.parse.quote(item) # this takes care of spaces in the item
    # Since URL quotes are already handled in the API service code, you can pass the item directly.
    url = TODO_API_URL + "/api/items/" + item
    requests.delete(url)
    return redirect(url_for('show_list'))


@app.route("/mark/<item>")
def mark_as_done(item):
    url = TODO_API_URL + "/api/items/" + item
    # The PUT request will update the status in the API service.
    requests.put(url)
    return redirect(url_for('show_list'))



if __name__ == "__main__":
    app.run("0.0.0.0", port = 5002)
