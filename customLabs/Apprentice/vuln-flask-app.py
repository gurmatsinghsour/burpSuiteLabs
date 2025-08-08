from flask import Flask, request, session, redirect, render_template_string, send_from_directory, jsonify
import os
import uuid
import requests
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # hardcoded, vulnerable

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, email TEXT)''')
    c.execute("INSERT OR REPLACE INTO users VALUES (1, 'user1', 'pass123', 'user', 'user1@company.com')")
    c.execute("INSERT OR REPLACE INTO users VALUES (2, 'admin', 'admin123', 'admin', 'admin@company.com')")
    c.execute("INSERT OR REPLACE INTO users VALUES (3, 'guest', 'guest', 'guest', 'guest@company.com')")
    conn.commit()
    conn.close()

init_db()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy in-memory messages
MESSAGES = {
    "1": "Welcome user1! Your account balance: $500. Recent transactions: Coffee shop $4.50",
    "2": "ADMIN: Server maintenance scheduled. Backup codes: 7749, 8851. Reset all user passwords.",
    "3": "Guest account - limited access only."
}

# CSS styling for better UI
CSS_STYLE = """
<style>
    body { 
        font-family: Arial, sans-serif; 
        max-width: 800px; 
        margin: 50px auto; 
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .container { 
        background: rgba(255,255,255,0.1); 
        padding: 30px; 
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .login-form { 
        background: rgba(255,255,255,0.2); 
        padding: 20px; 
        border-radius: 10px; 
        margin: 20px 0;
    }
    input[type="text"], input[type="password"], input[type="file"] { 
        width: 100%; 
        padding: 10px; 
        margin: 5px 0; 
        border: none; 
        border-radius: 5px;
        background: rgba(255,255,255,0.9);
        color: #333;
    }
    button, input[type="submit"] { 
        background: #ff6b6b; 
        color: white; 
        padding: 10px 20px; 
        border: none; 
        border-radius: 5px; 
        cursor: pointer;
        margin: 5px;
    }
    button:hover, input[type="submit"]:hover { 
        background: #ff5252; 
    }
    .nav-link { 
        display: inline-block; 
        background: rgba(255,255,255,0.2); 
        padding: 8px 15px; 
        margin: 5px; 
        text-decoration: none; 
        color: white; 
        border-radius: 5px;
    }
    .nav-link:hover { 
        background: rgba(255,255,255,0.3); 
        color: white;
    }
    .admin-panel { 
        background: rgba(255,215,0,0.2); 
        border: 2px solid gold; 
        padding: 15px; 
        border-radius: 8px; 
        margin: 10px 0;
    }
    .user-info { 
        background: rgba(255,255,255,0.15); 
        padding: 15px; 
        border-radius: 8px; 
        margin: 15px 0;
    }
    h1 { text-align: center; margin-bottom: 30px; }
    .vulnerability-hint { 
        background: rgba(255,0,0,0.1); 
        padding: 10px; 
        border-left: 4px solid #ff6b6b; 
        margin: 10px 0;
        font-size: 0.9em;
    }
</style>
"""

@app.route('/')
def index():
    return render_template_string(CSS_STYLE + '''
    <div class="container">
        <h1>🔒 SecureCorp Web Portal</h1>
        {% if session.get("username") %}
            <div class="user-info">
                <h3>Welcome back, {{session['username']}}!</h3>
                <p><strong>Role:</strong> {{session['role']}} | <strong>ID:</strong> {{session['id']}}</p>
                <p><strong>Access Level:</strong> 
                {% if session['role'] == "admin" %}
                    <span style="color: gold;">🌟 Administrator</span>
                {% elif session['role'] == "user" %}
                    <span style="color: lightblue;">👤 Standard User</span>
                {% else %}
                    <span style="color: lightgray;">👥 Guest</span>
                {% endif %}
                </p>
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <a href="/logout" class="nav-link">🚪 Logout</a>
                <a href="/upload" class="nav-link">📁 Upload Files</a>
                <a href="/fetch" class="nav-link">🌐 Fetch Data</a>
                <a href="/messages?id={{session['id']}}" class="nav-link">📧 My Messages</a>
                <a href="/profile?user={{session['username']}}" class="nav-link">👤 Profile</a>
                {% if session['role'] == "admin" %}
                    <a href="/admin-panel" class="nav-link" style="background: gold; color: black;">⚡ Admin Panel</a>
                {% endif %}
            </div>
            
            <div class="vulnerability-hint">
                <strong>🎯 Lab Objective:</strong> Explore this application and find security vulnerabilities. 
                Try different approaches to access unauthorized areas!
            </div>
        {% else %}
            <div class="login-form">
                <h2>🔐 Employee Login</h2>
                <form method="POST" action="/login">
                    <input name="username" placeholder="Username" required><br>
                    <input name="password" type="password" placeholder="Password" required><br>
                    <input type="submit" value="🚀 Login">
                </form>
                
                <div style="margin-top: 20px; font-size: 0.9em;">
                    <p><strong>Demo Accounts:</strong></p>
                    <p>👤 Standard User: user1 / pass123</p>
                    <p>👥 Guest: guest / guest</p>
                    <p>⚡ Admin: [Try to find the credentials!]</p>
                </div>
            </div>
        {% endif %}
    </div>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Vulnerable SQL query - SQLi possible here
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = c.execute(query).fetchone()
    conn.close()
    
    if result:
        session['username'] = result[1]
        session['role'] = result[3]
        session['id'] = str(result[0])
        return redirect('/')
    return render_template_string(CSS_STYLE + '''
        <div class="container">
            <h2 style="color: #ff6b6b;">❌ Login Failed</h2>
            <p>Invalid credentials provided.</p>
            <a href="/" class="nav-link">🔙 Back to Login</a>
        </div>
    '''), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/messages')
def messages():
    user_id = request.args.get('id')
    if not user_id:
        return "Missing user ID parameter", 400
    
    return render_template_string(CSS_STYLE + f'''
    <div class="container">
        <h2>📧 Messages for User #{user_id}</h2>
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
            <p>{MESSAGES.get(user_id, 'No messages found for this user.')}</p>
        </div>
        <a href="/" class="nav-link">🏠 Home</a>
    </div>
    ''')

@app.route('/profile')
def profile():
    username = request.args.get('user')
    if not username:
        return "Missing user parameter", 400
    
    # Vulnerable - no proper access control
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    user_data = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    
    if user_data:
        return render_template_string(CSS_STYLE + f'''
        <div class="container">
            <h2>👤 User Profile</h2>
            <div class="user-info">
                <p><strong>Username:</strong> {user_data[1]}</p>
                <p><strong>Role:</strong> {user_data[3]}</p>
                <p><strong>Email:</strong> {user_data[4]}</p>
                <p><strong>User ID:</strong> {user_data[0]}</p>
            </div>
            <a href="/" class="nav-link">🏠 Home</a>
        </div>
        ''')
    return "User not found", 404

@app.route('/admin-panel')
def admin_panel():
    # Weak access control - only checks session role
    if session.get('role') != 'admin':
        return render_template_string(CSS_STYLE + '''
        <div class="container">
            <h2 style="color: #ff6b6b;">🚫 Access Denied</h2>
            <p>You need administrator privileges to access this area.</p>
            <a href="/" class="nav-link">🏠 Home</a>
        </div>
        '''), 403
    
    return render_template_string(CSS_STYLE + '''
    <div class="container">
        <div class="admin-panel">
            <h2>⚡ Administrator Control Panel</h2>
            <h3>🔧 System Management</h3>
            <ul>
                <li>Server Status: Online ✅</li>
                <li>Database: Connected ✅</li>
                <li>Security Level: Medium ⚠️</li>
                <li>Last Backup: 2024-01-15</li>
            </ul>
            
            <h3>📊 User Statistics</h3>
            <ul>
                <li>Total Users: 3</li>
                <li>Active Sessions: 1</li>
                <li>Failed Login Attempts: 0</li>
            </ul>
            
            <h3>🔑 Administrative Actions</h3>
            <button onclick="alert('Password reset initiated for all users!')">Reset All Passwords</button>
            <button onclick="alert('System backup started!')">Backup Database</button>
            <button onclick="alert('Audit log exported!')">Export Logs</button>
        </div>
        <a href="/" class="nav-link">🏠 Home</a>
    </div>
    ''')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename:
            return "No file selected", 400
        
        # Weak validation - only checks extension, not content
        if file.filename.endswith(('.jpg', '.png', '.gif', '.txt')):
            filename = file.filename  # No secure_filename() used - vulnerable
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)
            return render_template_string(CSS_STYLE + f'''
            <div class="container">
                <h2>✅ Upload Successful</h2>
                <p>File uploaded to: <code>{path}</code></p>
                <p><a href="/uploads/{filename}" target="_blank">📎 View uploaded file</a></p>
                <a href="/upload" class="nav-link">📁 Upload Another</a>
                <a href="/" class="nav-link">🏠 Home</a>
            </div>
            ''')
        else:
            return render_template_string(CSS_STYLE + '''
            <div class="container">
                <h2 style="color: #ff6b6b;">❌ Upload Failed</h2>
                <p>Only .jpg, .png, .gif and .txt files allowed</p>
                <a href="/upload" class="nav-link">📁 Try Again</a>
            </div>
            '''), 400
    
    return render_template_string(CSS_STYLE + '''
    <div class="container">
        <h2>📁 File Upload Center</h2>
        <div class="login-form">
            <form method="POST" enctype="multipart/form-data">
                <label>Choose file to upload:</label>
                <input type="file" name="file" accept=".jpg,.png,.gif,.txt">
                <input type="submit" value="🚀 Upload File">
            </form>
            <p style="font-size: 0.9em; margin-top: 15px;">
                <strong>Allowed formats:</strong> JPG, PNG, GIF, TXT<br>
                <strong>Max size:</strong> 10MB
            </p>
        </div>
        <a href="/" class="nav-link">🏠 Home</a>
    </div>
    ''')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if url:
        try:
            # Vulnerable SSRF - no URL validation
            r = requests.get(url, timeout=5)
            return render_template_string(CSS_STYLE + f'''
            <div class="container">
                <h2>🌐 External Data Fetched</h2>
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto;">
                    <pre style="color: #00ff00; font-family: monospace;">{r.text}</pre>
                </div>
                <a href="/fetch" class="nav-link">🔄 Fetch Again</a>
                <a href="/" class="nav-link">🏠 Home</a>
            </div>
            ''')
        except Exception as e:
            return render_template_string(CSS_STYLE + f'''
            <div class="container">
                <h2 style="color: #ff6b6b;">❌ Fetch Error</h2>
                <p>Error occurred: {str(e)}</p>
                <a href="/fetch" class="nav-link">🔄 Try Again</a>
            </div>
            ''')
    
    return render_template_string(CSS_STYLE + '''
    <div class="container">
        <h2>🌐 External Data Fetcher</h2>
        <div class="login-form">
            <form method="GET">
                <label>Enter URL to fetch:</label>
                <input type="text" name="url" placeholder="https://api.example.com/data" style="font-family: monospace;">
                <input type="submit" value="🚀 Fetch Data">
            </form>
            <p style="font-size: 0.9em; margin-top: 15px;">
                <strong>Examples:</strong><br>
                • https://httpbin.org/json<br>
                • https://api.github.com/users/octocat<br>
                • http://localhost:5000/admin-panel
            </p>
        </div>
        <a href="/" class="nav-link">🏠 Home</a>
    </div>
    ''')

# Hidden admin endpoint - security through obscurity
@app.route('/secret-admin-backup-panel-x7k9')
def secret_admin():
    return render_template_string(CSS_STYLE + '''
    <div class="container">
        <div class="admin-panel">
            <h2>🔐 Secret Admin Backup Panel</h2>
            <p><strong>🚨 CONFIDENTIAL SYSTEM ACCESS 🚨</strong></p>
            <p>Database backup location: /var/backups/</p>
            <p>Root password: backup_root_2024!</p>
            <p>API Keys: sk-admin-xyz789, token-backup-abc123</p>
            <p>This panel should only be accessible to system administrators.</p>
        </div>
        <a href="/" class="nav-link">🏠 Home</a>
    </div>
    ''')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5999)