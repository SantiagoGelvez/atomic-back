import jwt

from rest_framework.exceptions import AuthenticationFailed

from users.models import User


def get_user_from_jwt_token(token):
    """
    Get user from JWT token
    :param token:
    :return: User
    """
    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')

    user = User.objects.get(uuid=payload['uuid'])
    return user
