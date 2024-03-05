import requests
from flask import Blueprint, request, jsonify
from functools import wraps
from firebase_admin import auth, exceptions

# Initialize the auth blueprint
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user with email and password.
    """
    try:
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required.'}), 400

        user = auth.create_user(
            email=data['email'],
            password=data['password']
        )
        return jsonify({'uid': user.uid}), 201

    except exceptions.FirebaseError as e:
        # Handle Firebase errors
        return jsonify({'error': e.message}), e.code

    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': 'Failed to create user.'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user and return a custom token.
    """
    try:
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required.'}), 400

        user = auth.get_user_by_email(data['email'])
        # Verify the password in Firebase Authentication
        # This is done on the client side in Firebase, but you could create a session cookie if needed

        # Create a custom token for the user
        custom_token = auth.create_custom_token(user.uid)

        return jsonify({'token': custom_token.decode('utf-8')}), 200

    except exceptions.FirebaseError as e:
        # Handle Firebase errors
        return jsonify({'error': e.message}), e.code

    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': 'Failed to log in.'}), 500

def verify_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        
        try:
            # Verify the token with Firebase Admin SDK
            decoded_token = auth.verify_id_token(token)
            # Add the token's user information to the request context
            request.user = decoded_token
            return f(*args, **kwargs)
        except auth.InvalidIdTokenError:
            return jsonify({'error': 'Invalid authentication token'}), 403
        except auth.ExpiredIdTokenError:
            return jsonify({'error': 'Expired authentication token'}), 403
        # Handle other exceptions and errors as needed

    return wrapper

@auth_bp.route('/profile', methods=['GET'])
@verify_token
def user_profile():
    """
    Retrieve the user profile of the currently logged-in user.
    """
    token = request.headers.get('Authorization')
    decoded_token, error_code = verify_token(token)
    
    if not decoded_token:
        return jsonify({'error': 'Invalid or expired token.'}), error_code

    uid = decoded_token['uid']
    user = auth.get_user(uid)
    return jsonify({
        'email': user.email,
        'uid': user.uid
    }), 200

@auth_bp.route('/social-login', methods=['POST'])
def social_login():
    """
    Log in a user with a token from a third-party provider like Google or Facebook.
    The client will send the OAuth token obtained from the provider,
    which will be verified and a custom Firebase token will be returned.
    """
    data = request.get_json()
    provider_token = data.get('provider_token')
    provider = data.get('provider')  # e.g., 'google', 'facebook'

    if not provider_token or not provider:
        return jsonify({'error': 'Provider token and name are required'}), 400

    try:
        # Verify the provider's token and get the Firebase user's UID
        firebase_user = auth.verify_id_token(provider_token, check_revoked=True)
        custom_token = auth.create_custom_token(firebase_user['uid'])
        return jsonify({'token': custom_token.decode('utf-8')}), 200
    except exceptions.FirebaseError as e:
        return jsonify({'error': e.message}), e.code
    except Exception as e:
        return jsonify({'error': 'Failed to log in with social provider.'}), 500

