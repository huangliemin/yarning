# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, flash, request
from . import auth
from flask.ext.login import login_user, logout_user, login_required
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
#		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash(u'用户名或密码错误！')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash(u'注销成功！')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register(): 
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data, password=form.password.data, role_id=3)
		db.session.add(user)
		flash(u'恭喜你，注册成功！')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',form=form)