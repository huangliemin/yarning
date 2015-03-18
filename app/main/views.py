# -*- coding: UTF-8 -*-
from flask import render_template, session, redirect, url_for, current_app, flash, request
from . import main
from datetime import datetime
from .. import db
from ..models import User, Permission, Post, Role
from ..decorators import admin_required, permission_required
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from flask.ext.login import login_user, logout_user, login_required, current_user

@main.route('/', methods=['GET','POST'])
def index():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body=form.body.data, author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	page = request.args.get('page',1,type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['YARNING_POSTS_PER_PAGE'],error_out=False)
	posts = pagination.items
	# return render_template('index.html',current_time=datetime.utcnow(),name=session.get('name'))
	return render_template('index.html',form=form,posts=posts,current_time=datetime.utcnow(),name=session.get('name'),pagination=pagination)

@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	page = request.args.get('page',1,type=int)
	pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['YARNING_POSTS_PER_PAGE'],error_out=False)
	posts = pagination.items
	return render_template('user.html',user=user,posts=posts,pagination=pagination)

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

@main.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user)
		flash(u'您的信息更新成功')
		return redirect(url_for('.user',username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me = current_user.about_me
	return render_template('edit_profile.html',form=form, name=current_user.name)

@main.route('/edit-profile/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin():
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username= form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		db.session.add(user)
		flash(u'信息更新成功')
		return redirect(url_for('.user',username=current_user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me = user.about_me
	return render_template('edit_profile_admin.html',form=form)

@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html',posts=[post])

@main.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	if current_user != post.author and not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		flash(u'更新说说成功！')
		return redirect(url_for('.post',id=post.id))
	form.body.data = post.body
	return render_template('edit_post.html',form=form)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(u'无此用户！')
		return redirect(url_for('.index'))
	if current_user.is_following(user):
		flash(u'您已经关注此用户！')
		return redirect(url_for('.user', username=username))
	current_user.follow(user)
	flash(u'您正在关注 %s！' % username)
	return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(u'无此用户！')
		return redirect(url_for('.index'))
	if not current_user.is_following(user):
		flash(u'您未关注过此用户！')
		return redirect(url_for('.user', username=username))
	current_user.unfollow(user)
	flash(u'您取消了对 %s 的关注！' % username)
	return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(u'无此用户！')
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followers.paginate(
		page, per_page=current_app.config['YARNING_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows = [{'user': item.follower, 'timestamp': item.timestamp}
			   for item in pagination.items]
	return render_template('followers.html', user=user, title="的粉丝",
						   endpoint='.followers', pagination=pagination,
						   follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(u'无此用户！')
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followed.paginate(
		page, per_page=current_app.config['YARNING_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows = [{'user': item.followed, 'timestamp': item.timestamp}
			   for item in pagination.items]
	return render_template('followers.html', user=user, title="的关注",
						   endpoint='.followed_by', pagination=pagination,
						   follows=follows)


