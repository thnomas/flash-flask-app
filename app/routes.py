from flask import render_template, url_for, flash, redirect, request
from app.forms import LoginForm, RegistrationForm, UpdateAccountForm, DeckForm
from app.models import User, Deck
from app import app, db, bcrypt
import secrets
from PIL import Image
import os
from flask_login import login_user, logout_user, login_required, current_user

@app.get("/")
@login_required
def index():
    decks = Deck.query.all()
    return render_template('index.html', decks=decks, title="Home")

@app.get("/review")
def review():
    return render_template('review.html')

@app.get("/quiz")
def quiz():
    return render_template('quiz.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}. You can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex +f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account have been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/create_deck", methods=['GET', 'POST'])
@login_required
def create_deck():
    decks = Deck.query.filter_by(user_id=current_user.id).all()
    form = DeckForm()
    if form.validate_on_submit():
        deck = Deck(title=form.title.data, description=form.description.data, created_by=current_user)
        db.session.add(deck)
        db.session.commit()
        flash('Deck created', 'success')
        return redirect(url_for('create_deck'))

    return render_template('create_deck.html', form=form, decks=decks)