"""
Database handler simulating user credential verification and session logging.
"""

fake_user_db = {
    "admin": {"id": 1, "password": "admin123"},
    "guest": {"id": 2, "password": "guest123"}
}

session_store = []

auth_logs = []

def find_user_by_credentials(username, password):
    """
    Finds a user by their credentials.
    
    Args:
        username (str): The username to search for.
        password (str): The password to verify.
    
    Returns:
        dict: A dictionary containing the user's ID and username if found, otherwise None.
    """

    user = fake_user_db.get(username)
    if user and user["password"] == password:
        return {"id": user["id"], "username": username}
    return None

def save_user_session(user_id, session_id):
    """
    Saves a user's session.
    
    Args:
        user_id (int): The ID of the user.
        session_id (str): The ID of the session.
    """

    session_store.append({"user_id": user_id, "session_id": session_id})
    print(f"Session {session_id} saved for user {user_id}")

def get_user_sessions(user_id):
    """
    Retrieves all sessions for a given user.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        list: A list of dictionaries containing the user's session information.
    """

    return [s for s in session_store if s["user_id"] == user_id]

def log_auth_attempt(username, success):
    """
    Logs an authentication attempt.
    
    Args:
        username (str): The username that attempted to authenticate.
        success (bool): Whether the authentication attempt was successful.
    """

    auth_logs.append({
        "username": username,
        "success": success
    })

def print_all_logs():
    """
    Prints all authentication logs.
    """

    print("=== AUTH LOGS ===")
    for log in auth_logs:
        print(log)
