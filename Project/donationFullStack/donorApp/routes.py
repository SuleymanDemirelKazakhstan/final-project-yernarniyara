import os

from sqlalchemy.sql.functions import user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from donorApp import app, db, UPLOAD_FOLDER
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
import json

from donorApp.helper_functions import *

from donorApp.models import *

db.create_all()


@app.route('/')
def main():
    return render_template('index.html', title='Главная - Донор', )


@app.route('/profile')
@login_required
def profile():
    donor, donor_data = get_donor_data_json()

    donor_data = json.loads(donor_data)

    latest_appointment = db.session.query(Donation, BloodCenter).join(BloodCenter).filter(
        Donation.donor_id == donor.id).filter(Donation.blood_center_id == BloodCenter.id).order_by(
        Donation.id.desc()).first()

    return render_template('profile.html', title='Донор - Мой профиль', donor=donor, donor_data=donor_data,
                           latest_appointment=latest_appointment)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            donor_user = find_user(username)

            if donor_user and check_password_hash(donor_user.password, password):
                login_user(donor_user)

                return redirect(url_for('profile', username=username))
            else:
                flash('Заполните логин и пароль правильно')

        else:
            flash('Заполните логин и пароль')
        return render_template('login.html', title='Донор - Войти')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/register-donor', methods=['GET', 'POST'])
def register_donor():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        password_retype = request.form.get('password_retype')
        email = request.form.get('email')

        print(username, password, password_retype, email)

        existing_email = User.query.filter_by(email=email).first()
        existing_username = find_user(username)

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

                new_user_id = find_user(username).id

                print(new_user_id)
                new_donor = Donor(user_id=new_user_id, points=0, data=json.dumps(initial_data))
                db.session.add(new_donor)
                db.session.commit()

                return redirect(url_for('login'))
        return render_template('registration.html', title='Донор - Регистрация')


@app.route('/blood-map', methods=['GET'])
def blood_map():
    return render_template('map.html', title='Донор - Где сдать кровь?')


@app.route('/faq', methods=['GET'])
def faq():
    return render_template('frequentquestions.html', title='Донор - FAQ')


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')
    age = request.form.get('age')
    profile_image = request.files.get('profile_image')

    donor, donor_data = get_donor_data_json()
    donor_data = change_donor_data_type(donor_data)
    dict_donor_data = json.loads(donor_data)

    if request.method == 'POST':

        dict_donor_data['main_data']['first_name'] = first_name
        dict_donor_data['main_data']['last_name'] = last_name
        dict_donor_data['main_data']['gender'] = gender
        dict_donor_data['main_data']['age'] = age

        if profile_image is not None:
            extension = os.path.splitext(profile_image.filename)[1]

            if extension != '':
                profile_image.filename = current_user.username + '-profile-image' + extension
                dict_donor_data['main_data']['profile_image'] = os.path.join('profile_pics',
                                                                             secure_filename(profile_image.filename))
                profile_image.save(os.path.join(UPLOAD_FOLDER, secure_filename(profile_image.filename)))

        donor.data = json.dumps(dict_donor_data)
        db.session.commit()

    return render_template('editprofile.html', title='Донор - Изменение профиля', donor=donor,
                           donor_data=dict_donor_data)


@app.route('/edit-contacts', methods=['GET', 'POST'])
@login_required
def edit_contacts():
    donor, donor_data = get_donor_data_json()

    donor_data = change_donor_data_type(donor_data)
    dict_donor_data = json.loads(donor_data)

    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        email = request.form.get('email')

        dict_donor_data['contacts']['phone_number'] = phone_number
        dict_donor_data['contacts']['address'] = address
        dict_donor_data['contacts']['email'] = email

        donor_user = find_user(current_user.username)
        donor_user.email = email

        donor.data = json.dumps(dict_donor_data)
        db.session.commit()

    return render_template('editprofile-1.html', title='Донор - Изменение профиля', donor=donor,
                           donor_data=dict_donor_data)


@app.route('/edit-fullprofile', methods=['GET', 'POST'])
@login_required
def edit_fullprofile():
    donor, donor_data = get_donor_data_json()
    donor_data = change_donor_data_type(donor_data)
    dict_donor_data = json.loads(donor_data)

    if request.method == 'POST':
        height = request.form.get('height')
        weight = request.form.get('weight')
        blood_type = request.form.get('blood_type')

        donor, donor_data = get_donor_data_json()
        dict_donor_data = json.loads(donor_data)

        dict_donor_data['medical_data']['height'] = height
        dict_donor_data['medical_data']['weight'] = weight
        dict_donor_data['medical_data']['blood_type'] = blood_type

        donor.data = json.dumps(dict_donor_data)
        db.session.commit()

    return render_template('editprofile-1-1.html', title='Донор - Изменение профиля', donor_data=dict_donor_data)


@app.route('/edit-password', methods=['GET', 'POST'])
@login_required
def edit_password():
    if request.method == 'POST':
        username = current_user.username
        db_old_password = find_user(username).password
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        new_password_repeat = request.form.get('new_password_repeat')

        existing_username = find_user(username)
        print(existing_username)

        old_password_hash = generate_password_hash(old_password)

        if existing_username is not None:
            print('not none')
            if check_password_hash(old_password_hash, db_old_password):
                print('true')
                if new_password_repeat == new_password:
                    print('true')
                    existing_username.password = generate_password_hash(new_password)
                    db.session.commit()
                    flash('Пароль успешно изменен')
            else:
                flash('Старый пароль введен неверно')
        else:
            flash('Не существует такого пользователя')

    return render_template('editprofile-1-1-1.html', title='Донор - Изменение профиля ')


@app.route('/achievements', methods=['GET'])
@login_required
def achievements():
    return render_template('achievements.html', title='Донор - Достижения')


@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    donor, donor_data = get_donor_data_json()
    donor_data = json.loads(donor_data)

    blood_center = BloodCenter.query.all()

    available_time = 0
    extra_data = 0
    data_commited = 0
    selected_blood_center = ''
    selected_blood_center_name = ' '

    selected_time = get_cur_time()
    date_time_for_donation = get_cur_time()

    if request.method == 'POST':
        blood_center = request.form.get('blood_center')
        time = request.form.get('date')

        selected_blood_center = int(blood_center)
        selected_blood_center_name = BloodCenter.query.filter_by(id=selected_blood_center).first().name

        available_time = db.session.query(DonationTime).join(BloodCenter).filter(
            DonationTime.blood_center_id == BloodCenter.id).filter(BloodCenter.id == blood_center).filter(
            DonationTime.is_available == False).all()

        extra_data = 1

        if time is not None:
            selected_time = DonationTime.query.filter_by(id=int(time)).first()
            print(selected_time.donation_time)
            new_donation = Donation(blood_center_id=selected_blood_center, donor_id=donor.id, donation_cost_fk=1,
                                    date_time=selected_time.donation_time, is_submitted=False)
            selected_time.is_available = True
            db.session.add(new_donation)
            db.session.commit()
            data_commited = 1

            date_time_for_donation = selected_time.donation_time

    return render_template('appointment.html', title='Донор - Достижения', donor=donor, donor_data=donor_data,
                           blood_center=blood_center, available_time=available_time, extra_data=extra_data,
                           selected_blood_center=selected_blood_center,
                           selected_blood_center_name=selected_blood_center_name, data_commited=data_commited,
                           date_time=date_time_for_donation)


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        new_password_repeat = request.form.get('new_password_repeat')

        existing_username = find_user(username)
        print(existing_username)
        if existing_username is not None:
            if new_password_repeat == new_password:
                print(existing_username.password)
                existing_username.password = generate_password_hash(new_password)
                db.session.commit()
                return redirect(url_for('login'))

        else:
            flash('Не существует такого пользователя')
    return render_template('forgot-password.html', title='Донор - Восстановить пароль')


@app.route('/bonuses', methods=['GET', 'POST'])
def bonuses():
    analysis_type = request.args.get('bonus')
    print(analysis_type)
    if analysis_type is not None:
        print('in')
        donor, donor_data = get_donor_data_json()
        if donor.points >= 100:
            achievement = db.session.query(Achievements).join(AchievementType).filter(
                Achievements.achievement_type_id == AchievementType.id).filter(
                AchievementType.name == analysis_type).first()

            achievement.quantity = int(achievement.quantity) - 1
            donor.points = int(donor.points) - 100

            random_code = randomize_string()

            new_pending = PendingAchievements(donor_id=donor.id, achievements_id=achievement.id, is_submitted=False,
                                              data=random_code)
            db.session.add(new_pending)
            db.session.commit()

            return redirect(url_for('mybonuses'))

    return render_template('bonuses.html', title='Донор - Бонусы')


@app.route('/mybonuses', methods=['GET', 'POST'])
def mybonuses():
    donor, donor_data = get_donor_data_json()

    donor_ach = db.session.query(PendingAchievements, Achievements).join(Achievements).filter(
        PendingAchievements.donor_id == donor.id).all()

    return render_template('mybonuses.html', title='Донор - Мои Бонусы', donor_ach=donor_ach)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404page.html', title='Донор - Страница не найдена'), 404


if __name__ == '__main__':
    app.run()
