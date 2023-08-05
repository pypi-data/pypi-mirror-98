from jose import jwt
from jose.exceptions import JWTError

from jwt_library import ALGORITHMS
from jwt_library.jwt_operations.utils.errors import AuthError

def fetch_token_from_header(token):
    if not token:
        raise AuthError({ "status": "authorization_header_missing",
                          "message": "Authorization header is expected."
        }, 401)

    parts = token.split()

    if parts[0].lower() != 'bearer':
        raise AuthError({"status": "invalid_header",
                        "message":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"status": "invalid_header",
                        "message": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"status": "invalid_header",
                        "message":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def validate_algorithm(unverified_header):
    if unverified_header['alg'] == "HS256":
            raise AuthError({"code": "invalid_header",
                "message":
                    "Invalid header. "
                    "Use an RS256 signed JWT Access Token"}, 401)

def get_unverified_header(token):
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({"code": "invalid_header",
                        "message":
                            "Invalid header. "
                            "Use an RS256 signed JWT Access Token"}, 401)
    return unverified_header

def get_token_verified_payload(token, rsa_key, issuer, audience):
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=audience,
            issuer="https://"+issuer+"/"
        )
    except jwt.ExpiredSignatureError:
        raise AuthError({"status": "token_expired",
                        "message": "token is expired"}, 401)
    except jwt.JWTClaimsError:
        raise AuthError({"status": "invalid_claims",
                        "message":
                            "incorrect claims,"
                            " please check the audience and issuer"}, 401)
    except Exception:
        raise AuthError({"status": "invalid_header",
                        "message":
                            "Unable to parse authentication"
                            " token."}, 401)
    return payload

def get_unverified_token_payload(token):
    return jwt.get_unverified_claims(token)

def authorize(token, required_scope):
    """[summary]

    Args:
        token          (str): The encoded JWT token.
        required_scope (str): The scope required to access the resource
    """
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope") and (required_scope in unverified_claims["scope"]):
        return True
    return False