from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database import History
from sqlalchemy import func

views = Blueprint("views", __name__, template_folder="templates")

# Views

usernames = []

@views.route('/', methods=['GET', 'POST'])
def home():
    #Login
    if request.method == 'POST':

        if 'logout' in request.form:
            if 'username' in session:
                if session['username'] in usernames:
                    usernames.remove(session['username'])
                del session['username']
            if 'room' in session:
                del session['room']
            flash(f"You were successfully logged out.")
            active = ['active', '', '']
            return render_template('index.html', active=active)

        if 'login' in request.form:
            if request.values.get('username') in usernames:
                flash(f"the username has already been taken")
                return redirect(url_for('views.home'))

            try:
                session['username'] = request.values.get('username')
                session['room'] = request.values.get('room')
            except KeyError as e:
                print(e)

            usernames.append(session['username'])

            if 'username' in session and 'room' in session:
                if session['username'] and session['room']:
                    flash(f"You were successfully logged in as { session['username'] }.")
                    active = ['', 'active', '']
                    return render_template('chat.html', username=session['username'], room=session['room'], active=active)
    
    active = ['active', '', '']
    return render_template('index.html', active=active)

@views.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' in session and 'room' in session:
        if session['username'] and session['room']:
            # flash(f"You were successfully logged in as { session['username'] }.")
            active = ['', 'active', '']
            return render_template('chat.html', username=session['username'], room=session['room'], active=active)
    
    return redirect(url_for('views.home'))

@views.route('/history')
def history():
    if 'username' in session and 'room' in session:
        if session['username'] and session['room']:
            active = ['', '', 'active']
            prev_messages = History.query.filter_by(room=session['room'])
            return render_template('history.html', username=session['username'], room=session['room'], prev_messages=prev_messages, active=active)
    
    return redirect(url_for('views.home'))


@views.route('/stats')
def stats():
    # result = History.query.group_by(History.username)
    result = History.query.with_entities(History.username, func.count(History.username)).group_by(History.username).all()
    active = ['', '', 'active']
    return render_template('stats.html', active=active, result=result)