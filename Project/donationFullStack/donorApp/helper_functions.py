from datetime import datetime

from donorApp.models import User, Donor, DonationTime
from donorApp import db
from flask_login import current_user

import json
import string
import random

initial_data = {
    'type': 'init_data',
    'main_data': {
        'first_name': '',
        'last_name': '',
        'gender': '',
        'age': '',
        'profile_image': ''
    },
    'contacts': {
        'phone_number': '',
        'address': '',
        'email': ''
    },
    'medical_data': {
        'height': 0,
        'weight': 0,
        'blood_type': ''
    }
}


def find_user(username):
    request_user = User.query.filter_by(username=username).first()
    return request_user


def find_donor(user_id):
    request_donor = Donor.query.filter_by(user_id=user_id).first()
    return request_donor


def get_donor_data_json():
    donor = db.session.query(Donor).join(User).filter(User.id == Donor.user_id).filter(
        User.username == current_user.username).first()

    donor_data = donor.data

    return donor, donor_data


def change_donor_data_type(donor_data):
    dict_donor_data = json.loads(donor_data)

    if dict_donor_data['type'] == 'init_data':
        dict_donor_data['type'] = 'filled_data'
        donor_data = json.dumps(dict_donor_data)
    else:
        pass

    return donor_data


def appointment_initial_data():
    init_data = {
        ''
    }

    return init_data


def get_cur_time():
    now = datetime.now().replace(second=0, microsecond=0)
    return now


def donation_time():
    new_date = DonationTime(blood_center_id=1, donation_time=get_cur_time(), is_available=False)
    db.session.add(new_date)
    db.session.commit()


def randomize_string():
    S = 10
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    return str(ran)
