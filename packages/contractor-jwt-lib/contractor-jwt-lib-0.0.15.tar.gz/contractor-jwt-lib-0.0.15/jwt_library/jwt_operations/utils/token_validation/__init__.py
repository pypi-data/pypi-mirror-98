
from calendar import timegm
from datetime import datetime, timedelta
from jose import jwk
from jose.exceptions import JWTClaimsError, ExpiredSignatureError
from jose.utils import base64url_decode
from six import string_types

from jwt_library.jwt_operations.utils.errors import AuthError

def verify_issuer(payload, issuer):
    if payload['iss'] != "https://" + issuer + "/":
        raise JWTClaimsError('Invalid Issuer')

def verify_cid(payload, cid_list):
    if not payload['cid'] in cid_list:
        raise JWTClaimsError('Invalid Client')

def verify_expiration(payload, leeway=0):
    if 'exp' not in payload:
        raise AuthError('Invalid token. No expiration date found.', 401)

    try:
        exp = int(payload['exp'])
    except ValueError:
        raise JWTClaimsError('Expiration Time payload (exp) must be an integer.')

    now = timegm(datetime.utcnow().utctimetuple())

    if exp < (now - leeway):
        raise ExpiredSignatureError('Token is expired.')

def verify_audience(payload, audience=None):
    if 'aud' not in payload:
        raise AuthError('Invalid token. No audience claim found.', 401)


    audience_c = payload['aud']

    if any(not isinstance(c, string_types) for c in audience_c):
        raise JWTClaimsError('Invalid claim format in token')
    if audience not in audience_c:
        raise JWTClaimsError('Invalid Audience')

def verify_iat(payload, leeway=300):
    time_now_with_leeway = datetime.utcnow() + timedelta(seconds=leeway)
    acceptable_iat = timegm((time_now_with_leeway).timetuple())

    if 'iat' in payload and payload['iat'] > acceptable_iat:
        raise JWTClaimsError('Invalid Issued At(iat) Time')

def validate_signature(token: str, rsa_key: dict) -> bool:
    """[summary]

    Args:
        token ([type]): [description]
    """
    key = jwk.construct(rsa_key)
    message, encoded_sig = token.rsplit('.', 1)
    decoded_sig = base64url_decode(encoded_sig.encode('utf-8'))
    valid = key.verify(message.encode(), decoded_sig)
    return valid

def validate_claims(payload, issuer, audience, cid_list=None):
    """ Validates Issuer, Client IDs, Audience
    Issued At time and Expiration in the Payload
    """
    if cid_list:
        verify_cid(payload, cid_list)

    verify_issuer(payload, issuer)
    verify_audience(payload, audience)
    verify_expiration(payload)
    verify_iat(payload)
    return True