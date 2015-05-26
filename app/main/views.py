from flask import render_template, session, redirect, url_for, current_app, \
	abort, flash
from flask.ext.login import login_required, current_user
from .. import db
from ..models import User, Role, Cv, Book, Permission
from . import main
from .forms import NameForm, CvNameForm, EditProfileForm, \
	EditProfileAdminForm, BookCvForm, EditBookCvForm
from ..decorators import admin_required

#----------------------------
#
# View Functions
#
#----------------------------

@main.route('/')
@main.route('/index.html')
def index():
	return render_template('index.html',
						 title='AnotherLine', tagline='Your academic story')


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	form = CvNameForm()

	if form.validate_on_submit():
		new_cv = Cv(
					cvname=form.cvname.data, 
					user=current_user._get_current_object() )
		db.session.add(new_cv)
		return redirect(url_for('.user', 
								username=current_user.username,
								user=user, 
								cvname=form.cvname.data))
	mycv = user.cv

	return render_template('user.html', form=form, user=user, mycv=mycv)
	

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.given_name = form.given_name.data
		current_user.mid_name = form.mid_name.data
		current_user.fam_name = form.fam_name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		current_user.university = form.university.data
		current_user.title = form.title.data
		db.session.add(current_user)
		flash('Your profile has been updated.')
		return redirect(url_for('.user', username=current_user.username))
	form.given_name.data = current_user.given_name
	form.mid_name.data = current_user.mid_name
	form.fam_name.data = current_user.fam_name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	form.university.data = current_user.university
	form.title.data = current_user.title
	return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		user.university = form.university.data
		user.title = form.title.data
		db.session.add(user)
		flash('The profile has been updated.')
		return redirect(url_for('.user', username=user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	form.university.data = user.university
	form.title.data = user.title
	return render_template('edit_profile.html', form=form, user=user)

#--------------------------
# ADD NEW BOOK Route
#--------------------------

@main.route('/add-book/<username>/', methods=['GET', 'POST'])
@login_required
def add_new_book(username):

	form = BookCvForm()
	if form.validate_on_submit():
		form = Book(title=form.title.data,
					given=form.given.data,
					middle_name=form.middle_name.data,
					fam_name=form.fam_name.data,
					year=form.year.data,
					publisher=form.publisher.data,
					city=form.city.data,
					state=form.state.data,
					url=form.url.data,
					book_info=form.book_info.data,
					user_id=current_user.id )
		db.session.add(form)
		db.session.commit()

		def book(form):
			book = form
			return book

		def append_book_to_cvees(bk):
			u = current_user
			u.books.append(bk)
			db.session.commit()
			flash('The book has been added to your CV.')
			bk = u.books
			return bk

		bk = book(form)
		append_book_to_cvees(bk)

		return redirect(url_for('.user', 
								username=current_user.username, 
								books=bk.title))

	return render_template('add_book.html', 
							form=form, 
							username=current_user.username)


@main.route('/edit-book/<username>/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit_book(username, id):
	edit_bk = Book.query.get_or_404(id)
	form = EditBookCvForm(obj=edit_bk)
	if form.validate_on_submit():
		edit_bk.title = form.title.data
		edit_bk.given = form.given.data
		edit_bk.middle_name = form.middle_name.data
		edit_bk.fam_name = form.fam_name.data
		edit_bk.year = form.year.data
		edit_bk.publisher = form.publisher.data
		edit_bk.city = form.city.data
		edit_bk.state = form.state.data
		edit_bk.url = form.url.data
		edit_bk.book_info = form.book_info.data
		db.session.add(edit_bk)
		flash('Your book has been updated.')
		return redirect(url_for('.user', 
								username=current_user.username, 
								id=edit_bk.id))
	return render_template('edit_book.html', form=form)


@main.route('/<username>/cv/<int:id>', methods=['GET', 'POST'])
def user_cv(username, id):
	user = User.query.get_or_404(id)

	def books_exist(self, id):
		bks_exist = self.query.filter(Cv.id == id)
		return self.query(bks_exist.exists())

	return render_template('cv.html', 
							user=user,
							username=user.username,
							id=id)