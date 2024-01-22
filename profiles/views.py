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
# now we add our serializer in view to fix 'Object of type Profile is not JSON serializable' bug
from .serializers import ProfileSerializer
from django.http import Http404
from rest_framework import status

class ProfileList(APIView):
    '''
    List all profiles
    No Create View (post method), as profile creation is handled by django "Signals"
    '''
    def get(self, request):
        profiles = Profile.objects.all()
        '''
        Before we return a Response, we’ll create  a ProfileSerializer instance.
        We’ll pass in profiles and many equals True, to specify  we’re serializing multiple Profile instances.
        Finally, in the Response, we’ll send  data returned from our serializer.
        '''
        # many = True means we'll pass multiple profile instances
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

class ProfileDetail(APIView):
    #    wouldn’t  it be better to have a nice form instead?   
    # If we explicitly set the serializer_class attribute  on our ProfileDetail view, the rest framework  
    # will automatically render a form for us, based on  the fields we defined in our ProfileSerializer.
    # Now, if we save and refresh,  a proper form appears inshort beautify and fix form as per DB.
    serializer_class = ProfileSerializer

    # We need code to handle request for profile id that dosen't exist,(see below)
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        # get single profile based on id so no manyu=true
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)