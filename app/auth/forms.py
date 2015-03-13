# -*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
	#username = StringField('Username',validators=[Required(),Length(1,64)])
	email = StringField(u'注册邮箱',validators=[Required(),Length(1,64),Email()])
	password = PasswordField(u'密码',validators=[Required()])
	remember_me = BooleanField(u'记住密码')
	submit = SubmitField(u'登录')

class RegistrationForm(Form):
	email = StringField(u'注册邮箱',validators=[Required(),Length(1,64),Email()])
	username = StringField(u'用户名',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])
	password = PasswordField(u'密码',validators=[Required(),EqualTo('password2',message=u'两次输入的密码不一致。')])
	password2 = PasswordField(u'确认密码',validators=[Required()])
	submit = SubmitField(u'注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'该邮箱已经被注册。')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'该用户名已经被注册。')

class ChangePasswordForm(Form):
	old_password = PasswordField(u'旧密码', validators=[Required()])
	password = PasswordField(u'新密码', validators=[Required(), EqualTo('password2', message=u'两次输入的密码不一致。')])
	password2 = PasswordField(u'确认密码', validators=[Required()])
	submit = SubmitField(u'修改密码')

class PasswordResetRequestForm(Form):
	email = StringField(u'邮箱', validators=[Required(), Length(1, 64),Email()])
	submit = SubmitField(u'重设密码')

class PasswordResetForm(Form):
	email = StringField(u'邮箱', validators=[Required(), Length(1, 64),Email()])
	password = PasswordField(u'新密码', validators=[Required(), EqualTo('password2', message=u'两次输入的密码不一致。')])
	password2 = PasswordField(u'确认密码', validators=[Required()])
	submit = SubmitField(u'重设密码')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError(u'无此用户，请确认邮箱输入是否正确。')

class ChangeEmailForm(Form):
	email = StringField(u'新邮箱', validators=[Required(), Length(1, 64),Email()])
	password = PasswordField(u'密码', validators=[Required()])
	submit = SubmitField(u'更新邮箱地址')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('此邮箱已经被注册。')