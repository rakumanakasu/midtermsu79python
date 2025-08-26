from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
import json
import requests
from datetime import date
from dotenv import load_dotenv
import os
# import iod
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load environment variables (if using .env)
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_flask_secret_key'

# Mail configuration
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "chhayheang974@gmail.com"
app.config['MAIL_PASSWORD'] = "jddyoqowcuchaewr"
app.config['MAIL_DEFAULT_SENDER'] = 'chhayheang974@gmail.com'

# --- Upload Folder ---
# This will create a folder named "uploads" inside "static" automatically if it doesn't exist
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mail = Mail(app)

# Telegram config
BOT_TOKEN = '7511564601:AAF4Vh37VeaF-rA_55HnCgu40epIAPuD37A'
CHAT_ID = '1253456651'

import route

if __name__ == '__main__':
    app.run(debug=True)

# @app.get('/detail/<int:pro_id>')
# def detail(pro_id):
#     return f"{pro_id}"
