from flask_login import UserMixin

from donorApp import db, manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    data = db.Column(db.Text, nullable=False)


class BloodCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contacts = db.Column(db.Text, nullable=False, default='{}')


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_center_id = db.Column(db.Integer, db.ForeignKey('blood_center.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    donation_cost_fk = db.Column(db.Integer, db.ForeignKey('donation_price.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False, default=db.func.now())
    is_submitted = db.Column(db.BOOLEAN)


class MedicalCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contacts = db.Column(db.Text, nullable=False, default='{}')


class DonationPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donation_type = db.Column(db.String(255), nullable=False)
    donation_cost = db.Column(db.Integer, nullable=False)


class Achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    achievement_type_id = db.Column(db.Integer, db.ForeignKey('achievement_type.id'))
    medical_center_id = db.Column(db.Integer, db.ForeignKey('medical_center.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    rus_name = db.Column(db.String(255), nullable=True)


class AchievementType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rus_name = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=False)


class BadgesAchieved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_type_id = db.Column(db.Integer, db.ForeignKey('badges_type.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)


class BadgesType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class RequiredBlood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_types_id = db.Column(db.Integer, db.ForeignKey('blood_types.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class BloodTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, nullable=False)
    rhd = db.Column(db.Integer, nullable=False)


class UsedAchievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    achievements_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)


class PendingAchievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    achievements_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    is_submitted = db.Column(db.Integer, default=False, nullable=False)
    data = db.Column(db.Text, nullable=False)


class DonationTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_center_id = db.Column(db.Integer, db.ForeignKey('blood_center.id'), nullable=False)
    donation_time = db.Column(db.DateTime, nullable=False, default=db.func.now())
    is_available = db.Column(db.Boolean, default=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
