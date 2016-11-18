import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

print("Initializing app...")

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='asd',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """
    connects to the specific database.
    :return:
    """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def cli_initdb():
    init_db()
    print("Initialized the database")


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    if error:
        print(str(error))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['secret_keytag'] != app.config['SECRET_KEY']:
            error = "Incorrect keytag. Contact the administrator."
        db = get_db()
        user_auth_cur = db.execute('select username from authentication where username = ?', [request.form['username']])
        user_auth_entries = user_auth_cur.fetchall()
        if len(user_auth_entries) != 0:
            error = "User already exists!"
        else:
            db.execute('insert into authentication(username, password) values (?, ?)',
                       [request.form['username'], request.form['password']])
            db.commit()
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('Successfully registered new user.')
            return redirect(url_for('show_entries'))
    return render_template('register.html', error=error)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries(title,text,username) values (?,?,?)',
               [request.form['title'], request.form['text'], session['username']])
    db.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        auth_cur = db.execute('select username, password from authentication '
                              'where username = ?', [request.form['username']])
        auth_entries = auth_cur.fetchall()
        if len(auth_entries) == 0:
            error = 'Unable to find username'
        elif auth_entries[0][1] != request.form['password']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = auth_entries[0][0]
            flash('You were logged in.')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('show_entries'))


@app.route("/")
def show_entries():
    db = get_db()
    cur = db.execute('select title, text, username from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

print("App loaded...")
# app.run()
