from token_utils import generate_token, is_token_expired
from db_handler import find_user_by_credentials, log_auth_attempt
from utils import log

"""
Handles user authentication including password verification and token generation.
"""

def authenticate_user(username, password):
    """
    Authenticate user by verifying credentials and generating a secure token.
    """
    log(f"Attempting authentication for user: {username}")
    user = find_user_by_credentials(username, password)
    
    if user:
        log(f"User {username} authenticated successfully.")
        log_auth_attempt(username, success=True)
        return generate_token(user["id"])
    else:
        log(f"User {username} failed authentication.")
        log_auth_attempt(username, success=False)
        return None


def refresh_token(old_token):
    """
    Refresh the token if it has expired.
    """
    if is_token_expired(old_token):
        user_id = old_token.split("-")[0]
        new_token = generate_token(user_id)
        log(f"Refreshed token for user ID: {user_id}")
        return new_token
    else:
        log("Token not expired. No refresh needed.")
        return old_token
