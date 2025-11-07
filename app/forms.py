from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Form for login logic
    """
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    """Form for registration logic.
    """
    secret_key = PasswordField("Geheimer Code", validators=[DataRequired()]) # set in app environment to restrict website to chosen people
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_again = PasswordField("Password bestätigen", validators=[DataRequired()]) # repeat password to avoid typo mistakes
    name = StringField("Name", validators=[DataRequired()])

    submit = SubmitField("Registrieren")


class CommentForm(FlaskForm):
    """Form to write a new comment
    """
    comment = TextAreaField("Schreibe deinen Glückwunsch", validators=[DataRequired()],
                            render_kw={
                                "class": "form-control",
                                "rows": 7,
                                "cols": 60,
                            })

    submit = SubmitField("Abschicken")
