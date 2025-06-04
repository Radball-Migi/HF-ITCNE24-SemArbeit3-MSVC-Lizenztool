from app.main import bp
from flask import render_template

@bp.route('/')
def show_frontend():
    return render_template("mainpage.html")