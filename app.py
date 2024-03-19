from flask import Flask, jsonify, request
from pymongo import MongoClient
import os


app = Flask(__name__)
mongodb_uri = os.environ.get("MONGODB_URI")
client = MongoClient(mongodb_uri)


db = client["Bookstore"]
collection = db["books"]


@app.route("/books", methods=["GET"])
def get_books():
    books = list(collection.find({}, {"_id": 0}))
    return jsonify({"books": books})

@app.route("/books/<isbn>", methods=["GET"])
def get_book(isbn):
    book = collection.find_one({"isbn": isbn}, {"_id": 0})
    return jsonify({"book": book})

@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.json
    collection.insert_one(new_book)
    return jsonify({"message": "Book added successfully"})


@app.route("/books/<isbn>", methods=["PUT"])
def update_book(isbn):
    updated_book = request.json
    collection.update_one({"isbn": isbn}, {"$set": updated_book})
    return jsonify({"message": "Book updated successfully"})

@app.route("/books/<isbn>", methods=["DELETE"])
def delete_book(isbn):
    collection.delete_one({"isbn": isbn})
    return jsonify({"message": "Book deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
