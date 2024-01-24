from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

# Now we'll use generics here that had already took care of most of work like get, post, put, delete

# good news is that with generics, the request (context={'request': request}) is a part of the context object by default.  
# What this means is that we no  longer have to pass it manually,  
# like we did in the regular class based views (post and profile views).

# here List is GET and Create is POST
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    # we don't want anonymous users to comment
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Instead of specifying only the model we’d like  to use, in DRF we set the queryset attribute.  
    # This way, it is possible to filter  out some of the model instances.  
    # This would make sense if we were  dealing with user sensitive data  
    # like orders or payments where we would need to  make sure users can access and query only their own data. BUT in this case we want all comments so .all()
    queryset = Comment.objects.all()
    # we’ll have to make sure  comments are associated with a user upon creation.  
    # We do this with generics by  defining the perform_create method,  
    # which takes in self and serializer as arguments.  Inside, we pass in the user making the request as  
    # owner into the serializer’s save method, just  like we did in the regular class based views.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Now this generic view can retrive, update and delete a comment
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsOwnerOrReadOnly
    ]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
    # Our serializer still needs to access the request  like in profile and post context={'request': request} ,  BUT as mentioned before, we don’t really need to  
    # do anything, as the request is passed in  as part of the context object by default.