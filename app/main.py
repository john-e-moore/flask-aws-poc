import os
from markdown import markdown
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/blog')
def blog():
    # List all markdown files and sort by date, most recent first.
    posts_dir = 'app/static/blog_posts'
    posts_files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
    posts_files.sort(reverse=True)
    # Read and convert each post to HTML.
    posts = []
    for filename in posts_files:
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r') as file:
            post_content = file.read()
        html_content = markdown(post_content)
        posts.append({'title': filename, 'content': html_content})
    return render_template('blog.html', posts=posts)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/projections')
@login_required
def projections():
    return render_template('projections.html', name=current_user.username)
