'''
APIView is very similar to Django’s View  class. It also provides a few bits of extra  
functionality such as making sure you  receive Request instances in your view,  
handling parsing errors, and adding  context to Response objects.

Even though we could use Django’s HttpResponse,  
the Response class is specifically built for the  rest framework, and provides a nicer interface for  
returning content-negotiated Web API responses  that can be rendered to multiple formats.
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile

class ProfileView(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        return Response(profiles)