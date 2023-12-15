
from enum import Enum

from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

def expert_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is expert
        jwt_authentication = JWTAuthentication()
        user, _ = jwt_authentication.authenticate(request)

        if user and user.is_expert:
            return view_func(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
    return _wrapped_view

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is staff
        jwt_authentication = JWTAuthentication()
        user, _ = jwt_authentication.authenticate(request)

        if user and user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
    return _wrapped_view
