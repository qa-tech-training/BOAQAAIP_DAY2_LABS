#! venv/bin/python3
import requests
from requests.auth import HTTPDigestAuth

base_url = 'http://localhost:5000'
auth = HTTPDigestAuth('learner', 'p@ssword')
token = requests.post(base_url + '/auth/tokens', auth=auth)
auth_header = {"Authorization": f"Bearer {token.text}"}

# Some sample book objects to populate the API server with. 
# Titles generated using Reedsy's book title generator: https://blog.reedsy.com/book-title-generator
books = [
    {
        "id": "0000012345",
        "title": "2132: Evolution",
        "genre": "sci-fi"
    },
    {
        "id": "0000012346",
        "title": "The Killer in the Fog",
        "genre": "thriller"
    },
    {
        "id": "0000012347",
        "title": "Point of Fear",
        "genre": "horror"
    },
    {
        "id": "0000012348",
        "title": "Blade of Grace",
        "genre": "fantasy"
    },
    {
        "id": "0000012349",
        "title": "The Sun of Earth That Was",
        "genre": "sci-fi"
    },
    {
        "id": "0000012350",
        "title": "Spell and the Shadow",
        "genre": "fantasy"
    }
]

for book in books:
    requests.post(base_url + '/api/books', json=book, headers=auth_header)
    print(f"added new book: {book}")