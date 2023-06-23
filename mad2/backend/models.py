from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import func
import datetime

db = SQLAlchemy()

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    rel_list = db.relationship("List")


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class List(db.Model):
    __tablename__ = 'list'
    lid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cards = db.relationship("Card", cascade="all, delete")


class Card(db.Model):
    __tablename__ = 'card'
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_title = db.Column(db.String, nullable=False)
    content = db.Column(db.String(120),  nullable=False)
    deadline = db.Column(db.String, server_default=func.now())
    flag = db.Column(db.String)
    list_id = db.Column(db.Integer, db.ForeignKey("list.lid"), nullable=False)
    last_change = db.Column(db.String, onupdate=datetime.datetime.now())
    card_created = db.Column(db.String, server_default=func.now())
