from rest_framework import serializers
from .models import Post
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    # owner: read only field
    owner = serializers.ReadOnlyField(source='owner.username')
    # is_owner: a serializer method field
    is_owner = serializers.SerializerMethodField()
    # profile_id: a read only field populated with the owner’s profile id.
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    # profile_image: a read only field populated with the owner's profile image url.
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    like_id = serializers.SerializerMethodField()

    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    # as the db field that needs to be vlidated is image so method would be validate_image "If we follow this naming convention,  this method will be called automatically  
    # and validate the uploaded image every  time we create or update a post."
    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                "Image size larger than 2MB!"
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                "Image width larger tha 4096px!"
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                "Image height larger tha 4096px!"
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                # see if currently logged in user is the user who liked the post we are trying to retrieve
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        # In response, inside fields could list them  all in an array or set to fields = '__all__'
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image', 'created_at', 'updated_at', 'title', 'content', 'image',
            'image_filter', 'like_id', 'likes_count', 'comments_count'
        ]