from auth.models import isPasswdOk, isUserExist, addUser
from .form import RegistrationForm
from flask import render_template, redirect, url_for, flash, request
from auth import auth

@auth.route('/', methods=['GET','POST'])
def login():
    # session.pop('user',None)
    # session.pop('passwd',None)

    username = request.form.get('Username')
    password = request.form.get('Password')
    if isPasswdOk(username, password):
        return redirect(url_for('main.correct'))
    else:
        return render_template('login.html', message='密码或用户名错误')
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # session.pop('user',None)
    # session.pop('passwd',None)
    form = RegistrationForm()
    if form.validate_on_submit():
        # 用户提交的表单信息
        username = form.username.data
        password = form.password.data
        if isUserExist(username):
            flash('The username has been used.')
            return render_template('register.html', form=form)
        else:
            addUser(username, password)
            flash('Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)