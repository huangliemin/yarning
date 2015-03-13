# -*- coding: UTF-8 -*-
from flask import render_template, session, redirect, url_for, current_app
from . import main
from datetime import datetime
from .. import db
from ..models import User

@main.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html',current_time=datetime.utcnow(),name=session.get('name'))

@main.route('/user/<name>')
def user(name):
	return render_template('user.html',name=name)
