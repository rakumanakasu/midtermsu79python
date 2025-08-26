from app import app, requests, render_template


@app.get('/cart')
def cart():
    return render_template('cart.html')
