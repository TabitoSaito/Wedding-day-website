from flask import render_template, flash, redirect, url_for, current_app
from flask_login import current_user
import json
import os

from app.models import User
from app.extensions import db
from app.helper import add_rel_position
from . import main_bp

@main_bp.route("/")
def home():
    """load homepage
    """
    return render_template("home.html", current_user=current_user, cur_page="home")

@main_bp.route("/timeline")
def timeline():
    """load 'events.json' and render timeline and event cards for events. Requires to be logged in
    """
    if current_user.is_authenticated:
        with open(os.path.join(current_app.static_folder, "data", "events.json"), "r") as file:
            events = json.load(file)

        return render_template("timeline.html", current_user=current_user, cur_page="timeline",
                               events=add_rel_position(events))
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("auth.login"))
    
@main_bp.route("/biography")
def biography():
    """load biography page. Requires to be logged in
    """
    if current_user.is_authenticated:
        return render_template("biography.html", current_user=current_user, cur_page="biography")
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("auth.login"))
    
@main_bp.route("/img-selection")
def img_selection():
    """load image selection page to change profile picture. Requires to be logged in
    """
    if current_user.is_authenticated:
        return render_template("img_selection.html")
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("auth.login"))

@main_bp.route("/change-profile/<img>")
def change_profile(img):
    """change profile picture and save changes in database. Redirects to homepage. Requires to be logged in

    Args:
        img (_type_): image name to change to
    """
    if current_user.is_authenticated:
        user = db.get_or_404(User, current_user.id)
        user.profile_pic = img
        db.session.commit()

        return redirect(url_for("main.home"))
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("auth.login"))