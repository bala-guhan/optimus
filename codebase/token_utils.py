import uuid
import time

"""
Token utility functions: token generation, expiration, parsing
"""

TOKEN_EXPIRY = 3600  # 1 hour

def generate_token(user_id):
    token = f"{user_id}-{uuid.uuid4()}-{int(time.time())}"
    return token

def decode_token(token):
    try:
        user_id, _, _ = token.split("-")
        return user_id
    except Exception:
        return None

def is_token_expired(token):
    try:
        _, _, ts = token.split("-")
        return (time.time() - int(ts)) > TOKEN_EXPIRY
    except:
        return True
