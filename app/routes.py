from app import app, db , mail
# from PIL import image
from flask import render_template, url_for, redirect, flash, request
from app.forms import PostForm, LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm
from app.models import Post, User
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message


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



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body  = f''' To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no change will occur. '''
    mail.send(msg)


app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # set the password hash
        user.set_password(form.password.data)
        user.password = user.set_password(form.password.data)
        # add to stage and commit to db, then flash and return
        db.session.commit()
        flash('Your password has been updated!')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
