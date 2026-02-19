from flask import Flask, request, jsonify, render_template, redirect
import os
import sqlite3
import tempfile
from flask import send_file

import db
import importer
import categorizer
import sync
import excel

DB_PATH = os.environ.get('LITE_DB', 'lite.db')
app = Flask(__name__)


# Root route redirects to UI
@app.route('/')
def index():
    return redirect('/ui')


@app.route('/init', methods=['POST'])
def init_route():
    db.init_db(DB_PATH)
    return jsonify({'status': 'ok', 'db': DB_PATH})


@app.route('/import', methods=['POST'])
def import_route():
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'no file uploaded'}), 400
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    f.save(tmp.name)
    count = importer.import_csv(tmp.name, db_path=DB_PATH)
    os.unlink(tmp.name)
    return jsonify({'imported': count})


@app.route('/transactions', methods=['GET'])
def list_route():
    rows = db.list_transactions(DB_PATH)
    result = []
    for id_, date, desc, amt, cat in rows:
        result.append({'id': id_, 'date': date, 'description': desc, 'amount': amt, 'category': cat})
    return jsonify(result)


@app.route('/categorize', methods=['POST'])
def categorize_route():
    updated = categorizer.categorize_all(db_path=DB_PATH)
    return jsonify({'updated': updated})


@app.route('/sync/upload', methods=['POST'])
def sync_upload_route():
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'no file uploaded'}), 400
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    f.save(tmp.name)
    tmp.close()
    result = sync.merge_xlsx(tmp.name, db_path=DB_PATH)
    os.unlink(tmp.name)
    return jsonify(result)


@app.route('/sync/pull', methods=['GET'])
def sync_pull_route():
    fmt = request.args.get('format', 'json')
    if fmt == 'xlsx':
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        excel.export_xlsx(tmp.name, db_path=DB_PATH)
        return send_file(tmp.name, as_attachment=True, download_name='transactions.xlsx')
    # default JSON
    rows = db.get_all_transactions(db_path=DB_PATH)
    result = []
    for id_, date, desc, amt, cat, ext in rows:
        result.append({'id': id_, 'date': date, 'description': desc, 'amount': amt, 'category': cat, 'external_id': ext})
    return jsonify(result)


@app.route('/ui', methods=['GET'])
def ui_route():
    # simple bulk edit UI served from templates/bulk_edit.html
    return render_template('bulk_edit.html')


@app.route('/api/transactions', methods=['GET'])
def api_transactions():
    rows = db.get_all_transactions(db_path=DB_PATH)
    result = []
    for id_, date, desc, amt, cat, ext in rows:
        result.append({'id': id_, 'date': date, 'description': desc, 'amount': amt, 'category': cat, 'external_id': ext})
    return jsonify(result)


@app.route('/api/apply_bulk', methods=['POST'])
def api_apply_bulk():
    data = request.get_json() or {}
    updates = data.get('updates', [])
    applied = 0
    for u in updates:
        try:
            tx_id = int(u.get('id'))
            cat = u.get('category')
            if cat is None:
                continue
            db.update_category(tx_id, cat, db_path=DB_PATH)
            applied += 1
        except Exception:
            continue
    return jsonify({'applied': applied, 'requested': len(updates)})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
