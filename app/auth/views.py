# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, flash, request
from . import auth
from flask.ext.login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import send_email

@auth.before_app_request
def before_request():
	if current_user.is_authenticated() \
			and not current_user.confirmed \
			and request.endpoint[:5] != 'auth.' \
			and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous() or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
#       user = User.query.filter_by(username=form.username.data).first()
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
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm Your Account','auth/email/confirm', user=user, token=token)
		flash(u'恭喜你，注册成功！')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash(u'认证激活成功！')
	else:
		flash(u'认证链接有误或者已经失效！')
	return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account','auth/email/confirm', user=current_user, token=token)
	flash(u'认证激活邮件已经发送，请查收，认证链接有效时间为1小时！')
	return redirect(url_for('main.index'))
