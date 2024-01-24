from rest_framework import serializers
from .models import Like
from django.db import IntegrityError

class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # Note: We don't need a get_is_owner method here because we don't need to know if the currently logged in user is the owner of a like.
    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'post']

    # Now to make sure user dosn't like same post more than 1 time
    def create(self, validated_data):
        try:
            # This create method is on the model serializer  and for that reason I had to call “super()”.
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })