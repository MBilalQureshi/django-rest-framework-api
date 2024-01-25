from rest_framework import serializers
from .models import Profile
from followers.models import Follower

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    # serializerMethodField is read only
    is_owner = serializers.SerializerMethodField()

    # To check who are we following
    following_id = serializers.SerializerMethodField()

    # Add counts made in profile list view here now, source not needed
    posts_count = serializers.ReadOnlyField()
    follower_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    # above is_owner is connected when saying below get_is_owner
    def get_is_owner(self, obj):
        # how to check if rquest.user is same as objects owner, see part of solution in view.py see "SOL" after adding SOL is context={'request': request} we come
        # back here and pass into our serializer likw below
        request = self.context['request']
        return request.user == obj.owner

    # Method to check who we are following
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            # check if user is following any other profiles using filter
            following = Follower.objects.filter(
                # if logged in user (owner=user) is following this profile (followed=obj.owner) an instance will be returned else None is returned
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        # if not authenticated user return None
        return None

    class Meta:
        model = Profile
        # In response, inside fields could list them  all in an array or set to fields = '__all__'
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'content', 'image', 
            'is_owner', 'following_id', 'posts_count','follower_count','following_count'
        ]