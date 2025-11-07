from flask import render_template, request, redirect, url_for, flash
from flask_login import  current_user
import datetime

from app.forms import CommentForm
from app.models import Comment
from app.extensions import db
from . import comment_bp

@comment_bp.route("/")
def comments():
    """Fetch all comments from database and load on page
    """
    result = db.session.execute(db.select(Comment))
    comments = result.scalars().all()

    return render_template("comments.html", current_user=current_user, cur_page="comments", comments=comments)

@comment_bp.route("/write", methods=["GET", "POST"])
def write():
    """load form to write a new comment and add to database. Requires to be logged in

    - GET: render form
    - POST: add comment to database and redirect to comments page
    """
    if current_user.is_authenticated:
        form = CommentForm()
        # validate form and add comment to database
        if request.method == "POST" and form.validate:
            new_comment = Comment(
                created_on=datetime.date.today().strftime("%d. %B %Y"),
                author=current_user,
                content=form.comment.data,
            )

            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("comments.comments"))

        return render_template("write_comment.html", current_user=current_user, cur_page="write_comment", form=form)
    else:
        flash("Du musst dich Anmelden oder Registrieren um diese Seite zu besuchen")
        return redirect(url_for("auth.login"))
    
@comment_bp.route("/delete/<comment_id>")
def delete_comment(comment_id):
    """delete comment from database by id

    Args:
        comment_id (_type_): id of comment to delete
    """
    comment_to_delete = db.get_or_404(Comment, comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for("comments.comments"))