from application import app, app_name, db
from application.forms import LoginForm, RegistrationForm, RequestPasswordResetForm, ResetPasswordForm
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from application.models import User
from application.email import send_password_reset_mail


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title=app_name, current_user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        print("user is already authenticated")
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first() is not None or User.query.filter_by(username=form.username.data).first() is not None:
            flash("User already exists.")
            return redirect(url_for('login'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash("Now you are a registered user :)")
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('index'))


@app.route('/request_password_reset', methods=["GET", "POST"])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("You have not already registered with us. Please signup.")
            return redirect(url_for('register'))
        send_password_reset_mail(user)
        flash("A password reset link has been sent to your email.")
        return redirect(url_for('login'))
    return render_template("request_password_reset.html", title="Request password reset", form=form, current_user=current_user)


@app.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password(token):
    #flash(token)
    if current_user.is_authenticated:
        flash("user is already authenticated")
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        flash("user not found")
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password1.data)
        db.session.commit()
        flash("Your password has been reset")
        return redirect(url_for('login'))
    return render_template('reset_password.html', title="Reset Password", form=form, current_user=current_user)
