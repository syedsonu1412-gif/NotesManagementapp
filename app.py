# from flask import Flask, render_template, request, redirect, session, flash, url_for
# import pymysql
# from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import URLSafeTimedSerializer
# from flask_mail import Mail, Message

# # --------------------
# # App Initialization
# # --------------------
# app = Flask(__name__)
# app.secret_key = "myverysecretkey"

# # --------------------
# # Mail Configuration
# # --------------------
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = "sonusyed392@gmail.com"
# app.config['MAIL_PASSWORD'] = "hojx yszj liaq qade"

# mail = Mail(app)

# # --------------------
# # Token Serializer
# # --------------------
# s = URLSafeTimedSerializer(app.secret_key)

# # --------------------
# # Database Connection
# # --------------------
# import pymysql

# def get_db_connection():
#     return pymysql.connect(
#         host="localhost",
#         user="root",
#         password="sonu",
#         database="notesdb",
#         charset="utf8mb4",
#         cursorclass=pymysql.cursors.DictCursor,
#         auth_plugin_map={
#             'caching_sha2_password': 'mysql_native_password'
#         }
#     )

# # def get_db_connection():
# #     return pymysql.connect(
# #         host="localhost",
# #         user="root",
# #         password="sonu",
# #         database="notesdb",
# #         cursorclass=pymysql.cursors.DictCursor
# #     )

# # --------------------
# # Home
# # --------------------
# @app.route('/')
# def home():
#     if 'user_id' in session:
#         return redirect('/viewall')
#     return redirect('/login')

# # --------------------
# # Register
# # --------------------
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username'].strip()
#         email = request.form['email'].strip()
#         password = request.form['password']

#         if not username or not email or not password:
#             flash("All fields required", "danger")
#             return redirect('/register')

#         hashed_pw = generate_password_hash(password)

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute("SELECT id FROM users WHERE email=%s", (email,))
#         if cur.fetchone():
#             flash("Email already registered", "danger")
#             return redirect('/register')

#         cur.execute(
#             "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
#             (username, email, hashed_pw)
#         )

#         conn.commit()
#         cur.close()
#         conn.close()

#         flash("Registration successful", "success")
#         return redirect('/login')

#     return render_template('register.html')

# # --------------------
# # Login
# # --------------------
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         if not email or not password:
#             flash("Email and password required", "danger")
#             return redirect(url_for('login'))

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute("SELECT * FROM users WHERE email=%s", (email,))
#         user = cur.fetchone()

#         cur.close()
#         conn.close()

#         if user and check_password_hash(user['password'], password):
#             session['user_id'] = user['id']
#             session['email'] = user['email']
#             session['username'] = user['username']
#             return redirect(url_for('viewall'))

#         flash("Invalid email or password", "danger")

#     return render_template('login.html')

# # --------------------
# # About & Contact
# # --------------------
# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# # --------------------
# # Forgot Password
# # --------------------
# @app.route('/forgot-password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form['email']

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute("SELECT * FROM users WHERE email=%s", (email,))
#         user = cur.fetchone()

#         if user:
#             token = s.dumps(email, salt='password-reset-salt')

#             reset_link = url_for(
#                 'reset_with_token',
#                 token=token,
#                 _external=True
#             )

#             msg = Message(
#                 subject="Reset Your Password",
#                 sender=app.config['MAIL_USERNAME'],
#                 recipients=[email]
#             )

#             msg.body = f"""
# Hello {user['username']},

# Click the link below to reset your password:
# {reset_link}

# This link will expire in 1 hour.
# """

#             mail.send(msg)

#         flash("If the email exists, a reset link has been sent.", "info")
#         return redirect(url_for('login'))

#     return render_template('forgot_password.html')

# # --------------------
# # Reset Password
# # --------------------
# @app.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_with_token(token):
#     try:
#         email = s.loads(token, salt='password-reset-salt', max_age=3600)
#     except:
#         flash("The reset link is invalid or expired.", "danger")
#         return redirect(url_for('forgot_password'))

#     if request.method == 'POST':
#         new_password = request.form['password']
#         hashed_password = generate_password_hash(new_password)

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute(
#             "UPDATE users SET password=%s WHERE email=%s",
#             (hashed_password, email)
#         )

#         conn.commit()
#         cur.close()
#         conn.close()

#         flash("Your password has been updated!", "success")
#         return redirect(url_for('login'))

#     return render_template('reset_password.html')

# # --------------------
# # Logout
# # --------------------
# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/login')

# # --------------------
# # Add Note
# # --------------------
# @app.route('/addnote', methods=['GET', 'POST'])
# def addnote():
#     if 'user_id' not in session:
#         return redirect('/login')

#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         user_id = session['user_id']

#         conn = get_db_connection()
#         cur = conn.cursor()

#         cur.execute(
#             "INSERT INTO notes (title, content, user_id) VALUES (%s,%s,%s)",
#             (title, content, user_id)
#         )

#         conn.commit()
#         cur.close()
#         conn.close()

#         return redirect('/viewall')

#     return render_template('addnote.html')

# # --------------------
# # Update Note
# # --------------------
# @app.route('/updatenote/<int:note_id>', methods=['GET', 'POST'])
# def updatenote(note_id):
#     if 'user_id' not in session:
#         return redirect('/login')

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM notes WHERE id=%s AND user_id=%s",
#         (note_id, session['user_id'])
#     )
#     note = cur.fetchone()

#     if not note:
#         return redirect('/viewall')

#     if request.method == 'POST':
#         cur.execute(
#             "UPDATE notes SET title=%s, content=%s WHERE id=%s AND user_id=%s",
#             (request.form['title'], request.form['content'], note_id, session['user_id'])
#         )
#         conn.commit()
#         return redirect('/viewall')

#     cur.close()
#     conn.close()
#     return render_template('updatenote.html', note=note)

# # --------------------
# # View All Notes
# # --------------------
# @app.route('/viewall')
# def viewall():
#     if 'user_id' not in session:
#         return redirect('/login')

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM notes WHERE user_id=%s ORDER BY created_at DESC",
#         (session['user_id'],)
#     )

#     notes = cur.fetchall()
#     cur.close()
#     conn.close()

#     return render_template('viewnotes.html', notes=notes)

# # --------------------
# # Delete Note
# # --------------------
# @app.route('/deletenote/<int:note_id>', methods=['POST'])
# def deletenote(note_id):
#     if 'user_id' not in session:
#         return redirect('/login')

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute(
#         "DELETE FROM notes WHERE id=%s AND user_id=%s",
#         (note_id, session['user_id'])
#     )

#     conn.commit()
#     cur.close()
#     conn.close()

#     return redirect('/viewall')

# # --------------------
# # Search Notes
# # --------------------
# @app.route('/search')
# def search():
#     if 'user_id' not in session:
#         return redirect('/login')

#     search_text = request.args.get('q', '').strip()
#     user_id = session['user_id']

#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute(
#         """
#         SELECT * FROM notes
#         WHERE user_id=%s
#         AND (title LIKE %s OR content LIKE %s)
#         ORDER BY created_at DESC
#         """,
#         (user_id, f"%{search_text}%", f"%{search_text}%")
#     )

#     notes = cur.fetchall()
#     cur.close()
#     conn.close()

#     return render_template('viewnotes.html', notes=notes, search_text=search_text)

# # --------------------
# # Run App
# # --------------------
# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

# --------------------
# App Initialization
# --------------------
app = Flask(__name__)
app.secret_key = "myverysecretkey"

# --------------------
# Mail Configuration
# --------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "sonusyed392@gmail.com"
app.config['MAIL_PASSWORD'] = "hojx yszj liaq qade"

mail = Mail(app)

# --------------------
# Token Serializer
# --------------------
s = URLSafeTimedSerializer(app.secret_key)

# --------------------
# SQLite Database Connection
# --------------------
def get_db_connection():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

# --------------------
# Home
# --------------------
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/viewall')
    return redirect('/login')

# --------------------
# Register
# --------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        if not username or not email or not password:
            flash("All fields required", "danger")
            return redirect('/register')

        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE email=?", (email,))
        if cur.fetchone():
            flash("Email already registered", "danger")
            conn.close()
            return redirect('/register')

        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (?,?,?)",
            (username, email, hashed_pw)
        )

        conn.commit()
        conn.close()

        flash("Registration successful", "success")
        return redirect('/login')

    return render_template('register.html')

# --------------------
# Login
# --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Email and password required", "danger")
            return redirect(url_for('login'))

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['username'] = user['username']
            return redirect(url_for('viewall'))

        flash("Invalid email or password", "danger")

    return render_template('login.html')

# --------------------
# About & Contact
# --------------------
@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # you can later email/store this
        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')

# --------------------
# Forgot Password
# --------------------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if user:
            token = s.dumps(email, salt='password-reset-salt')

            reset_link = url_for(
                'reset_with_token',
                token=token,
                _external=True
            )

            msg = Message(
                subject="Reset Your Password",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )

            msg.body = f"""
Hello {user['username']},

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.
"""
            mail.send(msg)

        flash("If the email exists, a reset link has been sent.", "info")
        return redirect(url_for('login'))

    return render_template('forgot_password.html')

# --------------------
# Reset Password
# --------------------
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash("The reset link is invalid or expired.", "danger")
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE users SET password=? WHERE email=?",
            (hashed_password, email)
        )

        conn.commit()
        conn.close()

        flash("Your password has been updated!", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html')

# --------------------
# Logout
# --------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# --------------------
# Add Note
# --------------------
@app.route('/addnote', methods=['GET', 'POST'])
def addnote():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO notes (title, content, user_id) VALUES (?,?,?)",
            (title, content, user_id)
        )

        conn.commit()
        conn.close()

        return redirect('/viewall')

    return render_template('addnote.html')

# --------------------
# Update Note
# --------------------
@app.route('/updatenote/<int:note_id>', methods=['GET', 'POST'])
def updatenote(note_id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM notes WHERE id=? AND user_id=?",
        (note_id, session['user_id'])
    )
    note = cur.fetchone()

    if not note:
        conn.close()
        return redirect('/viewall')

    if request.method == 'POST':
        cur.execute(
            "UPDATE notes SET title=?, content=? WHERE id=? AND user_id=?",
            (request.form['title'], request.form['content'], note_id, session['user_id'])
        )
        conn.commit()
        conn.close()
        return redirect('/viewall')

    conn.close()
    return render_template('updatenote.html', note=note)

# --------------------
# View All Notes
# --------------------
@app.route('/viewall')
def viewall():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM notes WHERE user_id=? ORDER BY created_at DESC",
        (session['user_id'],)
    )

    notes = cur.fetchall()
    conn.close()

    return render_template('viewnotes.html', notes=notes)

# --------------------
# Delete Note
# --------------------
@app.route('/deletenote/<int:note_id>', methods=['POST'])
def deletenote(note_id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM notes WHERE id=? AND user_id=?",
        (note_id, session['user_id'])
    )

    conn.commit()
    conn.close()

    return redirect('/viewall')

# --------------------
# Search Notes
# --------------------
@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect('/login')

    search_text = request.args.get('q', '').strip()
    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM notes
        WHERE user_id=?
        AND (title LIKE ? OR content LIKE ?)
        ORDER BY created_at DESC
        """,
        (user_id, f"%{search_text}%", f"%{search_text}%")
    )

    notes = cur.fetchall()
    conn.close()

    return render_template('viewnotes.html', notes=notes, search_text=search_text)

# --------------------
# Run App
# --------------------
if __name__ == '__main__':
    app.run(debug=True)
