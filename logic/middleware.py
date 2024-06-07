from django.utils.deprecation import MiddlewareMixin

class SessionAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.session.get('access_token')
        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'