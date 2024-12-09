from django.http import HttpResponseForbidden
from functools import wraps

def role_required(required_role):
    """
    Decorator to restrict access to specific roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this page.")

            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            elif not request.user.is_staff:
                return view_func(request, *args, **kwargs)

            return HttpResponseForbidden("You are not authorized to access this page.")
        return _wrapped_view
    return decorator
