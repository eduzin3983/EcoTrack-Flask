from flask import Blueprint, render_template

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    return render_template('index.html')

@public_bp.route('/sobre')
def sobre():
    return render_template('sobre.html')

@public_bp.route('/como-funciona')
def como_funciona():
    return render_template('como-funciona.html')
