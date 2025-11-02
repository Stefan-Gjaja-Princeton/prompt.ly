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
            print("ERROR: No Authorization header or invalid format")
            return None
        
        token = authorization_header.replace('Bearer ', '')
        payload = self.verify_token(token)
        
        if not payload:
            print("ERROR: Token verification failed")
            return None
        
        # Try to extract email from various possible locations in the token
        # Auth0 typically includes email in the 'email' claim when scope includes 'email'
        email = payload.get('email')
        
        # If email not found in standard location, try alternative locations
        if not email:
            email = (
                payload.get('https://promptly.app/email') or
                # Check for email in custom namespace claims
                (payload.get('https://promptly.app/user_metadata', {}).get('email') if isinstance(payload.get('https://promptly.app/user_metadata'), dict) else None)
            )
        
        name = payload.get('name')
        picture = payload.get('picture')
        nickname = payload.get('nickname')
        
        # Only call /userinfo as a last resort if email is missing
        # This should be rare if Auth0 is configured correctly
        if not email:
            try:
                userinfo_url = f"https://{self.domain}/userinfo"
                headers = {'Authorization': authorization_header}
                resp = requests.get(userinfo_url, headers=headers, timeout=5)
                
                if resp.status_code == 200:
                    ui = resp.json()
                    email = ui.get('email') or email
                    name = ui.get('name') or name
                    picture = ui.get('picture') or picture
                    nickname = ui.get('nickname') or nickname
                elif resp.status_code == 429:
                    # Rate limit - cannot proceed without email
                    print(f"ERROR: Auth0 rate limit hit. Cannot get user email. Sub: {payload.get('sub')}")
                    print("ERROR: Please configure Auth0 to include email in access tokens to avoid this issue.")
                    if not email:
                        # Return None to fail authentication gracefully
                        return None
                else:
                    print(f"WARNING: /userinfo call failed: {resp.status_code} {resp.text}")
                    if not email:
                        # Cannot proceed without email for database
                        print(f"ERROR: Cannot get user email from token or /userinfo. Sub: {payload.get('sub')}")
                        return None
            except requests.exceptions.RequestException as ex:
                print(f"WARNING: failed to fetch /userinfo: {ex}")
                if not email:
                    # Cannot proceed without email
                    print(f"ERROR: Cannot get user email. Sub: {payload.get('sub')}")
                    return None
        
        # Email is required for database operations
        if not email or '@' not in str(email):
            print(f"ERROR: Invalid or missing email in token.")
            print(f"ERROR: Sub: {payload.get('sub')}")
            print(f"ERROR: Available claims: {list(payload.keys())}")
            
            if 'email' in payload:
                email_value = payload['email']
                print(f"ERROR: Email key exists but value is invalid: {email_value}")
                print(f"ERROR: Check Auth0 action configuration and logs.")
            else:
                print(f"ERROR: Email claim not found in token.")
                print(f"ERROR: Make sure Auth0 action is configured correctly and you've logged in after setting it up.")
            
            return None

        return {
            'email': email,
            'sub': payload.get('sub'),
            'name': name.split() if isinstance(name, str) and name else [],
            'picture': picture,
            'nickname': nickname
        }

# Global auth service instance
auth_service = AuthService()

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            print("ERROR: No Authorization header in request")
            return jsonify({"error": "Authentication required. No token provided."}), 401
        
        user_data = auth_service.get_user_from_token(auth_header)
        
        if not user_data:
            print(f"ERROR: Authentication failed for endpoint: {request.endpoint}")
            return jsonify({
                "error": "Authentication failed",
                "details": "Token validation failed or email not found in token. If you just set up the Auth0 action, please log out and log back in."
            }), 401
        
        # Add user data to request context
        request.current_user = user_data
        return f(*args, **kwargs)
    
    return decorated_function
