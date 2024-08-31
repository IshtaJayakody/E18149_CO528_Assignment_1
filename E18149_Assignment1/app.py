from flask import Flask, jsonify, request

app = Flask(__name__)

newspapers = [
    {'id': 1, 'title': 'Newspaper-1', 'owner': 'ishta', 'entries': [
        {'id': 1, 'content': 'first part', 'date': '2024-08-29'},
        {'id': 2, 'content': 'second part', 'date': '2024-08-30'}
    ]},
]

def get_newspaper_by_id(newspaper_id):
    for newspaper in newspapers:
        if newspaper['id'] == newspaper_id:
            return newspaper
    return None

def get_entry_by_id(newspaper_id, entry_id):
    newspaper = get_newspaper_by_id(newspaper_id)
    if newspaper:
        for entry in newspaper['entries']:
            if entry['id'] == entry_id:
                return entry
    return None

# Newspaper endpoints
@app.route('/newspapers', methods=['GET'])
def get_newspapers():
    # Assuming authentication is in place to get the current user
    user_newspapers = [newspaper for newspaper in newspapers] 
    return jsonify({'newspapers': user_newspapers})

@app.route('/newspapers/<int:newspaper_id>', methods=['GET'])
def get_newspaper(newspaper_id):
    newspaper = get_newspaper_by_id(newspaper_id)
    if not newspaper:
        return jsonify({'error': 'Newspaper not found'}), 404
    return jsonify({'newspaper': newspaper})

@app.route('/newspapers', methods=['POST'])
def create_newspaper():
    newspaper = {
        'id': max(newspaper['id'] for newspaper in newspapers) + 1,
        'title': request.json['title'],
        'owner': request.json['owner'], 
        'entries': []
    }
    newspapers.append(newspaper)
    return jsonify({'newspaper': newspaper}), 201

@app.route('/newspapers/<int:newspaper_id>', methods=['PUT'])
def update_newspaper(newspaper_id):
    newspaper = get_newspaper_by_id(newspaper_id)
    if not newspaper:
        return jsonify({'error': 'Newspaper not found'}), 404
    newspaper['title'] = request.json.get('title', newspaper['title'])
    return jsonify({'newspaper': newspaper})

@app.route('/newspapers/<int:newspaper_id>', methods=['DELETE'])
def delete_newspaper(newspaper_id):
    newspaper = get_newspaper_by_id(newspaper_id)
    if not newspaper:
        return jsonify({'error': 'Newspaper not found'}), 404
    newspapers.remove(newspaper)
    return jsonify({'message': 'Newspaper deleted'})

# Newspaper Entry endpoints
@app.route('/newspapers/<int:newspaper_id>/entries', methods=['GET'])
def get_entries(newspaper_id):
    newspaper = get_newspaper_by_id(newspaper_id)
    if not newspaper:
        return jsonify({'error': 'Newspaper not found'}), 404
    return jsonify({'entries': newspaper['entries']})

@app.route('/newspapers/<int:newspaper_id>/entries', methods=['POST'])
def create_entry(newspaper_id):
    newspaper = get_newspaper_by_id(newspaper_id)
    if not newspaper:
        return jsonify({'error': 'Newspaper not found'}), 404
    entry = {
        'id': max(entry['id'] for entry in newspaper['entries']) + 1 if newspaper['entries'] else 1,
        'content': request.json['content'],
        'date': request.json['date']
    }
    newspaper['entries'].append(entry)
    return jsonify({'entry': entry}), 201

@app.route('/newspapers/<int:newspaper_id>/entries/<int:entry_id>', methods=['PUT'])
def update_entry(newspaper_id, entry_id):
    entry = get_entry_by_id(newspaper_id, entry_id)
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)