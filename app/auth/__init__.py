from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_

from models import User, db
from .forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            or_(
                User.username == form.username.data,
                User.email == form.email.data,
            )
        ).first()
        if existing_user is not None:
            flash('El nombre de usuario o correo ya está registrado.', 'error')
            return render_template('auth/register.html', form=form)

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Tu cuenta se creó correctamente.', 'success')
        return redirect(url_for('juegos'))

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña incorrectos.', 'error')
            return render_template('auth/login.html', form=form)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if next_page:
            parsed_next = urlsplit(next_page)
            if (
                next_page.startswith('/')
                and not next_page.startswith('//')
                and '\\' not in next_page
                and not parsed_next.scheme
                and not parsed_next.netloc
            ):
                return redirect(next_page)
        return redirect(url_for('juegos'))

    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('auth.login'))
