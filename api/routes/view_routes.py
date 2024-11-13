from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from api.models.user import Photo, User
from api import db

view_bp = Blueprint('view', __name__)

@view_bp.route('/view/<category>')
def view(category):
    photos = Photo.query.all()
    return render_template('view.html', category=category, photos=photos)

@view_bp.route('/react/<int:photo_id>/<reaction>', methods=['POST'])
@login_required
def react(photo_id, reaction):
    photo = Photo.query.get(photo_id)

    if reaction == 'like':
        photo.likes += 1
        current_user.total_likes += 1
    elif reaction == 'love':
        if current_user.daily_hearts > 0:
            photo.loves += 1
            current_user.total_loves += 1
            current_user.daily_hearts -= 1
        else:
            flash("You have no daily hearts left.")
            return redirect(url_for('view.view', category=request.args.get('category')))
    elif reaction == 'dislike':
        photo.dislikes += 1
        current_user.total_dislikes += 1

    db.session.commit()
    return redirect(url_for('view.view', category=request.args.get('category')))

@view_bp.route('/comment/<int:photo_id>', methods=['POST'])
def comment(photo_id):
    photo = Photo.query.get(photo_id)
    comment_text = request.form.get('comment')
    photo.comments.append(comment_text)
    db.session.commit()
    return redirect(url_for('view.view', category=request.args.get('category')))
