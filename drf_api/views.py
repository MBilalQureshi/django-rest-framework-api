from rest_framework.decorators import api_view
from rest_framework.response import Response
# 1. In drf_api/views.py, import JWT_AUTH settings from settings.py.
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)

@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to my Django rest framework API!"
    })

'''
Problem Statement
It turns out that dj-rest-auth has a bug that doesn’t allow users to log out (ref: DRF Rest Auth Issues).

The issue is that the samesite attribute we set to ‘None’ in settings.py (JWT_AUTH_SAMESITE = 'None') is not passed to the logout view. 
This means that we can’t log out, but must wait for the refresh token to expire instead.

One way to fix this issue is to have our own logout view, where we set both cookies to an empty 
string and pass additional attributes like secure, httponly and samesite, 
which was left out by mistake by the library.

2. Write a logout view. Looks like quite a bit, but all that’s happening here is that we’re setting the value of both the access token (JWT_AUTH_COOKIE) 
and refresh token (JWT_AUTH_REFRESH_COOKIE) to empty strings. We also pass samesite=JWT_AUTH_SAMESITE, which we set to ’None’ in settings.py 
and make sure the cookies are httponly and sent over HTTPS,
'''


# dj-rest-auth logout view fix
@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response