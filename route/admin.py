from app import app, flash, url_for, redirect, session, request, render_template
import sqlite3

app.secret_key = "741e4fa4-f067-4aec-b48d-deb18e9cca92"

@app.before_request
def protect_admin_routes():
    # Routes that require login
    protected_paths = ['/admin', '/product']  # add more if needed

    # If the requested path starts with any protected path AND user not logged in
    if any(request.path.startswith(p) for p in protected_paths) and not session.get('user_id'):
        flash('You must log in first', 'warning')
        return redirect(url_for('login'))
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('su79_database.sqlite3')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'danger')
            return render_template('admin/login.html')

    return render_template('admin/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        flash('You must log in first', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('su79_database.sqlite3')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    # Convert sqlite3.Row objects to dicts for JSON
    products_list = [dict(p) for p in products]

    return render_template('admin/index.html', products=products_list)


