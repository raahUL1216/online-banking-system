import jwt 

# paths to be excluded from authorization
path_dict = {
    '/': 'root',
    '/docs': 'doc',
    '/openapi.json': 'doc',
    '/register': 'Register API',
    '/auth': 'Auth API'
}

SECRET_KEY = "dummy-jwt-secret-key"
ALGORITHM = "HS256"

def generate_jwt(payload):
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt(access_token):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id", None)
    except Exception as e:
        print(f'Error while decoding access token. {e}')
        return None