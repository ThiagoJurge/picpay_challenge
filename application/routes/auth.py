from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/register', methods=['GET'])  # Corrected method
def register():
    print("bom dia")
    return "Register"
