import jwt
import requests
import time
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import traceback

def parse_token(token):
    if token.startswith('Bearer '):
        token = token[len('Bearer '):]
    return token
def validate_token(token, google_client_id):
    # Fetch Google's public keys
    response = requests.get('https://www.googleapis.com/oauth2/v1/certs')
    public_keys = response.json()
    token = parse_token(token)
    # Verify the token's signature using each public key
    signature_verified = False
    for key_id, cert_str in public_keys.items():
        try:
            cert_obj = load_pem_x509_certificate(cert_str.encode('utf-8'), default_backend())
            public_key = cert_obj.public_key()
            jwt.decode(token, public_key, audience=google_client_id, algorithms=['RS256'])
            # Signature verified and all claims valid
            signature_verified = True
            break  # Stop iterating if verification succeeds
        except Exception as e:
            # If verification fails with this key, try the next one
            print(f'Signature verification failed with key: {key_id}')
            print(f'Error: {e}')

    return signature_verified
