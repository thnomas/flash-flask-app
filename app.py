from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

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

print(__name__)

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



    
@app.get("/login")
def login():
    form  = LoginForm()
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)