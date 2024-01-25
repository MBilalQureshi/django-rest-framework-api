from rest_framework import generics, permissions, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer
from django.db.models import Count


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Post.objects.all()
    queryset = Post.objects.annotate(
        comments_count = Count('comment', distinct=True),
        likes_count = Count('likes', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]

    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at',
    ]

    # Adding search
    search_fields = [
        'owner__username',
        'title',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = Post.objects.all()
    queryset = Post.objects.annotate(
        comments_count = Count('comment',distinct=True),
        likes_count = Count('likes',distinct=True)
    ).order_by('-created_at')
