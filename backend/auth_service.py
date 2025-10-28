from typing import Optional, Dict
from functools import wraps
from flask import request, jsonify
import requests
from jose import jwt
from config import Config

class AuthService:
    def __init__(self):
        self.domain = Config.AUTH0_DOMAIN
        self.api_audience = Config.AUTH0_API_AUDIENCE
        self.algorithms = [Config.AUTH0_ALGORITHMS]
        self.issuer = Config.AUTH0_ISSUER
        
    def get_public_key(self, token: str) -> Dict:
        """Get public key from Auth0 for JWT verification"""
        try:
            # Get JWKS from Auth0
            jwks_url = f"https://{self.domain}/.well-known/jwks.json"
            response = requests.get(jwks_url)
            response.raise_for_status()
            
            jwks = response.json()
            unverified_header = jwt.get_unverified_header(token)
            
            # Find the matching key
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    return {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
            
            raise ValueError('Unable to find appropriate key')
            
        except Exception as e:
            print(f"Error getting public key: {e}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify Auth0 JWT token and return payload"""
        try:
            # Get public key
            public_key = self.get_public_key(token)
            
            # Verify token
            payload = jwt.decode(
                token,
                public_key,
                algorithms=self.algorithms,
                audience=self.api_audience,
                issuer=self.issuer
            )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.JWTClaimsError as e:
            print(f"Invalid token claims: {e}")
            return None
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None
    
    def get_user_from_token(self, authorization_header: str) -> Optional[Dict]:
        """Extract user info from Authorization header"""
        if not authorization_header or not authorization_header.startswith('Bearer '):
            return None
        
        token = authorization_header.replace('Bearer ', '')
        payload = self.verify_token(token)
        
        if payload:
            # Log the payload to see what we're getting
            print(f"DEBUG: Auth0 payload: {payload}")
            # If email is not present in token, fetch from /userinfo
            email = payload.get('email') or payload.get('https://promptly.app/email')
            name = payload.get('name')
            picture = payload.get('picture')
            nickname = payload.get('nickname')

            if not email:
                try:
                    userinfo_url = f"https://{self.domain}/userinfo"
                    auth_header = authorization_header.replace('Bearer ', '')
                    headers = { 'Authorization': f'Bearer {auth_header}' }
                    resp = requests.get(userinfo_url, headers=headers)
                    if resp.status_code == 200:
                        ui = resp.json()
                        email = ui.get('email') or email
                        name = ui.get('name') or name
                        picture = ui.get('picture') or picture
                        nickname = ui.get('nickname') or nickname
                    else:
                        print(f"WARNING: /userinfo call failed: {resp.status_code} {resp.text}")
                except Exception as ex:
                    print(f"WARNING: failed to fetch /userinfo: {ex}")

            return {
                'email': email,
                'sub': payload.get('sub'),
                'name': name.split() if isinstance(name, str) and name else [],
                'picture': picture,
                'nickname': nickname
            }
        
        return None

# Global auth service instance
auth_service = AuthService()

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        user_data = auth_service.get_user_from_token(auth_header)
        
        if not user_data:
            return jsonify({"error": "Authentication required"}), 401
        
        # Add user data to request context
        request.current_user = user_data
        return f(*args, **kwargs)
    
    return decorated_function
