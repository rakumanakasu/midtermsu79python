from app import app, requests, render_template

@app.get('/support')
def about():
    return render_template('support.html')