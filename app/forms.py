from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    secret_key = PasswordField("Geheimer Code", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_again = PasswordField("Password bestätigen", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])

    submit = SubmitField("Registrieren")


class CommentForm(FlaskForm):
    comment = TextAreaField("Schreibe deinen Glückwunsch", validators=[DataRequired()],
                            render_kw={
                                "class": "form-control",
                                "rows": 7,
                                "cols": 60,
                            })

    submit = SubmitField("Abschicken")
