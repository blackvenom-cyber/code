from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''INSERT INTO users (username, password) VALUES ('admin', 'admin123')''')
    conn.commit()
    conn.close()

@app.route('/vulnerable', methods=['GET', 'POST'])
def vulnerable():
    user_id = request.args.get('userId')
    username = request.form.get('username')
    password = request.form.get('password')
    
    # SQL Injection Vulnerability
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    result = c.execute(query)

    user_data = ""
    for row in result:
        user_data += f"ID: {row[0]}, Username: {row[1]}<br>"

    conn.close()

    # XSS Vulnerability
    response = f"""
    <html>
        <body>
            <form method="post" action="/vulnerable">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
            <br>
            {user_data}
        </body>
    </html>
    """

    # Hardcoded credentials
    if username == "admin" and password == "admin123":
        response += "<br>Login successful!"
    else:
        response += "<br>Login failed!"

    return render_template_string(response)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

