from django.contrib.auth import get_user

def navbar_parameters(request):
    user = get_user(request)
    return {
        'session_user': user,
    }