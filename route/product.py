import os

from werkzeug.utils import secure_filename

from app import app, render_template, request, jsonify
import sqlite3

# List products
@app.route('/products')
def products():
    conn = sqlite3.connect('su79_database.sqlite3')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()
    return render_template('admin/product.html', products=[dict(row) for row in rows])

# Add productz
@app.route('/products/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    category = request.form.get('category')
    price = request.form.get('price')

    image_file = request.files.get('image')
    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = ''

    conn = sqlite3.connect('su79_database.sqlite3')
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, category, price, image) VALUES (?, ?, ?, ?)",
                (name, category, price, filename))
    product_id = cur.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': 'Product added successfully',
        'product': {
            'id': product_id,
            'name': name,
            'category': category,
            'price': price,
            'image': filename
        }
    })


# Edit product
@app.route('/products/edit/<int:id>', methods=['POST'])
def edit_product(id):
    name = request.form.get('name')
    category = request.form.get('category')
    price = request.form.get('price')

    image_file = request.files.get('image')
    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        # Use the old image if no new file uploaded
        filename = request.form.get('current_image', '')

    conn = sqlite3.connect('su79_database.sqlite3')
    cur = conn.cursor()
    cur.execute("UPDATE products SET name=?, category=?, price=?, image=? WHERE id=?",
                (name, category, price, filename, id))
    conn.commit()
    conn.close()
    return jsonify({
        'success': True,
        'message': 'Product updated successfully',
        'product': {
            'id': id,
            'name': name,
            'category': category,
            'price': price,
            'image': filename
        }
    })

# Delete product
@app.route('/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn = sqlite3.connect('su79_database.sqlite3')
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Product deleted successfully'})
