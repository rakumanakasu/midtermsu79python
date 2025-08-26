from app import app, render_template
import sqlite3

# @app.get('/getData')
# def getData():
#     connection = sqlite3.connect('su79_database.sqlite3')
#     connection.row_factory = sqlite3.Row
#     cursor = connection.cursor()
#     rows = cursor.execute("SELECT * FROM products").fetchall()
#
#     products = [dict(row) for row in rows]
#
#     return render_template('render_product.html', products=products)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    connection = sqlite3.connect('su79_database.sqlite3')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    rows = cursor.execute("SELECT * FROM products").fetchall()
    products = [dict(row) for row in rows]
    return render_template('home.html', products=products, error='')


@app.route('/detail/<int:pro_id>')
def detail(pro_id):
    product = None
    error = ''
    try:
        connection = sqlite3.connect('su79_database.sqlite3')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        row = cursor.execute("SELECT * FROM products WHERE id=?", (pro_id,)).fetchone()
        if row:
            product = dict(row)
        else:
            error = "Product not found"
    except Exception as e:
        error = str(e)
    return render_template('detail.html', product=product, error=error)
