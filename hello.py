# -*- coding: UTF-8 -*-
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.script import Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'my son is huangzheyan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('submit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	users = db.relationship('User', backref = 'role', lazy = 'dynamic')
	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True, index = True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User %r>' % self.username

@app.route('/', methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data, role_id=3)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html',known=session.get('known',False),current_time=datetime.utcnow(),name=session.get('name'),form=form)

@app.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))

if __name__=="__main__":
	manager.run()
	
