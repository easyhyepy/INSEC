from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

db = MongoClient('mongodb://localhost:27017')['threads']
                
@app.route('/discussion/thread', methods=['GET'])
def get_thread_with_replies():
    data = json.loads(request.data)
    thread = db.threads.find_one({'_id': data['_id']})

    if not thread:
        return jsonify({'error': 'Thread not found'}), 404

    # Fetch the first 3 replies
    replies = list(db.replies.find({'thread_id': thread['_id']}).sort('date', 1).limit(3))

    thread_details = {
        'title': thread['title'],
        'initial_post': thread['initial_post'],
        'replies': [{'author_id': reply['author_id'], 'content': reply['content']} for reply in replies]
    }
    
    return jsonify(thread_details), 200