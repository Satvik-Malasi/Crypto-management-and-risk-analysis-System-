# from flask import Flask, render_template, request, redirect, url_for
# app = Flask(__name__)
# stocks = []
# @app.route('/', methods=['GET', 'POST'])
# def dashboard():
#     if request.method == 'POST':
#         if 'add_stock' in request.form:
#             email = (request.form.get('email') or '').strip()
#             stock_name = (request.form.get('stock_name') or '').strip()
#             quantity = (request.form.get('quantity') or '').strip()
#             if stock_name and quantity:  
#                 try:
#                     quantity = int(quantity)
#                     stocks.append({
#                         'email': email,
#                         'stock_name': stock_name.upper(),
#                         'quantity': quantity
#                     })
#                 except ValueError:
#                     pass
#             return redirect(url_for('dashboard'))
#         elif 'generate_report' in request.form:
#             return redirect(url_for('dashboard'))
#     return render_template('dashboard.html', stocks=stocks)
# if __name__ == '__main__':
#     app.run(debug=True, port=5001)


from flask import Flask, render_template, request, redirect, url_for, flash
from backendConnection.report_pipeline import generate_and_send_report  # your backend logic

app = Flask(__name__)
app.secret_key = "super_secret_key"

# temporary in-memory storage
stocks = []
user_email = None  # store one email only

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    global user_email, stocks

    if request.method == 'POST':
        # === Add Stock ===
        if 'add_stock' in request.form:
            email = (request.form.get('email') or '').strip()
            stock_name = (request.form.get('stock_name') or '').strip().upper()
            quantity = (request.form.get('quantity') or '').strip()

            # If email not set yet, take the first one
            if not user_email:
                if not email:
                    flash("⚠️ Please enter your email ID.", "error")
                    return redirect(url_for('dashboard'))
                user_email = email
            elif email and email != user_email:
                flash(f"⚠️ You can only use one email ({user_email}) for this report.", "error")
                return redirect(url_for('dashboard'))

            # Validate stock info
            if not stock_name or not quantity:
                flash("⚠️ Stock name and quantity are required.", "error")
                return redirect(url_for('dashboard'))

            try:
                quantity = int(quantity)
                stocks.append({'stock_name': stock_name, 'quantity': quantity})
                flash(f"✅ Added {stock_name} ({quantity}) to your portfolio.", "success")
            except ValueError:
                flash("⚠️ Quantity must be a number.", "error")

            return redirect(url_for('dashboard'))

        # === Generate Report ===
        elif 'generate_report' in request.form:
            if not stocks:
                flash("⚠️ Please add at least one stock before generating the report.", "error")
                return redirect(url_for('dashboard'))

            if not user_email:
                flash("⚠️ Please enter an email ID before generating the report.", "error")
                return redirect(url_for('dashboard'))

            # Build holdings dict: {'AAPL': 20, 'MSFT': 10, ...}
            holdings = {s['stock_name']: s['quantity'] for s in stocks}

            try:
                generate_and_send_report(holdings, user_email)
                flash(f"✅ Portfolio report sent successfully to {user_email}.", "success")
            except Exception as e:
                flash(f"❌ Error while generating/sending report: {str(e)}", "error")

            # Optional: clear data for next session
            stocks.clear()
            user_email = None
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', stocks=stocks, user_email=user_email)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
