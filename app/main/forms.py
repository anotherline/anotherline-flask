from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
	SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User, Cv, Book, Permission

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')

class EditProfileForm(Form):
	given_name = StringField('Given name', validators=[Length(0, 64)])
	mid_name = StringField('Middle name', validators=[Length(0, 64)])
	fam_name = StringField('Family name', validators=[Length(0, 64)])
	university = StringField('University', validators=[Length(0, 128)])
	title = StringField('Title', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
	email = StringField('Email', 
						validators=[
						Required(), Length(1, 64), Email()])
	username = StringField('Username', 
						validators=[
						Required(), Length(1, 64), 
						Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
								'Usernames must have only letters, '
								  'numbers, dots or underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)
	given_name = StringField('Given name', validators=[Length(0, 64)])
	mid_name = StringField('Middle name', validators=[Length(0, 64)])
	fam_name = StringField('Family name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name)
							 for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and \
				User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if field.data != self.user.username and \
				User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

class CvNameForm(Form):
	cvname = StringField('Name your CV:', validators=[Required()])
	submit = SubmitField('Submit')

class BookCvForm(Form):
	title = StringField('Title:', validators=[Required(), Length(1, 128)])
	given = StringField('Given name:', validators=[Required(), Length(1, 64)])
	middle_name = StringField('Middle name:', validators=[Required(), Length(1, 64)])
	fam_name = StringField('Family name:', validators=[Required(), Length(1, 64)])
	year = StringField('Year:', validators=[Required(), Length(1,4)])
	publisher = StringField('Publisher:', validators=[Required(), Length(1, 64)])
	city = StringField('City:', validators=[Required(), Length(1, 64)])
	state = StringField('State:', validators=[Required(), Length(1, 64)])
	url = StringField('URL:')
	book_info = TextAreaField('Book Description:')
	submit = SubmitField('Submit')

class EditBookCvForm(Form):
	title = StringField('Title:', validators=[Required(), Length(1, 128)])
	given = StringField('Given name:', validators=[Required(), Length(1, 64)])
	middle_name = StringField('Middle name:', validators=[Required(), Length(1, 64)])
	fam_name = StringField('Family name:', validators=[Required(), Length(1, 64)])
	year = StringField('Year:', validators=[Required(), Length(1,4)])
	publisher = StringField('Publisher:', validators=[Required(), Length(1, 64)])
	city = StringField('City:', validators=[Required(), Length(1, 64)])
	state = StringField('State:', validators=[Required(), Length(1, 64)])
	url = StringField('URL:')
	book_info = TextAreaField('Book Description:')
	submit = SubmitField('Submit')