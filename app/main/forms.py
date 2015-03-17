# -*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Email, Length, Regexp

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('submit')

class EditProfileForm(Form):
	name = StringField(u'真实姓名',validators=[Length(0,64)])
	location = StringField(u'住址',validators=[Length(0,64)])
	about_me = TextAreaField(u'个人简介')
	submit = SubmitField(u'确认提交')

class EditProfileAdminForm(Form):
	email = StringField(u'邮箱地址',validators=[Required(),Length(1,64),Email()])
	username = StringField(u'用户名',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,u'用户名必须由数字、字母或下划线组成！')])
	confirmed = BooleanField(u'是否已认证')
	role = SelectField(u'角色',coerce=int)
	name = StringField(u'真实姓名',validators=[Length(0,64)])
	location = StringField(u'住址',validators=[Length(0,64)])
	about_me = TextAreaField(u'个人简介')
	submit = SubmitField(u'确认提交')

	def __init__(self,user,*args,**kwags):
		super(EditProfileAdminForm,self).__init__(*args,**kwags)
		self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('此邮箱已经被注册。')

	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(email=field.data).first():
			raise ValidationError('此用户名已经被注册。')

class PostForm(Form):
	body = TextAreaField(u'您的观点', validators=[Required()])
	submit = SubmitField(u'确认提交')