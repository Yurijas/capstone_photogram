from app import app, db
from flask import render_template, url_for, redirect, flash, request
from app.forms import PostForm, LoginForm, RegisterForm
from app.models import Post, User
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # fake data for a while
    people = [
        {
            'id': 1001,
            'username': 'user1',
            'desc': 'photo',
            'date_posted': 3.98

        },
        {
            'id': 1002,
            'username': 'user2',
            'desc': 'photo',
            'date_posted': 3.98
        },
        {
            'id': 1003,
            'username': 'user3',
            'desc': 'photo',
            'date_posted': 3.98
        },
        {
            'id': 1004,
            'username': 'user4',
            'desc': 'photo',
            'date_posted': 3.98
        }
    ]
    return render_template('index.html', people=people)

@login_required
@app.route('/posts/<username>', methods=['GET', 'POST'])
def posts(username):
    form = PostForm()
    # query database for proper person
    person = User.query.filter_by(username=username).first()
    # when form is submitted appends to post lists, re-render posts page
    if form.validate_on_submit():
        desc = form.desc.data
        post = Post(desc=desc, user_id=current_user.id)
        # add post variable to database stage, then commit
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts', username=username))

    return render_template('posts.html', person=person, title='Posts', form=form, username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))

    form = LoginForm()
    # check if form is submitted, log user in if so
    if form.validate_on_submit():
        #
        user = User.query.filter_by(username=form.username.data).first()
        # if user doesn't exit current page

        print(user.check_password(form.password.data))
        if user is None or not user.check_password(form.password.data):
            flash('Credentials are incorrect.')
            return redirect(url_for('login'))
        # if user does exist, and credentials are correct, log them in and send them to their profile page
        login_user(user, remember=form.remember_me.data)
        flash('You are now logged in!')
        return redirect(url_for('posts', username=current_user.username))

    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            url = form.url.data,
            age = int(form.age.data),
            bio = form.bio.data
        )

        # set the password hash
        user.set_password(form.password.data)
        # add to stage and commit to db, then flash and return
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now registered!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
