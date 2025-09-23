from django.shortcuts import redirect
from django.conf import settings


class UnderConstructionRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.IS_UNDER_CONSTRUCTION == 'True':
            if request.path != '/under_construction/':
                return redirect('site_under_construction')
        else:
            if request.path != '/':
                return redirect('home')
        response = self.get_response(request)
        return response
