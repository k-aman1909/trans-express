# myapp/middleware.py

from loginapp.models import User

class SuperUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view (middleware logic)
        superusers = User.objects.filter(username=request.user)
        for superuser in superusers:
            if superuser.is_superuser:
                request.s_user = superuser.is_superuser
                request.s_name = superuser.first_name
            else:
                request.s_user = superuser.role  # Assuming you have a 'role' field in your User model
                request.s_name = superuser.first_name
        
        response = self.get_response(request)

        # Code to be executed for each response after the view (if needed)

        return response
