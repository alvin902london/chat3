from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database import History

views = Blueprint("views", __name__, template_folder="templates")

# Views

@views.route('/', methods=['GET', 'POST'])
def home():
    #Login
    if request.method == 'POST':
        if 'logout' in request.form:
            if 'username' in session:
                del session['username']
            if 'room' in session:
                del session['room']
            flash(f"You were successfully logged out.")
            active = ['active', '', '']
            return render_template('index.html', active=active)
        if 'login' in request.form:
            try:
                session['username'] = request.values.get('username')
                session['room'] = request.values.get('room')
            except KeyError as e:
                print(e)
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