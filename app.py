# Import the needed librarys from flask and sessions.
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

# Create the web app in flask.
app = Flask(__name__)

# Configure the sessions in the web app.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define the main route as both a POST and GET route.
@app.route('/', methods = ['POST', 'GET'])
def index():
    # If the method is POST, the user will be entering the calculations.
    if request.method == 'POST':
        # Clear all the values from the session if there are any.
        session.pop('message', None)
        session.pop('total', None)
        session.pop('subtotal', None)
        session.pop('taxAmount', None)

        # Try to receive the input from the user and validate the input.
        try:
            price = float(request.form['price'])
            amount = float(request.form['amount'])
            tax = float(request.form['tax'])
        # If it fails to validate, add the error message to the session and redirect back to the GET page.
        except:
            session['message'] = 'You must fill out all input fields.'
            return redirect(url_for('index'))

        # If everything worked so far, calculate the subtotal, tax, and total.
        subtotal = (price * amount)
        tax_amount = (price * amount) * (tax / 100.0)
        total = (price * amount) * (1 + (tax / 100.0))

        # Save all the results to the session.
        session['subtotal'] = "${:,.2f}". format(subtotal)
        session['taxAmount'] = "${:,.2f}". format(tax_amount)
        session['total'] = "${:,.2f}". format(total)

        # Then redirect the user back to the GET form of the page.
        return redirect(url_for('index'))

    else:
        # Just render the page if it is a GET request.
        return render_template('index.html')

# The 404 handler.
@app.errorhandler(404)
def not_found(e):
  return render_template('404.html'), 404

# Start the web application.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')