from app import app, request, render_template, mail, BOT_TOKEN, CHAT_ID
from flask import flash
from flask_mail import Message
import json, requests, io
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')

        cart_json = request.form.get('cart_data')
        try:
            cart_list = json.loads(cart_json) if cart_json else []
        except json.JSONDecodeError:
            cart_list = []

        total = sum(item.get('qty', 0) * item.get('price', 0) for item in cart_list)

        # Email invoice
        invoice_html = render_template('email_invoice.html',
                                       name=name,
                                       phone=phone,
                                       email=email,
                                       address=address,
                                       cart_list=cart_list,
                                       total=total)

        msg = Message(subject='Your Order Invoice',
                      recipients=[email],
                      html=invoice_html)

        try:
            mail.send(msg)

            # Telegram invoice
            message_lines = [
                f"<strong>🧾 Invoice #{date.today().strftime('%Y%m%d')}</strong>",
                f"<code>👤 {name}</code>",
                f"<code>📧 {email}</code>",
                f"<code>📆 {date.today()}</code>",
                f"<code>🏠 {address}</code>",
                "<code>=======================</code>",
            ]
            for i, item in enumerate(cart_list, start=1):
                title = item.get('title') or item.get('name') or 'Unknown'
                qty = item.get('qty', 0)
                price = item.get('price', 0)
                message_lines.append(f"<code>{i}. {title} x{qty} = ${price}</code>")

            message_lines.append("<code>=======================</code>")
            message_lines.append(f"<code>💵 Total: ${total:.2f}</code>")

            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": "\n".join(message_lines), "parse_mode": "HTML"}
            )

            # PDF generation (optional)
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.drawString(50, 750, f"Invoice for {name}")
            pdf.drawString(50, 735, f"Email: {email}")
            pdf.drawString(50, 720, f"Phone: {phone}")
            pdf.drawString(50, 705, f"Address: {address}")
            pdf.drawString(50, 690, "-" * 40)

            y = 670
            for i, item in enumerate(cart_list, start=1):
                title = item.get('title') or item.get('name') or 'Unknown'
                qty = item.get('qty', 0)
                price = item.get('price', 0)
                pdf.drawString(50, y, f"{i}. {title} x{qty} = ${price}")
                y -= 20

            pdf.drawString(50, y - 10, f"Total: ${total:.2f}")
            pdf.save()
            buffer.seek(0)

            # Success flag for template
            return render_template('checkout.html', order_success=True)

        except Exception as e:
            flash(f'Failed to send invoice: {str(e)}', 'danger')

    return render_template('checkout.html', order_success=False)
