# Chat Application

## Setup

Make sure you have python 3.6+ installed.

```bash
pip install -r requirements.txt
```

Create database if one doesn't exist

```bash
cd path/to/chat3
python
from app import db
db.create_all()
```


## Running the Server

```bash
python app.py
```

## Clearing Chat History

Simply delete the `history.db` file.

## Future Improvements

* Test Plan
    * pytest

* Development Side:
    * A User table for storing user info and login instead of using only sessions
    * Make the server side an api to scale
    * Save config in an env environment

* UI/UX:
    * A list of users who are in the chat room
    * A list of active/archived rooms
    * User's own message to be displayed on the opposite side
    * Messages are archievd when the user logout, not when the user leaves the room
    * Chat history should starts from the most recent and cap at certain time



# chat3
