import jwt
from datetime import datetime, timedelta

# Your JWT secret key
JWT_SECRET_KEY = 'your_jwt_secret_key'  # Replace with your actual secret key

def generate_jwt_token(user_id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=1),  # Token expires after 1 hour
            'iat': datetime.utcnow(), 
            'sub': str(user_id)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
        return jwt_token
    except Exception as e:
        return "Cannot generate session token"

def decode_jwt_token(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

# Test the JWT generation and decoding
if __name__ == "__main__":
    user_id = 123  # Example user ID
    token = generate_jwt_token(user_id)
    print("Generated JWT Token:", token)
    
    # Decode the token to verify its contents
    decoded_token = decode_jwt_token(token)
    print("Decoded JWT Token:", decoded_token)

    # Check if the token is valid and not expired
    if 'exp' in decoded_token:
        exp = datetime.utcfromtimestamp(decoded_token['exp'])
        print("Token expires at:", exp)
