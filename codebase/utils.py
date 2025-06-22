"""
Utility functions used throughout the app for logging and request validation.
"""

def log(message):
    print(f"[LOG] {message}")

def validate_request(request):
    if not isinstance(request, dict):
        return False
    return "username" in request and "password" in request

def debug_data(obj):
    print("=== DEBUG START ===")
    print(obj)
    print("=== DEBUG END ===")
