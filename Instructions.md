### Prerequisites
Clone this repository into your WSL home directory as Labs2:
```bash
cd ~
git clone https://github.com/qa-tech-training/BOAQAAIP_DAY2_LABS.git Labs2
```

### Lab PY05 - Interacting With APIs
#### Objective
Deploy a provided REST API, and create a python script to make authenticated requests to it

#### Outcomes
By the end of this lab, you will have:
* Deployed a Python Web API using *Flask*
* Used the *requests* library to make GET, POST, PUT and DELETE requests
* Utilised Bearer token and Digest authentication to interact with secure endpoints

#### High-Level Steps
- Install dependencies and deploy the API
- Create a script which can make HTTP GET requests to the API
- Implement client-side authentication to enable POST, PUT & DELETE requests

#### Detailed Steps
##### Launch the example API
1. On your classroom machine, ensure that _docker desktop_ is started.
2. Edit the docker desktop settings and check 'enable WSL integration'
3. Ensure you have an active VSCode session connected to WSL, and navigate to the lab directory:
```bash
cd ~/Labs2/PY05
```
4. Deploy the sample API using docker compose:
```bash
sudo docker compose -f compose.yml up -d --build
```

##### Make HTTP get requests
5. Open the api_requests.py file, and add the following content:
```python
#! venv/bin/python3
import requests

if __name__ == '__main__':
    books = requests.get('http://localhost:5000/api/books')
    print(books.json())
```
6. In the VSCode terminal, install requests in a new virtual environment and run your script:
```shell
python3 -m venv venv
venv/bin/pip3 install requests
./api_requests.py
```
7. Observe the response from the API - an empty list ([]), as there are currently no books

##### Make a POST request
8. In your api_requests script, add a post request to create a new book object:
```python
#! venv/bin/python3
import requests

if __name__ == '__main__':
    book = {"title": "Lorem Ipsum", "genre": "fantasy", "blurb": "Lorem ipsum, dolor sic amet..."} # add this line
    requests.post('http://localhost:5000/api/books', json=book) # and this line
    books = requests.get('http://localhost:5000/api/books')
    print(books.json())
```
9. Run your script again. Notice there are still no books even after the POST request. Amend your script to provide some debug information:
```python
#! venv/bin/python3
import requests

if __name__ == '__main__':
    book = {"id": "0000012345", "title": "Lorem Ipsum", "genre": "fantasy", "blurb": "Lorem ipsum, dolor sic amet..."}
    p = requests.post('http://localhost:5000/api/books', json=book) # edit this line
    print(p.status_code, p.text) # add this line
    books = requests.get('http://localhost:5000/api/books')
    print(books.json())
```
10. This API requires authentication for any action other than a GET. The example API uses two forms of authentication: 
- bearer token authentication for POST/PUT/DELETE actions 
- Digest authentication for the generation of bearer tokens themselves 
11. First, we will amend our script to generate a bearer token we can then use for subsequent requests:
```python
#! venv/bin/python3
import requests
from requests.auth import HTTPDigestAuth # add this import

if __name__ == '__main__':
    auth = HTTPDigestAuth('learner', 'p@ssword') # provide username and password
    token = requests.post('http://localhost:5000/auth/tokens', auth=auth) # make a request to get a token
    print(token.text) # display token value
    books = requests.get('http://localhost:5000/api/books')
    print(books.json())
```
12. Run the script - you should see a random token value returned by the API server. Now that we are able to generate tokens, we can use token authentication to make a POST request:
```python
#! venv/bin/python3
import requests
from requests.auth import HTTPDigestAuth

if __name__ == '__main__':
    auth = HTTPDigestAuth('learner', 'p@ssword') # define digest auth info
    token = requests.post('http://localhost:5000/auth/tokens', auth=auth) # get new token
    t_auth_headers = {"Authorization": f"Bearer {token.text}"} # create request header with the new token
    book = {"id": "0000012345", "title": "Lorem Ipsum", "genre": "fantasy", "blurb": "Lorem ipsum, dolor sic amet..."}
    requests.post('http://localhost:5000/api/books', json=book, headers=t_auth_headers) # make post request with token header
    books = requests.get('http://localhost:5000/api/books')
    print(books.json())
```
13. The auth flow in this script is as follows:
- The client (i.e. the script) makes an initially unauthenticated POST request to /tokens
- The server returns a response indicating that authentication is required, and providing some server-side generated cryptographic variables
- The client uses the HTTPDigestAuth library to compute a shared secret from the given password and returned cryptographic variables. The server independently computes the same secret
- The client makes a now-authenticated POST request to /tokens, resulting in a token being created and returned
- This token is then subsequently used to authenticate future requests, via HTTP Bearer token authentication
14. Running the script again should show the book now created.

##### Make PUT and DELETE requests
Now that we have a book object to work with, we should try using some other request methods
15. First, edit your script to use a PUT request to update the existing book object:
```python
#! venv/bin/python3
import requests
from requests.auth import HTTPDigestAuth

if __name__ == '__main__':
    auth = HTTPDigestAuth('learner', 'p@ssword')
    token = requests.post('http://localhost:5000/auth/tokens', auth=auth)
    t_auth_headers = {"Authorization": f"Bearer {token.text}"}
    book = {"id": "0000012345", "title": "Lorem Ipsum", "genre": "fantasy", "blurb": "A gripping high-fantasy with sci-fi/thriller elements"} # <- edit this line
    requests.put('http://localhost:5000/api/books', json=book, headers=t_auth_headers) # <- change 'post' to 'put'
    books = requests.get('http://localhost:5000/api/books')
    print(books.json())
```
16. Run the script: `./api_requests.py`. Note the updated blurb for the returned book object.
17. Now let's DELETE the book:
```python
#! venv/bin/python3
import requests
from requests.auth import HTTPDigestAuth

if __name__ == '__main__':
    auth = HTTPDigestAuth('learner', 'p@ssword')
    token = requests.post('http://localhost:5000/auth/tokens', auth=auth)
    t_auth_headers = {"Authorization": f"Bearer {token.text}"}
    book = {"id": "0000012345"} # the only data needed to delete a book is the id
    requests.delete('http://localhost:5000/api/books', json=book, headers=t_auth_headers) # change 'put' to 'delete'
    books = requests.get('http://localhost:5000/api/books')
    print(books.json())
```
18. Re-run the script again and confirm the deletion of the book

#### Stretch Tasks
- Using the file i/o topics we looked at yesterday, create JSON files for book, author and review objects (there is no defined schema for these objects in this API, so these can really be any valid JSON), and amend your script to parse these files and post their contents to the API
- modify your script further to allow the user to specify a file or files to read as the source for the JSON to post

### Lab PY06 - Implementing Retry Logic

#### Objective
Create a script which is able to implement retries for failed API requests

#### Outcomes
By the end of this lab, you will have:
* Implemented *exponential backoff* with a time-out to handle API availability errors

#### High-Level Steps
- Implement a request to a deliberately unreliable endpoint, with basic error handling
- Improve the implementation to use an exponential backoff approach

#### Detailed Steps
##### Ensure the example API is Running
1. Ensure that the sample API server is running (it may still be running from the previous lab):
```bash
sudo docker ps | grep sample-flask-app || sudo sh -c "cd ~/Labs2/PY05; docker compose -f compose.yml up -d --build"
```

##### Make a get request
2. Change directory into PY06: `cd ~/Labs2/PY06` 
3. Create a new virtual environment, with the requests library installed:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install requests
```
4. Open the retry.py file, and add the following contents:
```python
#! venv/bin/python3
import requests

if __name__ == '__main__':
    response = requests.get('http://localhost:5000/api/flaky') # intentionally flaky endpoint
    print(response.status_code)
```
5. Execute the script:
```shell
./retry.py
```
6. Due to the implementation of the deliberately flaky endpoint, you have about a 50-50 chance of getting a 200 or 500 response. If needed, run the script a few times to observe this behaviour

##### Implement retry logic
7. Edit retry.py, and make the changes as shown below:
```python
#! venv/bin/python3
import requests

if __name__ == '__main__':
    try:
        response = requests.get('http://localhost:5000/api/flaky')
    except:
        response = requests.Response() # if the request fails with an exception, just create an empty response object as placeholder
    while response.status_code == None or response.status_code >= 500:
        try:
            response = requests.get('http://localhost:5000/api/flaky')
        except:
            response = requests.Response()
    if response.headers.get('content-type', '') == 'application/json':
        print(response.json())
```
8. This version of the script will first make an initial attempt to connect to the API. Since this could fail with an exception, we wrap this with a try-except. We then continuously re-attempt the request until getting a response with a successful status code, before finally printing the response JSON from the server.  

##### Improve the retry logic
The retry logic we have just implemented has several weaknesses that we would want to avoid in reality. For a start, what if the server never delivers a successful response. We ideally should have some condition under which the client gives up attempting the request and reports a failure.  
Additionally, if the server is unavailable due to traffic saturation, this infinite loop of rapid-fire requests will only make matters worse.  
For these reasons, we will enhance our script to use a more robust retry methodology: _exponential backoff with timeout_. In this method, an exponentially increasing delay is added between attempts, to give the server time to return to a healthy state before the next retry, and a timeout is used to break out of the retry loop after so many failed requests. 
9. Edit retry.py again, like so:
```python
#! venv/bin/python3
import requests
from time import sleep

if __name__ == '__main__':
    delay = 2 # initial delay between requests of 2 seconds
    try:
        response = requests.get('http://localhost:5000/api/flaky')
    except:
        response = requests.Response() # if the request fails with an exception, just create an empty response object as placeholder
    while response.status_code == None or response.status_code >= 500:
        if delay > 60: # if enough iterations have passed for delay to exceed 60s, give up
            print("too many failed attempts")
            break
        sleep(delay) # wait for the delay period
        try:
            response = requests.get('http://localhost:5000/api/flaky') # retry request
        except:
            response = requests.Response()
        delay *= 2 # double the delay if no successful response
    if response.headers.get('content-type', '') == 'application/json':
        print(response.json())
```
10. Run the script again. The retry logic ensures that we have a correct response, with a parseable JSON body, before we attempt to print the JSON.

##### Implement header parsing
11. In the case of a 500 response, the flaky endpoint is configured to return a custom ERROR header as part of the response. We will now parse that header to get more info about the failure. 
12. Edit retry.py again:
```python
#! venv/bin/python3
import requests
from time import sleep

if __name__ == '__main__':
    delay = 2
    try:
        response = requests.get('http://localhost:5000/api/flaky')
    except:
        response = requests.Response() # if the request fails with an exception, just create an empty response object as placeholder
    while response.status_code == None or response.status_code >= 500:
        if delay > 60:
            print("too many failed attempts")
            break
        print("Error: " + response.headers.get("ERROR", "No Error header received"))
        sleep(delay)
        try:
            response = requests.get('http://localhost:5000/api/flaky')
        except:
            response = requests.Response()
        delay *= 2
    if response.headers.get('content-type', '') == 'application/json':
        print(response.json())
```
13. The added print statement parses the ERROR header, if it is present, and prints a debug message with this information. Re-run the script again to observe this behaviour.

#### Optional Stretch Tasks
- Refactor the retry script logic to use an else clause to the while-loop for better handling of loop exit conditions

### Lab PY07 - Async Programming

#### Objective
Adapt an existing, synchronous script to operate asynchronously

#### Outcomes
By the end of this lab, you will have:
* Implemented async behaviour into a script with *asyncio*

#### High-Level Steps
- Run a synchronous script against the data from the example API
- Edit the script logic to use async features, qualitatively compare performance (quantitative comparison will come later)

#### Detailed Steps
##### Set up the API server for this exercise
1. Ensure the API server is running:
```shell
sudo docker ps | grep sample-flask-app || sudo sh -c "cd ~/Labs2/PY05; docker compose -f compose.yml up -d --build"
```
2. Switch directory into the PY07 directory, and setup a virtual environment:
```bash
cd ~/Labs2/PY07
python3 -m venv venv
venv/bin/python3 -m pip install -r requests
```
3. Populate the API server with some sample data using the provided script:
```bash
./populate_books.py
```

##### Starting point
4. Review the contents of 'client.py' - this is the starting point for this exercise. Observe that this initial client is entirely synchronous. We have two key functions in this file. 
* get_book() - retrieves a book, by it's id, from a given array of book objects. 
* process_book_data() - takes a book object, constructs a string from the book objects' attributes, sleeps to imitate some further, time-intensive processing and then returns the string.
The body of the script iterates a list of ids, and for each id uses get_book to get the corresponding book from a list (retrieved via an initial GET request to the API server) and then calls process_book_data on the returned object, in an entirely synchronous process. 
5. Run the client script:
```shell
./client.py
```
6. Make a mental note of roughly how long the script takes to execute - when benchmarking the script during the development of this lab it took approx. 6-7 seconds, but this may be different from machine to machine, and depending on how much data the API already had from previous labs

##### Introducing async
7. Open the client.py file for editing. We will make some key changes in order to make the script asynchronous.
###### Imports
8. We will of course need to import asyncio to be able to use the async features it provides, so change the imports at the top of the script accordingly:
```python
#! venv/bin/python3
import requests
import asyncio
```
###### get_book
9. We will also be making both of our key functions asynchronous, starting with get_book():
```python
async def get_book(iq, books, bq):
    i = await iq.get()
    book = dict()
    for b in books:
        if b.get("id", '') == i:
            book = b
            break
    await bq.put(book)
```
Note the implementation changes here - asides from declaring the function as async, the function now pulls the book id from a queue, and pushes the book object identified by that id to a separate queue
###### process_book_data
10. We will make similar changes to the process_book_data implementation:
```python
async def process_book_data(queue):
    book = await queue.get()
    bookstr = ""
    bookstr += f"ID: {str(book.get('id', ''))}\n"
    bookstr += f"TITLE: {book.get('title', '')}\n"
    bookstr += f"GENRE: {book.get('genre', '')}\n"
    await asyncio.sleep(1)
    print(bookstr)
```
Again, observe the use of a queue to pull books from. Also note that we are now directly printing the book string from this function rather than returning it - this is just to minimise the changes needed to the script - a better approach would be to write the string to yet another queue, and have another async function which reads from that queue and prints the strings out, but this is left as an open extension task, should you wish to attempt it.
###### main
11. We will now edit our main function, which will aggregate the various async logic elements into one entrypoint:
```python
async def main():
    books = requests.get('http://localhost:5000/api/books').json()
    books_queue = asyncio.Queue()
    ids_queue = asyncio.Queue()
    for i in ids:
        await ids_queue.put(i)
    gets = [get_book(ids_queue, books, books_queue) for i in ids]
    procs = [process_book_data(books_queue) for i in ids]
    await asyncio.gather(*gets)
    await asyncio.gather(*procs)
```
This function is now handling setting up the queue objects and the use of asyncio.gather() to run multiple instances of our coroutines concurrently
###### The if name main block
12. With main() consolidating all of the required logic, our if name main block simply needs to asyncronously invoke the main() function:
```python
if __name__ == '__main__':
    asyncio.run(main())
```
###### The overall script
```python
#! venv/bin/python3
import requests
import asyncio

ids = [
    "0000012345",
    "0000012346",
    "0000012347",
    "0000012348",
    "0000012349",
    "0000012350"
]

async def get_book(iq, books, bq):
    i = await iq.get()
    book = dict()
    for b in books:
        if b.get("id", '') == i:
            book = b
            break
    await bq.put(book)

async def process_book_data(queue):
    book = await queue.get()
    bookstr = ""
    bookstr += f"ID: {str(book.get('id', ''))}\n"
    bookstr += f"TITLE: {book.get('title', '')}\n"
    bookstr += f"GENRE: {book.get('genre', '')}\n"
    await asyncio.sleep(1)
    print(bookstr)

async def main():
    books = requests.get('http://localhost:5000/api/books').json()
    books_queue = asyncio.Queue()
    ids_queue = asyncio.Queue()
    for i in ids:
        await ids_queue.put(i)
    gets = [get_book(ids_queue, books, books_queue) for i in ids]
    procs = [process_book_data(books_queue) for i in ids]
    await asyncio.gather(*gets)
    await asyncio.gather(*procs)

if __name__ == '__main__':
    asyncio.run(main())
```

##### Run the async script
13. Save the changes to client.py, and run the script again:
```shell
./client.py
```
14. Compare the execution speed to the original, non-async version - benchmarks during the development of this lab have the async version taking only a second or so to execute, a significant reduction compared to ~6 seconds for the synchronous implementation.

#### Optional Stretch Tasks
- amend the script to also retrieve any author and review data from the API server, and process that. 
- stretch goal 1 will require adding additional calls to requests - investigate the use of the `aiohttp` library to make these requests asynchronously as well

### Lab PY08 - Introduction to the Sandbox API

#### Objective
Deploy and interact with a RESTful API which manages developer sandboxes

#### Outcomes
By the end of this lab, you will have:
* Deployed a RESTful API using the *FastAPI* framework
* Used the FastAPI dev server's swagger UI to test API functionality
* Implemented Authentication for an API server

#### High-Level Steps
- Deploy the API
- Test using the swagger UI
- Add simple auth

#### Detailed Steps
##### Setup the Project
1. Switch directory into the PY08 directory:
```bash
cd ~/Labs2/PY08
```
2. Create a new virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
venv/bin/python3 -m pip install -r requirements.txt
```

##### Deploy the API
3. Start the API server:
```bash
fastapi dev main.py
```

##### Interact with the API via swagger
4. Navigate to http://localhost:8000/docs in your browser to visit the APIs _swagger_ interface. FastAPI automatically generates this interface along with an OpenAPI spec for your application.
5. Edit the example POST requests' body with the following data:
```json
{
  "name": "team-alpha-sbx",
  "owner_email": "owner@bankx.com",
  "size": "small",
  "ttl_days": 7,
  "allowed_cidrs": ["203.0.113.0/24"]
}
```
and execute the request.
7. Copy the returned sandbox ID from the POST request, and use it to experiment with the other endpoints exposed by the API using the UI.

##### Implementing Authentication
Currently, the starter API is unauthenticated. We will change that. 
8. In auth.py, add the following to add FastAPIs authentication middleware:
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()
```
9. To use this middleware, make the following changes to main.py:
* Add these imports:
```python
import auth
from fastapi.security import HTTPAuthorizationCredentials
```
* Add the following additional parameter to each of the handler functions:
```python
authorization: Annotated[HTTPAuthorizationCredentials, Depends(auth.security)]
```
The API will now automatically reject, with a 403, any request which does not present a bearer token. Note that the validity of any presented token is not yet being validated, only that one has been presented.
10. Restart the API, and test it via the swagger UI again. Note that there is now an 'Authenticate' button on the UI, this will allow you to add an appropriate credential which will be used when making the requests.

#### Optional Stretch Tasks
- Expand auth.py to read a set of valid tokens in from a file, and provide a helper function to check whether a token is valid. Add logic to each of your handler functions to call this function on the token presented as part of a request.

- Use your understanding of the requests library to implement scripted POST, GET, PATCH and DELETE requests to the API
