from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    # serializerMethodField is read only
    is_owner = serializers.SerializerMethodField()
    # above is_owner is connected when saying below get_is_owner
    def get_is_owner(self, obj):
        # how to check if rquest.user is same as objects owner, see part of solution in view.py see "SOL" after adding SOL is context={'request': request} we come
        # back here and pass into our serializer likw below
        request = self.context['request']
        return request.user == obj.owner


    class Meta:
        model = Profile
        # In response, inside fields could list them  all in an array or set to fields = '__all__'
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name', 'content', 'image', 
            'is_owner'
        ]