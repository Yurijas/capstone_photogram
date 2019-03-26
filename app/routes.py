import os
import secrets
# from PIL import Image
from app import app, db , mail
from flask import render_template, url_for, redirect, flash, request
from app.forms import PostForm, LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm, EditProfileForm
from app.models import Post, User
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # fake data for a while
    # person = User.query.filter_by(username=username).first()
    # posts = [
    #     {'author': person, 'body': 'Test post #1'},
    #     {'author': person, 'body': 'Test post #2'}
    # ]
    return render_template('index.html')

# /index/<username>
# person=person, , posts=posts

@login_required
@app.route('/posts/<username>', methods=['GET', 'POST'])
def posts(username):
    form = PostForm()
    # url = url_for('static', filename='profile_pics/' + current_user.url)
    # query database for proper person
    person = User.query.filter_by(username=username).first()
    # when form is submitted appends to post lists, re-render posts page
    if form.validate_on_submit():
        # setting the name of the folder
        post_foldername = current_user.username
        # pointing to directory for user image folder
        img_path = os.path.abspath(os.path.dirname(__file__)) + '/static/images/'
        # making folder for each user
        if not os.path.exists(img_path + post_foldername):
            os.mkdir(img_path + post_foldername)

        # pointing to directory for images
        post_basedir = os.path.abspath(os.path.dirname(__file__)) + '/static/images/' + post_foldername + '/'

        # setting the name of image
        num = len(current_user.posts)
        post_filename = str(num) + '_post.png'
        # save pic
        url = post_basedir + post_filename
        form.pic.data.save(url)

        # resize with Pillow
        # im = Image.open(url)
        # Image.resize((100,100), Image.ANTIALIAS)
        # url.save(url)


        post = Post(desc=form.desc.data, user_id=current_user.id, url=url)
        # add post variable to database stage, then commit
        db.session.add(post)
        db.session.commit()
        flash('Your photo has been posted!.')
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
            username = form.username.data,
            email = form.email.data
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

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_gn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
#
#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#
#     return picture_fn

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # if form.url.data:
        #     picture_file = save_picture(form.url.data)
        #     current_user.url = picture_file
        # pointing to directory for images
        profile_basedir = os.path.abspath(os.path.dirname(__file__)) + '/static/profile_images/'

        # setting the name of image
        profile_filename = current_user.username+ '_profile.png'

        # save pic
        form.pic.data.save(profile_basedir + profile_filename)

        current_user.url = profile_filename
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your changes have been saved. Please go back to your account page.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.pic.data = current_user.url
        form.bio.data = current_user.bio
    return render_template('edit_profile.html', title='Edit Profile', form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body  = f''' To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no change will occur. '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
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


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
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
