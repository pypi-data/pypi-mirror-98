from flask import Blueprint, redirect, url_for, flash, render_template, jsonify, request, session, g
from app.models import User

bp = Blueprint('main', __name__, template_folder='templates/main')

@bp.route('/')
def main():
    return render_template('dashboard.html')