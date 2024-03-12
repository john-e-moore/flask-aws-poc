import os
import pandas as pd
from markdown import markdown
from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from .config import Config

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
        authored_date = filename.split('_')[0]
        post_title = filename.split('_')[1].split('.')[0].replace('-',' ').title()
        with open(filepath, 'r') as file:
            post_content = file.read()
        html_content = markdown(post_content)
        posts.append({'date': authored_date, 'title': post_title, 'content': html_content})
    return render_template('blog.html', posts=posts)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

@main.route('/projections')
@login_required
def projections():
    local_download_path = Config.PROJECTIONS_DOWNLOAD_LOCAL_KEY
    if os.path.exists(local_download_path):
        usecols = [
            'player', 'Team', 'Opponent', 'DK Position', 'proj_source', 'DK Salary',
            'DK Projection', 'proj_fpts_dk', 'DK Difference'
        ]
        data = pd.read_csv(local_download_path, usecols=usecols)
        data_html = data.to_html(classes='display', index=False)
        data_html = data_html.replace('<table border="1" class="dataframe display">', '').replace('</table>', '')
    else:
        data_html = "<p>No data available.</p>"
    return render_template(
        'projections.html', 
        name=current_user.username,
        data=data_html,
        last_updated=current_app.config['LAST_UPDATED']
    )
