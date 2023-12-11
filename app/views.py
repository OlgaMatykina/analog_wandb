from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
from flask import url_for
from flask import request
from urllib.parse import urlsplit

from app.utils import get_project_names, get_runs, make_image

import matplotlib.pyplot as plt

@app.route('/')
@app.route('/index')
@login_required
def index():
    projects = get_project_names(db, current_user.username)
    return render_template("index.html",
        title = 'Home',
        projects = projects)

@app.route('/project/<project>', methods=['GET', 'POST'])
@login_required
def project(project):
    runs = get_runs(db, current_user.username, project)
    names = []
    for run in runs:
        names.append(run.name)
    if request.method == 'GET':
        make_image(db, runs)
        return render_template('project.html', runs=names, checked=names)
    elif request.method == 'POST':
        checked = request.form.getlist('hello')
        # make_image(db, checked)
        return render_template('project.html', runs=names, checked=names)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @login_required
# def index():
#     return render_template("index.html", title='Home Page', experiments=experiments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    experiments = [
        {'author': user, 'name': 'Test post #1'},
        {'author': user, 'name': 'Test post #2'}
    ]
    return render_template('user.html', user=user, experiments=experiments)