# -*- coding: UTF-8 -*-
from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from ..email import send_mail
from datetime import datetime	
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET','POST'])
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
			if current_app.config['YARNING_ADMIN']:
				send_mail(current_app.config['YARNING_ADMIN'],'New User','mail/new user',user=user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('.index'))
	return render_template('index.html',known=session.get('known',False),current_time=datetime.utcnow(),name=session.get('name'),form=form)

@main.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)
