from constants import *


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=True, nullable=False)
    gallery_flag = db.Column(db.Integer, unique=False, nullable=False, default=0)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), unique=True, nullable=False, default='123467890')


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(80), unique=True, nullable=False)
    filename = db.Column(db.String(80), unique=False, nullable=False)


db.create_all()
