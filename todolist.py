from flask import Flask, render_template, redirect, request, url_for
import requests
import os
from googletrans import Translator

app = Flask(__name__)
TODO_API_URL = os.getenv("TODO_API_URL", "http://34.135.80.40:5001")
translator = Translator()

@app.route("/")
def show_list():
    lang = request.args.get('lang', None)

    resp = requests.get(f"{TODO_API_URL}/api/items")
    tdlist = resp.json()

    if lang:
        for item in tdlist:
            item['what_to_do'] = translator.translate(item['what_to_do'], dest=lang).text

    return render_template('index.html',
                           todolist=tdlist,
                           current_lang=lang or '')

@app.route("/add", methods=['POST'])
def add_entry():
    requests.post(f"{TODO_API_URL}/api/items", json={
        "what_to_do": request.form['what_to_do'],
        "due_date": request.form['due_date']
    })
    return redirect(url_for('show_list', lang=request.form.get('lang', '')))

@app.route("/delete/<item>")
def delete_entry(item):
    item = requests.utils.requote_uri(item)
    requests.delete(f"{TODO_API_URL}/api/items/{item}")
    return redirect(url_for('show_list', lang=request.args.get('lang', '')))

@app.route("/mark/<item>")
def mark_as_done(item):
    item = requests.utils.requote_uri(item)
    requests.put(f"{TODO_API_URL}/api/items/{item}")
    return redirect(url_for('show_list', lang=request.args.get('lang', '')))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5002)
