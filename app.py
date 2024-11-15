from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

class CreateAccountForm(FlaskForm):
    fname = StringField('First Name', [DataRequired()])
    lname = StringField('Last Name', [DataRequired()])
    email = StringField(
        'Email', [DataRequired(), Email("Invalid email address.")])
    password = PasswordField('Password', [DataRequired(), Length(
        min=10, max=20, message="Password must have between 10 and 20 characters")])
    submit = SubmitField(label='Submit')


class LoginForm(FlaskForm):
    email = StringField(
        'Email', [DataRequired(), Email("Invalid email address.")])
    password = PasswordField('Password', [DataRequired(), Length(
        min=10, max=20, message="Password must have between 10 and 20 characters")])
    submit = SubmitField(label='Login')


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
Bootstrap(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User: {self.fname} {self.lname}>'


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
def login():
    db.create_all()
    print("Database created.")
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        query = text(
            "SELECT EXISTS(SELECT 1 FROM User WHERE email=:email AND password=:password)")
        result = db.session.execute(
            query, {"email": email, "password": password})
        exists = result.scalar()
        if exists:
            return redirect(url_for('home'))
        else:
            boolean = False
            return render_template("login.html", form=login_form, boolean=boolean)
    return render_template("login.html", form=login_form)


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    create_account_form = CreateAccountForm()
    if create_account_form.validate_on_submit():
        new_user = User(
            fname=create_account_form.fname.data,
            lname=create_account_form.lname.data,
            email=create_account_form.email.data,
            password=create_account_form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        return redirect(url_for('login'))
    return render_template("create-account.html", form=create_account_form)


@app.route("/delete_database")
def delete_database():
    db.drop_all()
    print("Database deleted.")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
