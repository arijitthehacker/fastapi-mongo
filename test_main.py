import pytest
from pymongo import MongoClient
from app import app

# Test case 1: Create and insert post in the collection
def test_root():
    #app.config['TESTING'] = True
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test_database']
    coll = db.create_collection("sample")

    posts = {'name': 'Arijit', 'docs': 'sample'}
    post_id = coll.insert_one(posts).inserted_id

    assert post_id is not None, "Post ID should not be None"
    assert len(coll.find({'_id': post_id})) == 1, f'Expected only one document to be inserted'

    # Test error handling
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200, "Expect status code 200 for root endpoint"