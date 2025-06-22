from auth_service import authenticate_user, refresh_token
from utils import validate_request, log

"""
API-like routes for handling login requests and token refresh.
"""

def login_route(request):
    if not validate_request(request):
        return {"error": "Invalid request payload"}

    username = request.get("username")
    password = request.get("password")

    token = authenticate_user(username, password)

    if token:
        return {"status": "success", "token": token}
    else:
        return {"status": "failure", "message": "Authentication failed"}

def token_refresh_route(request):
    old_token = request.get("token")
    if not old_token:
        return {"error": "Token not provided"}

    new_token = refresh_token(old_token)
    return {"token": new_token}
