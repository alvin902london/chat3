from flask import Flask, session, flash
from flask_socketio import SocketIO, join_room, leave_room
from flask_session import Session
from datetime import datetime
from __init__ import create_app
from database import db, History

# Setup
app = create_app()
Session(app)
# manage_session=False > set socket to not fork their own sessions so the session is managed on the server side and is in sync
socketio = SocketIO(app, cors_allowed_origins='*', manage_session=False) 


# Communication functions
@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info(f"{ data['username'] } has sent a message to the room { data['room'] }: { data['message'] }")

    created_at = datetime.now()
    history = History(username=data['username'], room=data['room'], message=data['message'], created_at=created_at)
    _save_msg(history)

    
    data['created_at'] = created_at.strftime("%d %b %Y, %H:%M")
    socketio.emit('received_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    msg = f"{ data['username'] } has joined the room { data['room'] }"
    app.logger.info(msg)

    history = History(username="admin", room=data['room'], message=msg)
    _save_msg(history)

    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    msg = f"{ data['username'] } has left the room { data['room'] }"
    app.logger.info(msg)
    
    history = History(username="admin", room=data['room'], message=msg)
    _save_msg(history)

    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])

# @socketio.on('logout')
# def logout(data):
#     del session['username']
#     del session['room']
#     flash(f"You were successfully logged out.")

# Utilities
def _save_msg(data):
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        print(e)


# Mainline to start the web server
if __name__ == '__main__':
    socketio.run(app, debug=True)

