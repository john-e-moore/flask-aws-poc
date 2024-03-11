from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/blog')
def blog():
    return render_template('blog.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/projections')
@login_required
def projections():
    return render_template('projections.html', name=current_user.username)
