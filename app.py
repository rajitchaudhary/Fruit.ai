from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



# MongoDB Atlas connection string (replace with your URI)
app.config["MONGO_URI"] = "mongodb+srv://rajitchaudhary34:rajit@fruit.yd8ce.mongodb.net/faqs_db?retryWrites=true&w=majority"

# Initialize PyMongo
mongo = PyMongo(app)

# Define routes
@app.route('/')
def index():
    return "Welcome to the FAQ API"

# GET all FAQs
@app.route('/faqs', methods=['GET'])
def get_faqs():
    faqs = mongo.db.faqs.find()
    result = []
    for faq in faqs:
        result.append({
            'id': str(faq['_id']),
            'title': faq['title'],
            'description': faq['description'],
            'image': faq.get('image'),
            'altText': faq.get('altText')
        })
    return jsonify(result)

# GET a single FAQ
@app.route('/faqs/<id>', methods=['GET'])
def get_faq(id):
    faq = mongo.db.faqs.find_one({'_id': ObjectId(id)})
    if faq:
        return jsonify({
            'id': str(faq['_id']),
            'title': faq['title'],
            'description': faq['description'],
            'image': faq.get('image'),
            'altText': faq.get('altText')
        })
    else:
        return jsonify({'error': 'FAQ not found'}), 404

# POST a new FAQ
@app.route('/faqs', methods=['POST'])
def add_faq():
    data = request.get_json()
    result = mongo.db.faqs.insert_one({
        'title': data.get('title'),
        'description': data.get('description'),
        'image': data.get('image'),
        'altText': data.get('altText')
    })
    return jsonify({'id': str(result.inserted_id)}), 201

# PUT (Update) an existing FAQ
@app.route('/faqs/<id>', methods=['PUT'])
def update_faq(id):
    data = request.get_json()
    result = mongo.db.faqs.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'title': data.get('title'),
            'description': data.get('description'),
            'image': data.get('image'),
            'altText': data.get('altText')
        }}
    )
    if result.matched_count:
        return jsonify({'message': 'FAQ updated successfully'})
    else:
        return jsonify({'error': 'FAQ not found'}), 404

# DELETE an FAQ
@app.route('/faqs/<id>', methods=['DELETE'])
def delete_faq(id):
    result = mongo.db.faqs.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'FAQ deleted successfully'})
    else:
        return jsonify({'error': 'FAQ not found'}), 404

if _name_ == '_main_':
        port = int(os.environ.get('PORT', 5000))
            app.run(host='0.0.0.0', port=port, debug=True)