from django.http import HttpResponsePermanentRedirect

#!!! FORBIDDEN !!!
# should be handled by Apache.
class ForceHTTPSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.is_secure():
            secure_url = request.build_absolute_uri().replace('http://', 'https://', 1)
            return HttpResponsePermanentRedirect(secure_url)

        return self.get_response(request)
