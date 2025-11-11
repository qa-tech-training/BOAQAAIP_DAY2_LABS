#! venv/bin/python3
import requests
from time import sleep

ids = [
    "0000012345",
    "0000012346",
    "0000012347",
    "0000012348",
    "0000012349",
    "0000012350"
]

def get_book(i, books):
    book = dict()
    for b in books:
        if b.get("id", '') == i:
            book = b
            break
    return book

def process_book_data(book):
    bookstr = ""
    bookstr += f"ID: {str(book.get('id', ''))}\n"
    bookstr += f"TITLE: {book.get('title', '')}\n"
    bookstr += f"GENRE: {book.get('genre', '')}\n"
    sleep(1)
    return bookstr

def main():
    books = requests.get('http://localhost:5000/api/books').json()
    for i in ids:
        book = get_book(i, books)
        print(process_book_data(book))

if __name__ == '__main__':
    main()

