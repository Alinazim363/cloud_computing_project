from flask import Flask, render_template, redirect, request, url_for
import requests
import os
from googletrans import Translator

app = Flask(__name__)
TODO_API_URL = os.getenv('TODO_API_URL', 'http://34.28.88.161:5001')
translator = Translator()


@app.route('/')
def show_list():
    lang = request.args.get('lang', None)
    cat_filter = request.args.get('category', '')

    resp = requests.get(f"{TODO_API_URL}/api/items")
    tdlist = resp.json()
    if cat_filter:
        tdlist = [i for i in tdlist if i['category']==cat_filter]

    if lang:
        for item in tdlist:
            item['what_to_do'] = translator.translate(item['what_to_do'], dest=lang).text
            if item.get('due_date'):
                item['due_date'] = translator.translate(item['due_date'], dest=lang).text
            if item.get('category'):
                item['category'] = translator.translate(item['category'], dest=lang).text

    # static labels
    static_labels = {
        'heading':       'oh, so many things to do...',
        'mark_button':   'mark as done',
        'delete_button': 'delete',
        'add_item':      'add a new item',
        'cancel_entry':  'cancel the new entry',
        'what_label':    'what to do:',
        'when_label':    'when:',
        'category_label':'category:',
        'save_button':   'save the new item',
        'empty_message':'Unbelievable. Nothing to do for now.',
        'filter_label':  'Filter by category:'
    }
    if lang:
        for k,v in static_labels.items():
            static_labels[k] = translator.translate(v, dest=lang).text

    return render_template(
        'index.html',
        todolist=tdlist,
        current_lang=lang or '',
        current_cat=cat_filter,
        static_labels=static_labels
    )


@app.route('/add', methods=['POST'])
def add_entry():
    lang = request.form.get('lang','')
    category = request.form['category']
    requests.post(f"{TODO_API_URL}/api/items", json={
        'what_to_do': request.form['what_to_do'],
        'due_date': request.form['due_date'],
        'category': category
    })
    return redirect(url_for('show_list', lang=lang, category=category))


@app.route('/delete/<int:item_id>')
def delete_entry(item_id):
    lang = request.args.get('lang','')
    cat  = request.args.get('category','')
    requests.delete(f"{TODO_API_URL}/api/items/{item_id}")
    return redirect(url_for('show_list', lang=lang, category=cat))


@app.route('/mark/<int:item_id>')
def mark_as_done(item_id):
    lang = request.args.get('lang','')
    cat  = request.args.get('category','')
    requests.put(f"{TODO_API_URL}/api/items/{item_id}")
    return redirect(url_for('show_list', lang=lang, category=cat))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002)