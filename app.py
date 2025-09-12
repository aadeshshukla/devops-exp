from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)

# In-memory storage for registered users (for demonstration purposes)
# In a real application, you would use a database.
users = []

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    - GET: Displays the registration form.
    - POST: Processes the form submission and adds the user.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if name and email:
            users.append({'name': name, 'email': email})
            # Redirect to the success page after registration
            return redirect(url_for('success'))
    # Display the registration form for GET requests
    return render_template('register.html')

@app.route('/success')
def success():
    """Displays a success message after registration."""
    return render_template('success.html')

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True)
