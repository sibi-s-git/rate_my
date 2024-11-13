# api/routes/home_routes.py
from flask import Blueprint, render_template

# Create a blueprint for the home route
home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def home():
    return render_template("home.html")
