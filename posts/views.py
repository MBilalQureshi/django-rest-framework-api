from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from django.http import Http404
# Importing the permission we made in drf_api
from drf_api.permissions import IsOwnerOrReadOnly

class PostList(APIView):
    # Like we said before below line of code is to beautify the form as per db
    serializer_class = PostSerializer

    # Adding buit-in permission it's not like ou made permission in drf_api
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

class PostDetail(APIView):
    permission_classes = [
        IsOwnerOrReadOnly
    ]
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            # check if user had permission to add or delete
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request,pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        # SOL is context={'request': request} making request part of context object to access it in serializer.py side
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)