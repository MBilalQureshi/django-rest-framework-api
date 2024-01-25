from rest_framework import generics, filters
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer
from django.db.models import Count

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    # Aggregation: https://docs.djangoproject.com/en/3.2/topics/db/aggregation/
    # Annotates : https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.annotate
    # Count: https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.Count
    # distinct=True DRF Documentation: double underscore: https://docs.djangoproject.com/en/3.2/topics/db/aggregation/#combining-multiple-aggregations

    serializer_class = ProfileSerializer
    # Annotate function allows us to add extra fields in query set, so we'll change the code below
    # queryset = Profile.objects.all()
    queryset = Profile.objects.annotate(
        # we can use __ to show relation ship between profile(table) -> user(table) -> post(table) so, owner__post, owner(field) is in profile table.
        posts_count = Count('owner__post', distinct=True),
        # This time its owner(field)__followed(field), followed is in Followers table
        follower_count = Count('owner__followed', distinct=True),
        following_count = Count('owner__following', distinct=True)
    ).order_by('-created_at')

    # Adding this very filter will activate filter on front
    filter_backends = [
        filters.OrderingFilter
    ]
    # This below code will only active these filters on front
    ordering_fields = [
        'posts_count',
        'follower_count',
        'following_count',
        # As these are regular database fields, I  don’t need to add them to the queryset,  
        # but I still have to add them  to the ordering_fields list.
        'owner__following__created_at',
        'owner__followed__created_at'
    ]



class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = Profile.objects.all()
    # Just copy the above view code for queryset here to see the effects for single profile as well, obviously filters are not needed for single profile
    queryset = Profile.objects.annotate(
        # we can use __ to show relation ship between profile(table) -> user(table) -> post(table) so, owner__post, owner(field) is in profile table.
        posts_count = Count('owner__post', distinct=True),
        # This time its owner(field)__followed(field), followed is in Followers table
        follower_count = Count('owner__followed', distinct=True),
        following_count = Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer