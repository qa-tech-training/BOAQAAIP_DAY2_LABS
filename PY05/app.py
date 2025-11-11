from flask import Flask, request, jsonify, Response
from secrets import token_hex, compare_digest
# import time
import hashlib
import re
import random

books = []
authors = []
reviews = []

users = {"learner":"p@ssword"}
valid_tokens = {user: [] for user in users.keys()}

app = Flask(__name__)

def is_valid_token(token):
    valid = False
    for ts in valid_tokens.values():
        for t in ts:
            if compare_digest(t, token):
                valid = True
                break
        if valid:
            break
    return valid

def validate_response(auth_params, method):
    nonce = auth_params.get('nonce', '')
    cnonce = auth_params.get('cnonce', '')
    nc = auth_params.get('nc', '')
    response = auth_params.get('response', '')
    user = auth_params.get('username', '')
    realm = auth_params.get('realm', '')
    opaque = auth_params.get('opaque', '')
    qop = auth_params.get('qop', '')
    password = users.get(user, '')
    path = auth_params.get('uri', '')
    ha1 = hashlib.md5(f'{user}:{realm}:{password}'.encode('utf-8')).hexdigest()
    ha2 = hashlib.md5(f'{method}:{path}'.encode('utf-8')).hexdigest()
    expected = hashlib.md5(f'{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}'.encode('utf-8')).hexdigest()
    return expected == response

@app.route('/auth/tokens', methods=['POST'])
def get_new_token():
    if not request.headers.get('Authorization', ''):
        nonce = token_hex(16)
        opaque = token_hex(16)
        return "Unauthorized", 401, {"WWW-Authenticate": f'Digest realm="example@api.com", nonce="{nonce}", opaque="{opaque}", qop="auth"'}
    reg = re.compile('([a-zA-Z0-9_]+)[=] ?"?([a-zA-Z0-9_@./]+)"?')
    auth_params = dict(reg.findall(request.headers.get("Authorization")))
    user = auth_params.get('username', '')
    if validate_response(auth_params, request.method):
        new_token = token_hex(32)
        valid_tokens[user].append(new_token)
        return Response(new_token, mimetype='text/plain')
    return f"Auth failure", 401

@app.route('/api/flaky', methods=['GET'])
def flaky():
    if random.randint(0, 10) > 5:
        return "Oopsie", 500, {"ERROR": "Bad luck"}
    return {"result": "success", "data": [1, 2, 3]}, 200

@app.route('/api/authors', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_authors():
    if request.method == 'GET':
        return jsonify(authors)
    else:
        request_token = request.headers.get("Authorization", "auth not defined").split(" ")[1]
        if not is_valid_token(request_token):
            return "Unauthorized", 401
        author_data = request.get_json()
        if request.method == 'POST':
            authors.append(author_data)
            return author_data
        elif request.method == 'PUT':
            for i, a in enumerate(authors):
                if a.get("id") == author_data["id"]:
                    authors[i] = author_data
                    break
            return author_data
        elif request.method == 'DELETE':
            for i, a in enumerate(authors):
                if a.get("id") == author_data["id"]:
                    del authors[i]
                    break
            return author_data
        else:
            return "Method Not Allowed", 405

@app.route('/api/books', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_books():
    if request.method == 'GET':
        return jsonify(books)
    else:
        request_token = request.headers.get("Authorization", "auth not defined").split(" ")[1]
        if not is_valid_token(request_token):
            return "Unauthorized", 401
        book_data = request.get_json()
        if request.method == 'POST':
            books.append(book_data)
            return book_data
        elif request.method == 'PUT':
            for i, b in enumerate(books):
                if b.get("id") == book_data["id"]:
                    books[i] = book_data
                    break
            return book_data
        elif request.method == 'DELETE':
            for i, b in enumerate(books):
                if b.get("id") == book_data["id"]:
                    del books[i]
                    break
            return book_data
        else:
            return "Method Not Allowed", 405
    
@app.route('/api/reviews', methods=['GET', 'POST'])
def handle_reviews():
    if request.method == 'GET':
        return jsonify(reviews)
    else:
        request_token = request.headers.get("Authorization", "auth not defined").split(" ")[1]
        if not is_valid_token(request_token):
            return "Unauthorized", 401
        review_data = request.get_json()
        if request.method == 'POST':
            reviews.append(review_data)
            return review_data
        elif request.method == 'PUT':
            for i, r in enumerate(reviews):
                if r.get("id") == review_data["id"]:
                    reviews[i] = review_data
                    break
            return review_data
        elif request.method == 'DELETE':
            for i, r in enumerate(reviews):
                if r.get("id") == review_data["id"]:
                    del reviews[i]
                    break
            return review_data
        else:
            return "Method Not Allowed", 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

