#!/usr/bin/env python
import os
import psycopg2
from app import create_app, db
from app.models import User, Role, Permission, Cv, Book
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import config


# from app.models import User, Role, Cv, General, Address, Profiles, Teaching, Publications, Books, BookAuthors, Chapters, ChapterAuthors, Articles, ArticleAuthors, WebPubs, WebPubAuthors, CourseWork, CourseWorkAuthors, Presentations, ConferencePres, ConfPresAuthors, Workshops, WorkshopAuthors, DeptPres, DeptPresAuthors, Education, Undergrad, UndergradCommittee, Masters, MastersCommittee, Phd, PhdCommittee, Service, Editorial, Groups, Committees, Awards, Grants, Affiliations, Languages, Skills, Audio, Video, Office, CourseManagement, OtherSkills

app = create_app(os.getenv('LNDGRN_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	imports = dict(app=app, db=db, User=User, Role=Role, Permission=Permission, Cv=Cv, Book=Book)
	return imports
	
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
	manager.run()