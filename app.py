import datetime
import json
import random
import os

from flask import Flask, redirect, render_template, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from forms import LoginForm, RegisterForm, CommentForm

import locale

load_dotenv()

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

MIN_SPACING = 5
PROFILE_CHOICE = ["mann", "frau"]

SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY_REGISTER = os.environ.get("SECRET_KEY_REGISTER")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.getenv('DATABASE_URL', "sqlite:///data.db")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")

    created_on: Mapped[str] = mapped_column(String(250), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_pic: Mapped[str] = mapped_column(String(100), nullable=False)
    comments = relationship("Comment", back_populates="author")


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route("/")
def home():
    return render_template("home.html", current_user=current_user, cur_page="home")


@app.route("/timeline")
def timeline():
    if current_user.is_authenticated:
        with open("data/events.json", "r") as file:
            events = json.load(file)

        return render_template("timeline.html", current_user=current_user, cur_page="timeline",
                               events=add_rel_position(events))
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("login"))


@app.route("/comments")
def comments():
    result = db.session.execute(db.select(Comment))
    comments = result.scalars().all()

    return render_template("comments.html", current_user=current_user, cur_page="comments", comments=comments)


@app.route("/biography")
def biography():
    if current_user.is_authenticated:
        return render_template("biography.html", current_user=current_user, cur_page="biography")
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("login"))


@app.route("/write_comment", methods=["GET", "POST"])
def write_comment():
    if current_user.is_authenticated:
        form = CommentForm()
        if request.method == "POST" and form.validate:
            new_comment = Comment(
                created_on=datetime.date.today().strftime("%d. %B %Y"),
                author=current_user,
                content=form.comment.data,
            )

            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("comments"))

        return render_template("write_comment.html", current_user=current_user, cur_page="write_comment", form=form)
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("login"))


@app.route("/delete/<comment_id>")
def delete_comment(comment_id):
    comment_to_delete = db.get_or_404(Comment, comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for("comments"))


@app.route("/img-selection")
def img_selection():
    if current_user.is_authenticated:
        return render_template("img_selection.html")
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("login"))

@app.route("/change-profile/<img>")
def change_profile(img):
    if current_user.is_authenticated:
        user = db.get_or_404(User, current_user.id)
        user.profile_pic = img
        db.session.commit()

        return redirect(url_for("home"))
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("Du hast schon ein Konto! Melde dich an")
            return redirect(url_for('login'))

        if form.secret_key.data != SECRET_KEY_REGISTER:
            flash("Falscher Geheimcode")
            return redirect(url_for("register"))
        elif form.password_again.data != form.password.data:
            flash("Passwörter stimmen nicht überein")
            return redirect(url_for("register"))
        else:
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            
            gender = random.choice(PROFILE_CHOICE)
            n = random.randint(1, 10)
            
            new_user = User(
                email=form.email.data,
                name=form.name.data,
                password=hash_and_salted_password,
                profile_pic=f"{gender}{n}"
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for("home"))

    return render_template("register.html", form=form, current_user=current_user, cur_page="register")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form, current_user=current_user, cur_page="login")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


class RangeScaler:
    def __init__(self, lower_range, upper_range, values: list):
        self.values = values
        self.lower = lower_range
        self.upper = upper_range
        self.max = max(values)
        self.min = min(values)

    def get_scaled_list(self) -> list:
        scaled_list = [self.lower + (v - self.min) * (self.upper - self.lower) / (self.max - self.min) for v in
                       self.values]
        return scaled_list

    def scale_item(self, item):
        return self.lower + (item - self.min) * (self.upper - self.lower) / (self.max - self.min)


def add_rel_position(data: dict) -> list:
    cur_year = datetime.datetime.now().year
    events: list = data["events"]
    events.append(
        {
            "id": len(events),
            "event": "Heute",
            "date": cur_year
        }
    )
    events.sort(key=lambda x: x["date"])

    scaler = RangeScaler(MIN_SPACING, 100 - MIN_SPACING, [event["date"] for event in events])

    cid = 1
    for event in events:
        event["rel_pos"] = scaler.scale_item(event["date"])
        event["id"] = cid
        cid += 1

    for i in range(len(events) - 1):
        event1 = events[i]
        event2 = events[i + 1]

        pos1 = event1["rel_pos"]
        pos2 = event2["rel_pos"]

        if pos2 - pos1 < MIN_SPACING and pos2 < 100 - MIN_SPACING * 2:
            event2["rel_pos"] = pos2 + MIN_SPACING - (pos2 - pos1)

    return events


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
