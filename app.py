from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

# WTForm to create account
class CreateAccountForm(FlaskForm):
    fname = StringField('First Name', [DataRequired()])
    lname = StringField('Last Name', [DataRequired()])
    email = StringField(
        'Email', [DataRequired(), Email("Invalid email address.")])
    password = PasswordField('Password', [DataRequired(), Length(
        min=10, max=50, message="Password must have between 10 and 20 characters")])
    submit = SubmitField(label='Submit')


# WTForm to login
class LoginForm(FlaskForm):
    email = StringField(
        'Email', [DataRequired(), Email("Invalid email address.")])
    password = PasswordField('Password', [DataRequired(), Length(
        min=10, max=50, message="Password must have between 10 and 20 characters")])
    submit = SubmitField(label='Login')


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)

# SQLite database setup
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User: {self.fname} {self.lname}>'


# Main route when user logs in: index.html
@app.route("/home")
def home():
    return render_template("index.html")

# Default route: login.html
@app.route("/", methods=["GET", "POST"])
def login():
    # Creates SQLite database instance
    db.create_all()
    print("Database created.")
    # WTForm login form instance
    login_form = LoginForm()
    # POST request
    if login_form.validate_on_submit():
        # Gets email input value
        email = login_form.email.data
        # Gets password input value
        password = login_form.password.data
        # Secure query setup to check if user exists with email and password above
        query = text(
            "SELECT EXISTS(SELECT 1 FROM User WHERE email=:email AND password=:password)")
        result = db.session.execute(
            query, {"email": email, "password": password})
        exists = result.scalar()
        if exists:
            # Flag to send to login.html
            user_exists = True
            # If user account exists, log in
            return render_template("index.html", user_exists=user_exists)
        else:
            # Flag to send to login.html
            boolean = False
            # If user account doesn't exist, do nothing
            return render_template("login.html", form=login_form, boolean=boolean)
    # GET request
    return render_template("login.html", form=login_form)

# Create new account route
@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    # WTForm create account form instance
    create_account_form = CreateAccountForm()
    # POST request
    if create_account_form.validate_on_submit():
        # New user object
        new_user = User(
            fname=create_account_form.fname.data,
            lname=create_account_form.lname.data,
            email=create_account_form.email.data,
            password=create_account_form.password.data
        )
        # Secure query setup to check if email exists
        query = text(
            "SELECT EXISTS(SELECT 1 FROM User WHERE email=:email)")
        result = db.session.execute(
            query, {"email": new_user.email})
        email_exists = result.scalar()
        if email_exists:
            # Flag to send to create-account.html
            boolean = False
            # If email exists, do nothing
            return render_template("create-account.html", form=create_account_form, boolean=boolean)
        else:
            # Add new user object to database
            db.session.add(new_user)
            db.session.commit()
            print(new_user)
            return redirect(url_for('login'))
    # GET request
    return render_template("create-account.html", form=create_account_form)

# Delete account route
@app.route("/delete_database")
def delete_database():
    # Deletes database
    db.drop_all()
    print("Database deleted.")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
