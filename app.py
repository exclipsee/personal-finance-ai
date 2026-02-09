from flask import Flask, request, jsonify
import os
import sqlite3
import tempfile

import db
import importer
import categorizer

DB_PATH = os.environ.get('LITE_DB', 'lite.db')
app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
