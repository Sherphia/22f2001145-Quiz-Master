from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import create_access_token
from models.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

auth_bp = Blueprint('auth_bp', __name__)

# User Signup
@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role') 

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        email=data['email'],
        password=hashed_password,
        full_name=data.get('full_name'),
        qualification=data.get('qualification'),
        dob=datetime.datetime.strptime(data.get('dob'), '%Y-%m-%d'),
        role='user'
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# User Login
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    user = User.query.filter_by(email=email, role=role).first() 

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=json.dumps({'id': user.id, 'email': user.email, 'role': user.role}))

    # ✅ Send token with user info
    return jsonify({
        'message': 'Login successful',
        'token': access_token,
        'user': {
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role
        }
    }), 200
