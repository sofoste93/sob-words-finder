from flask import Flask, render_template, request, session, redirect, url_for
from utils import authentication, operations, finder
import os

app = Flask(__name__)
app.secret_key = 'super secret key'  # Replace this with a real secret key in production!

from flask import jsonify


@app.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if operations.verify_answer(user_answer, session):
            username, pin = authentication.generate_credentials()
            session['username'] = username
            session['pin'] = pin
            return jsonify({'status': 'success', 'username': username, 'pin': pin}), 200
        else:
            return jsonify({'status': 'failure', 'message': 'Incorrect answer. Please try again.'}), 200
    else:
        operation, result = operations.generate_operation()
        session['result'] = result
        return render_template('landing.html', operation=operation)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin = request.form.get('pin')
        if authentication.verify_credentials(username, pin, session):
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


@app.route('/default_finder', methods=['GET', 'POST'])
def default_finder():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        word = request.form.get('word')
        file_path = os.path.join(os.path.dirname(__file__), 'uploads', 'default.txt')
        results = finder.find_word(file_path, word)
        return render_template('search.html', results=results, title='Default Finder', is_custom=False)
    else:
        return render_template('search.html', title='Default Finder', is_custom=False)


@app.route('/custom_finder', methods=['GET', 'POST'])
def custom_finder():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        word = request.form.get('word')
        file = request.files['file']  # Here's the file reference
        file_path = os.path.join(os.path.dirname(__file__), 'uploads', file.filename)  # It's used here
        file.save(file_path)
        results = finder.find_word(file_path, word)
        return render_template('search.html', results=results, title='Custom Finder', is_custom=True)
    else:
        return render_template('search.html', title='Custom Finder', is_custom=True)


@app.route('/new-operation', methods=['GET'])
def new_operation():
    operation, result = operations.generate_operation()
    session['result'] = result
    return jsonify({'operation': operation}), 200


@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        word = request.form.get('word')
        file = request.files.get('file')  # this may be None if no file was uploaded
        if file:  # custom search in the uploaded file
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            results = finder.find_word(file_path, word)
            return render_template('search.html', results=results, title='Custom Finder', is_custom=True)
        else:  # default search in 'default.txt'
            results = finder.find_word('default.txt', word)
            return render_template('search.html', results=results, title='Default Finder', is_custom=False)
    else:
        return render_template('search.html', title='Custom Finder', is_custom=True)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


if __name__ == '__main__':
    app.run(debug=True)
