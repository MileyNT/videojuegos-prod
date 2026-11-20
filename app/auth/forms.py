from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = StringField(
        'Correo electrónico',
        validators=[DataRequired(), Email(), Length(max=255)],
    )
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(), Length(min=8)],
    )
    confirm_password = PasswordField(
        'Confirmar contraseña',
        validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField('Crear cuenta')
