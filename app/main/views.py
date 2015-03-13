# -*- coding: UTF-8 -*-
from flask import render_template, session, redirect, url_for, current_app
from . import main
from datetime import datetime
from .. import db
from ..models import User, Permission
from ..decorators import admin_required, permission_required
from flask.ext.login import login_required

@main.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html',current_time=datetime.utcnow(),name=session.get('name'))

@main.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
	return u"只有管理员能够访问"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
	return u"只有审核员和管理员能够访问"
