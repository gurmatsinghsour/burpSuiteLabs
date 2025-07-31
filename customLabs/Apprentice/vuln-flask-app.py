from flask import Flask, request, session, redirect, render_template_string, send_from_directory
import os
import uuid
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # hardcoded, vulnerable

USERS = {
    "user1": {"password": "pass123", "role": "user", "id": "1001"},
    "admin": {"password": "admin123", "role": "admin", "id": "9001"}
}

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy in-memory messages
MESSAGES = {
    "1001": "Welcome user1. Your inbox is empty.",
    "9001": "Admin messages: reset credentials, audit logs"
}

@app.route('/')
def index():
    return render_template_string('''
        <h1>Vuln App</h1>
        {% if session.get("username") %}
            <p>Hello, {{session['username']}} ({{session['role']}})</p>
            <a href="/logout">Logout</a><br>
            <a href="/upload">Upload file</a><br>
            <a href="/fetch">Fetch external</a><br>
            <a href="/messages?id={{session['id']}}">My Messages</a><br>
            {% if session['role'] == "admin" %}
                <a href="/admin-panel">Admin Panel</a><br>
            {% endif %}
        {% else %}
            <form method="POST" action="/login">
                <input name="username"><br>
                <input name="password" type="password"><br>
                <input type="submit">
            </form>
        {% endif %}
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = USERS.get(username)
    if user and password == user['password']:
        session['username'] = username
        session['role'] = user['role']
        session['id'] = user['id']
        return redirect('/')
    return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/messages')
def messages():
    user_id = request.args.get('id')
    return f"<h2>Messages for user {user_id}</h2><p>{MESSAGES.get(user_id, 'No messages found.')}</p>"

@app.route('/admin-panel')
def admin_panel():
    if session.get('role') != 'admin':
        return "403 Forbidden", 403
    return "Welcome to the Admin Panel"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.jpg') or file.filename.endswith('.png'):
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            return f"Uploaded to {path}"
        else:
            return "Only .jpg and .png allowed", 400
    return '''
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
        </form>
    '''

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if url:
        try:
            r = requests.get(url, timeout=2)
            return f"<pre>{r.text}</pre>"
        except Exception as e:
            return f"Error: {e}"
    return "Please provide ?url=...", 400

if __name__ == '__main__':
    app.run(debug=True)
