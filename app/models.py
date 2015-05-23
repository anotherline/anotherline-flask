from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
import hashlib
from flask import request
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import login_manager, db

class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	MAKE_CV = 0x04
	ADMINISTER = 0x80


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	@staticmethod
	def insert_roles():
		roles = {
			'User': (Permission.FOLLOW |
					 Permission.COMMENT |
					 Permission.MAKE_CV, True),
			'Administrator': (0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

	def __repr__(self):
		return '<Role %r>' % self.name

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	cv = db.relationship("Cv", uselist=False, backref="user") #1-to-1
	books = db.relationship("Book", lazy='dynamic') #1-to-Many

	given_name = db.Column(db.String(64))
	mid_name = db.Column(db.String(64))
	fam_name = db.Column(db.String(64))
	fullname = column_property(given_name + ' ' + mid_name + ' ' + fam_name)
	apa_beg_name = column_property(fam_name + ', ' + given_name[0].capitalize() \
																				+ '.' + mid_name[0].capitalize() + '.')
	apa_end_name = column_property(given_name[0].capitalize() + '.' \
																				+ mid_name[0].capitalize() + '. ' \
																				+ fam_name)

	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64), unique=True, index=True)
	title = db.Column(db.String(64), unique=True)
	university = db.Column(db.String(128), unique=True)
	phone = db.Column(db.String(64), unique=True)
	website = db.Column(db.String(64), unique=True)
	password_hash = db.Column(db.String(128))
	avatar_hash = db.Column(db.String(32))
	confirmed = db.Column(db.Boolean, default=False)

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['LNDGRN_ADMIN']:
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()
		if self.email is not None and self.avatar_hash is None:
			self.avatar_hash = hashlib.md5(
				self.email.encode('utf-8')).hexdigest()

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id})

	def reset_password(self, token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		return True

	def generate_email_change_token(self, new_email, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'change_email': self.id, 'new_email': new_email})

	def change_email(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('change_email') != self.id:
			return False
		new_email = data.get('new_email')
		if new_email is None:
			return False
		if self.query.filter_by(email=new_email).first() is not None:
			return False
		self.email = new_email
		db.session.add(self)
		return True

	def gravatar(self, size=100, default='identicon', rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://www.gravatar.com/avatar'
		hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, \
			hash=hash, size=size, default=default, rating=rating)

	def can(self, permissions):
		return self.role is not None and \
			(self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTER)

	def is_user(self):
		return self.can(Permission.MAKE_CV)

	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	def __repr__(self):
		return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False


login_manager.anonymous_user = AnonymousUser

# User loader callback function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Cv(db.Model):
	__tablename__ = 'cvees'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	cvname = db.Column(db.String(64))

	def delete_cv(self):
		cv_to_del = self.query.filter_by(cvname=cv.cvname)
		db.session.delete(cv_to_del)
		db.session.commit()

	def __repr__(self):
		return '<Cv %r>' % self.cvname


class Book(db.Model):
	__tablename__ = 'books'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey('users.id'))

	forthcoming = db.Column(db.Boolean, default=False)
	role = db.Column(db.Boolean, default=True) #author==T; editor==F
	num_colleagues = db.Column(db.Integer)
	book_info = db.Column(String(50))
	title = db.Column(db.String(64))
	publisher = db.Column(db.String(64))
	city = db.Column(db.String(64))
	state = db.Column(db.String(64))
	year = db.Column(db.String(4))
	url = db.Column(db.String(64))
	given = db.Column(db.String(64))
	fam_name = db.Column(db.String(64))
	middle_name = db.Column(db.String(64))
	pub_type = db.Column(db.String(64))

	@hybrid_property
	def name (self):
		given = self.given if self.given is not None else ""
		middle_name = self.middle_name if self.middle_name is not None else ""
		fam_name = self.fam_name if self.fam_name is not None else ""
		return " ".join((given, middle_name, fam_name)).strip()

	@name.setter
	def name (self, string):
		given = ""
		middle_name = ""
		fam_name = ""
		split_string = string.split(' ')
		if len(split_string) == 1:
			given = string
		elif len(split_string) == 2:
			given, fam_name = split_string
		elif len(split_string) == 3:
			given, middle_name, fam_name = split_string
		else: #len(split_string) > 3:
			given = split_string[0]
			fam_name = split_string[-1]
			middle_name = " ".join(split_string[1:-2])
		self.given = given
		self.middle_name = middle_name
		self.fam_name = fam_name

	@name.expression
	def name (cls):
		f = cls.given
		m = cls.middle_name
		l = cls.fam_name
		return f+' '+m+' '+l

	def __repr__(self):
		return '<Book %r>' % self.title
