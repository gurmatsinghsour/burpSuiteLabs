# 🔒 Cybersecurity Lab: Server-Side Vulnerabilities

## 🎯 Lab Overview
This lab contains a vulnerable Flask web application with multiple security flaws. Your mission is to identify and exploit these vulnerabilities using the knowledge from your Burp Suite server-side vulnerabilities training.

## 🛠️ Setup Instructions

### 1. Environment Setup
```bash
# Create a new directory for the lab
mkdir cybersec-lab
cd cybersec-lab

# Save the Python code as 'app.py'
# Install required packages
pip install flask requests

# Run the application
python app.py
```

### 2. Access the Application
- Open your browser and go to `http://localhost:5000`
- The application will be running with debug mode enabled

### 3. Tools You'll Need
- **Burp Suite Community/Pro** (for intercepting requests)
- **Web browser** (Chrome/Firefox with developer tools)
- **Command line/Terminal** (for creating test files)

---

## 🎮 Lab Challenges

### Challenge 1: Authentication Bypass (SQL Injection)
**Difficulty:** ⭐⭐☆☆☆ (Apprentice Level)

**Objective:** Gain access to the admin account without knowing the password.

**Hints:**
- Look at the login form
- Try special characters in the username field
- Remember the SQL injection techniques from your reading
- The admin username is `admin` but you need to bypass the password check

**What to try:**
- Enter different payloads in the username field
- Use Burp Suite to intercept the login request
- Look for SQL syntax that could break the query logic

**Success criteria:** You should be able to log in as admin and see the "Admin Panel" link.

---

### Challenge 2: Horizontal Privilege Escalation (IDOR)
**Difficulty:** ⭐⭐☆☆☆ (Apprentice Level)

**Objective:** Access another user's messages and profile information.

**Starting point:** Log in as `user1` with password `pass123`

**Hints:**
- Look at the URL when viewing "My Messages"
- Try changing the ID parameter
- Check the "Profile" link and experiment with the user parameter
- Remember: there are 3 users in the system (IDs: 1, 2, 3)

**What to explore:**
- `/messages?id=X` - try different values for X
- `/profile?user=X` - try different usernames

**Success criteria:** You should be able to read admin messages and view other users' profiles.

---

### Challenge 3: Server-Side Request Forgery (SSRF)
**Difficulty:** ⭐⭐⭐☆☆ (Intermediate)

**Objective:** Use the "Fetch Data" feature to access internal/local resources.

**Hints:**
- The fetch feature makes requests to external URLs
- Try pointing it to localhost/internal services
- Remember the loopback addresses: `127.0.0.1`, `localhost`
- Look for internal endpoints that might be accessible

**What to try:**
- `http://localhost:5000/admin-panel`
- `http://127.0.0.1:5000/messages?id=2`
- `http://localhost:5000/profile?user=admin`

**Success criteria:** You should be able to access admin functionality through SSRF.

---

### Challenge 4: Unprotected Functionality Discovery
**Difficulty:** ⭐⭐☆☆☆ (Apprentice Level)

**Objective:** Find hidden admin endpoints through reconnaissance.

**Hints:**
- Not all admin functionality is linked from the main interface
- Try directory/endpoint enumeration
- Look for common admin paths
- Sometimes functionality is hidden with "security by obscurity"

**Common admin paths to try:**
- `/admin`
- `/administrator`
- `/admin-console`
- `/management`
- Look for endpoints with random strings (harder to guess)

**Success criteria:** Find the hidden admin panel with sensitive information.

---

### Challenge 5: File Upload Vulnerabilities
**Difficulty:** ⭐⭐⭐☆☆ (Intermediate)

**Objective:** Upload malicious files and achieve code execution.

**Hints:**
- The upload function has weak validation
- Try different file extensions
- Create files with double extensions
- Look into bypassing the MIME type checks

**What to try:**
1. Create a simple PHP web shell:
   ```php
   <?php echo system($_GET['cmd']); ?>
   ```
2. Save it with different extensions
3. Try uploading and accessing it

**Success criteria:** Upload a web shell and execute system commands.

---

### Challenge 6: Vertical Privilege Escalation
**Difficulty:** ⭐⭐⭐☆☆ (Intermediate)

**Objective:** Combine multiple vulnerabilities to gain admin access.

**Approach:**
- Use IDOR to access admin information
- Use that information to escalate privileges
- Chain vulnerabilities together

**Success criteria:** Gain full administrative access through vulnerability chaining.

---

## 📋 Lab Progress Tracking

### Vulnerability Checklist:
- [ ] **SQL Injection** - Bypass login authentication
- [ ] **IDOR (Horizontal)** - Access other users' data
- [ ] **SSRF** - Access internal services
- [ ] **Unprotected Functionality** - Find hidden endpoints
- [ ] **File Upload** - Upload malicious files
- [ ] **Access Control** - Vertical privilege escalation

### Evidence Collection:
For each vulnerability found, document:
1. **Vulnerability Type**
2. **Location** (URL/parameter)
3. **Payload Used**
4. **Impact** (what you could access/do)
5. **Screenshot** (if applicable)

---

## 🔍 Advanced Challenges (Optional)

### Challenge A: Session Manipulation
- Analyze the session cookies
- Try to manipulate session data
- Look for session fixation issues

### Challenge B: Information Disclosure
- Look for error messages that reveal system information
- Check for debug information leakage
- Find configuration files or backup files

### Challenge C: Command Injection
- If you achieve file upload, try to chain it with command injection
- Look for ways to execute system commands

---

## 🛡️ Defensive Mindset

After completing the challenges, think about:

### How to Fix These Vulnerabilities:
1. **SQL Injection**: Use parameterized queries
2. **IDOR**: Implement proper access controls
3. **SSRF**: Validate and restrict URLs
4. **File Upload**: Proper validation and sandboxing
5. **Access Control**: Implement role-based access control

### Security Best Practices:
- Input validation and sanitization
- Least privilege principle
- Defense in depth
- Regular security testing

---

## 📝 Submission Requirements

Create a report documenting:

1. **Executive Summary**
2. **Vulnerabilities Found** (with evidence)
3. **Risk Assessment** (High/Medium/Low for each)
4. **Remediation Recommendations**
5. **Testing Methodology**

---

## 🆘 Need Help?

### Stuck on a Challenge?
1. Review the relevant section in your study materials
2. Use Burp Suite's built-in scanner for hints
3. Check the browser's developer tools for clues
4. Try variations of the suggested payloads

### Learning Resources:
- **OWASP Top 10**
- **PortSwigger Web Security Academy**
- **Burp Suite Documentation**

---

**Remember:** This is a safe learning environment. Take your time, experiment, and learn from each attempt. Real-world applications should never be tested without explicit permission!

Good luck, and happy hacking! 🎉