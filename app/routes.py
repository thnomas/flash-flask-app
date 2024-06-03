from flask import render_template, url_for, flash, redirect
from app.forms import LoginForm, RegistrationForm
from app.models import User, Deck
from app import app

decks = [
    {
        'author': 'thomas mooney',
        'title': 'Dutch Vocab',
        'date_created': '2024-09-12'
    },
    {
        'author': 'ciara gibbons',
        'title': 'Every Capital',
        'date_created': '2024-08-12'
    }
]

@app.get("/")
def index():
    return render_template('index.html', decks=decks, title="home")


@app.get("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == "password":
            flash(f'Youve been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful', 'danger')
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

