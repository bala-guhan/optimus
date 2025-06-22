from token_utils import decode_token
from db_handler import save_user_session, get_user_sessions
from utils import log

"""
Manages sessions by storing and retrieving session data for users.
"""

def handle_session(token):
    """
    Handles a session by storing and retrieving session data for users.
    
    Args:
        token (str): The token to be decoded and used to create a session.
    
    Returns:
        dict: A dictionary containing the session ID or an error message.
    """

    user_id = decode_token(token)
    if user_id is None:
        log("Invalid token received.")
        return {"error": "Invalid token"}
    
    session_id = f"session-{user_id}-{uuid.uuid4()}"
    save_user_session(user_id, session_id)
    return {"session_id": session_id}

def user_session_summary(user_id):
    """
    Retrieves a summary of sessions for a given user ID.
    
    Args:
        user_id (str): The ID of the user for whom to retrieve session summaries.
    
    Returns:
        dict: A dictionary containing the user ID, sessions, and session count.
    """

    sessions = get_user_sessions(user_id)
    return {
        "user_id": user_id,
        "sessions": sessions,
        "count": len(sessions)
    }
