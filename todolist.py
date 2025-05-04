from flask import Flask, render_template, redirect, request, url_for
import requests
import os
from googletrans import Translator

app = Flask(__name__)
TODO_API_URL = os.getenv("TODO_API_URL", "http://34.29.150.16:5001")
translator = Translator()

@app.route("/")
def show_list():
    lang = request.args.get('lang', None)

    resp = requests.get(f"{TODO_API_URL}/api/items")
    tdlist = resp.json()

    if lang:
        for item in tdlist:
            item['what_to_do'] = translator.translate(item['what_to_do'], dest=lang).text

    # Static UI labels for translation
    static_labels = {
        'heading':       'oh, so many things to do...',
        'mark_button':   'mark as done',
        'delete_button': 'delete',
        'add_item':      'add a new item',
        'cancel_entry':  'cancel the new entry',
        'what_label':    'what to do:',
        'when_label':    'when:',
        'save_button':   'save the new item',
        'empty_message': 'Unbelievable. Nothing to do for now.'
    }
    if lang:
        for key, text in static_labels.items():
            static_labels[key] = translator.translate(text, dest=lang).text

    return render_template(
        'index.html',
        todolist=tdlist,
        current_lang=lang or '',
        static_labels=static_labels
    )

@app.route("/add", methods=['POST'])
def add_entry():
    lang = request.form.get('lang', '')
    requests.post(f"{TODO_API_URL}/api/items", json={
        "what_to_do": request.form['what_to_do'],
        "due_date":    request.form['due_date']
    })
    return redirect(url_for('show_list', lang=lang))

@app.route("/delete/<item>")
def delete_entry(item):
    lang = request.args.get('lang', '')
    item_enc = requests.utils.requote_uri(item)
    requests.delete(f"{TODO_API_URL}/api/items/{item_enc}")
    return redirect(url_for('show_list', lang=lang))

@app.route("/mark/<item>")
def mark_as_done(item):
    lang = request.args.get('lang', '')
    item_enc = requests.utils.requote_uri(item)
    requests.put(f"{TODO_API_URL}/api/items/{item_enc}")
    return redirect(url_for('show_list', lang=lang))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5002)
