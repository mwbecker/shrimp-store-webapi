import hashlib
import hmac
import base64

def generate_token(username, password):
    message = f"{username}:{password}".encode('utf-8')
    hashed_message = hashlib.sha256(message)
    digest = hashed_message.digest()
    token = base64.b64encode(digest).decode('utf-8')
    return token

def validate_token(token):
    try:
        # Decode the provided token
        base64.b64decode(token)
        return True
    except:
        return False
