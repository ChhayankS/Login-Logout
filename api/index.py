from flask import Flask, render_template_string, request, redirect, url_for, session
import os

app = Flask(__name__)

# Set secret key for sessions
app.secret_key = os.urandom(24)

# In-memory "database" to store users
users_db = {}

# Route to Signup page (renders HTML content directly)
@app.route('/')
def signup():
    signup_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Signup</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                width: 400px;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h2 {
                margin-bottom: 20px;
                color: #333;
            }
            input {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Signup to DOSS MEDIATECH</h2>
            <form action="/signup" method="POST">
                <input type="text" name="name" placeholder="Full Name" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Sign Up</button>
            </form>
            <p>Already have an account? <a href="/login">Login here</a></p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(signup_html)

# Route to handle signup form submission
@app.route('/signup', methods=['POST'])
def handle_signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Check if the email already exists in the "database"
    if email in users_db:
        return "User with this email already exists!"

    # Insert new user data into the "database"
    users_db[email] = {'name': name, 'password': password}
    return redirect(url_for('login'))

# Route to Login page (renders HTML content directly)
@app.route('/login')
def login():
    login_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                width: 400px;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h2 {
                margin-bottom: 20px;
                color: #333;
            }
            input {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Login to DOSS MEDIATECH</h2>
            <form action="/login_user" method="POST">
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <p>Don't have an account? <a href="/">Sign up here</a></p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(login_html)

# Route to handle login form submission
@app.route('/login_user', methods=['POST'])
def handle_login():
    email = request.form['email']
    password = request.form['password']

    # Check if the email exists in the "database" and password matches
    user = users_db.get(email)

    if user and user['password'] == password:
        session['user'] = email  # Store email in session to track user
        return redirect(url_for('welcome'))
    else:
        return "Invalid credentials!"

# Route to Welcome page after login (renders HTML content directly)
@app.route('/welcome')
def welcome():
    if 'user' in session:
        user = users_db.get(session['user'])
        welcome_html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .container {{
                    width: 400px;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }}
                h2 {{
                    margin-bottom: 20px;
                    color: #333;
                }}
                button {{
                    width: 100%;
                    padding: 10px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                button:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Welcome, {user['name']}!</h2>
                <p>You have successfully logged in to DOSS MEDIATECH.</p>
                <a href="/logout"><button>Logout</button></a>
            </div>
        </body>
        </html>
        '''
        return render_template_string(welcome_html)
    return redirect(url_for('login'))

# Route to logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
