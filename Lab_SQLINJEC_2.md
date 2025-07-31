# Lab Report – SQL Injection Login Bypass

**Lab Title:** SQL injection vulnerability allowing login bypass  
**Category:** SQL Injection  
**Platform:** Web Security Academy  
**Author:** Gurmat Singh Sour  
**Date:** July 30, 2025  

---

## 1. Summary

This lab demonstrates how a SQL injection vulnerability in the login functionality can be exploited to bypass authentication and gain access to an administrator account without valid credentials.

---

## 2. Reconnaissance

**Target URL:**  
`https://<lab-url>/login`

**Tools Used:**
- Burp Suite Community Edition (Proxy, Repeater)
- Browser

**Pages Observed:**
- `/` – Homepage  
- `/login` – Login page with `username` and `password` fields  
- Possible admin dashboard or user account page after login

**Initial Behavior:**  
The login page accepts any username and password, and on failed login displays an error such as "Invalid username or password." This hints at SQL query behavior behind the form.

---

## 3. Vulnerability Discovery

Testing began by submitting common SQL injection payloads in the username and/or password fields, such as:

```
Username: ' OR 1=1--
Password: anything
```
![alt text](/Screenshots/SQL_injectionLab2/2.png)

&


![alt text](/Screenshots/SQL_injectionLab2/1.png)


Both approach attempts to manipulate the SQL `WHERE` clause to always return true, bypassing authentication checks.

---

## 4. Exploitation

### Payload Used:

```sql
Username: ' OR 1=1--
Password: '
```
and

```sql
Username: administrator'--
Password: '
```

5. Impact

A successful SQL injection in the login function allows:

Bypassing user authentication without credentials
Logging in as other users, including administrators
Potential privilege escalation and full system compromise
In real-world scenarios, this could result in data breaches, account takeovers, or even server access if chained with other vulnerabilities.

### 6. Recommendation

To prevent login bypass via SQL injection:

Always use parameterized queries (prepared statements)
Validate and sanitize all user inputs on the server side
Avoid building SQL queries by concatenating strings
Implement logging and alerting for suspicious login attempts
Regularly test authentication mechanisms for injection flaws

### 7. Conclusion

The login form was vulnerable to a SQL injection attack, which allowed bypassing authentication logic by injecting a true condition. This confirms that user input was being directly inserted into the SQL query without proper sanitization, making it possible to log in as the administrator without valid credentials.