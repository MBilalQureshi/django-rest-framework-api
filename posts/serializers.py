from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # owner: read only field
    owner = serializers.ReadOnlyField(source='owner.username')
    # is_owner: a serializer method field
    is_owner = serializers.SerializerMethodField()
    # profile_id: a read only field populated with the owner’s profile id.
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    # profile_image: a read only field populated with the owner's profile image url.
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        # In response, inside fields could list them  all in an array or set to fields = '__all__'
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image', 'created_at', 'updated_at', 'title', 'content', 'image'
        ]