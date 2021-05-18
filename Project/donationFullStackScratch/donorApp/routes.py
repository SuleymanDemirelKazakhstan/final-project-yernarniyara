from werkzeug.security import check_password_hash, generate_password_hash

from donorApp import app, db
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user

from donorApp.models import User

db.create_all()


@app.route('/')
def main():
    return render_template('base.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('my_profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            redir_next_page = request.args.get('next_page')

            redirect(redir_next_page)
        else:
            flash('Fill username and password correctly')

    else:
        flash('Fill username and password')
    return render_template('my_login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/register-donor', methods=['GET', 'POST'])
def register_donor():
    username = request.form.get('username')
    password = request.form.get('password')
    password_retype = request.form.get('password_retype')
    email = request.form.get('email')

    existing_email = User.query.filter_by(email=email).first()
    existing_username = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        if not (username, password_retype, password, email):
            flash('Fill all')
        elif password_retype != password:
            flash('Password doesnt match')
        elif existing_email == email or existing_username == username:
            flash('Email or username is already taken')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(username=username, password=hash_pwd, email=email)

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))
    return render_template('register_donor.html')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    if response.status_code == 401:
        return render_template('404notfound.html')
    return response



if __name__ == '__main__':
    app.run()
