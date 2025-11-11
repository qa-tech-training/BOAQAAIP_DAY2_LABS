# Python Flask Example API

## Setup
### Prerequisites
Python 3, Pip, Virtual Environment & Git need to be installed:
```bash
sudo apt update 
sudo apt install -y python3 python3-pip python3-venv git
```

### Launch
Install dependencies and run:
```bash
python3 -m venv venv
venv/bin/python3 -m pip install -r requirements.txt
venv/bin/python3 app.py &
```

## Routes
The API setup is running on port `5000` and has the following routes configured:

| Route | Description | Content Type|
|--|--|--|
|`/api/books`|Create,Read,Update,Delete Book objects|`application/json`|
|`/api/authors`|Create,Read,Update,Delete Author objects|`application/json`|
|`/api/reviews`|Create,Read,Update,Delete Review objects|`application/json`|
|`/auth/tokens`|Validate user digest auth credentials and return a bearer token if valid|`text/plain`|

