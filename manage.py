#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Permission, Cv, Book
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import config


# from app.models import User, Role, Cv, General, Address, Profiles, Teaching, Publications, Books, BookAuthors, Chapters, ChapterAuthors, Articles, ArticleAuthors, WebPubs, WebPubAuthors, CourseWork, CourseWorkAuthors, Presentations, ConferencePres, ConfPresAuthors, Workshops, WorkshopAuthors, DeptPres, DeptPresAuthors, Education, Undergrad, UndergradCommittee, Masters, MastersCommittee, Phd, PhdCommittee, Service, Editorial, Groups, Committees, Awards, Grants, Affiliations, Languages, Skills, Audio, Video, Office, CourseManagement, OtherSkills

# app = create_app(config or 'default')
app = create_app(os.getenv('LNDGRN_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Permission=Permission, Cv=Cv, Book=Book)
	#return dict(app=app, db=db, User=User, Role=Role, Cv=Cv, General=General, Address=Address, Profiles=Profiles, Teaching=Teaching, Publications=Publications, Books=Books, BookAuthors=BookAuthors, Chapters=Chapters, ChapterAuthors=ChapterAuthors, Articles=Articles, ArticleAuthors=ArticleAuthors, WebPubs=WebPubs, WebPubAuthors=WebPubAuthors, CourseWork=CourseWork, CourseWorkAuthors=CourseWorkAuthors, Presentations=Presentations, ConferencePres=ConferencePres, ConfPresAuthors=ConfPresAuthors, Workshops=Workshops, WorkshopAuthors=WorkshopAuthors, DeptPres=DeptPres, DeptPresAuthors=DeptPresAuthors, Education=Education, Undergrad=Undergrad, UndergradCommittee=UndergradCommittee, Masters=Masters, MastersCommittee=MastersCommittee, Phd=Phd, PhdCommittee=PhdCommittee, Service=Service, Editorial=Editorial, Groups=Groups, Committees=Committees, Awards=Awards, Grants=Grants, Affiliations=Affiliations, Languages=Languages, Skills=Skills, Audio=Audio, Video=Video, Office=Office, CourseManagement=CourseManagement, OtherSkills=OtherSkills)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
	manager.run()