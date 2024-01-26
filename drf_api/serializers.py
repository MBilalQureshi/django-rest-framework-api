# Now we need to add the profile_id  and profile_image to fields returned when  
# requesting logged in user’s details.  This way we’ll know which profile to  
# link to and what image to show in the  navigation bar for a logged in user.
# The documentation here tells us how  to extend their UserDetailsSerializer.
# In drf_api, I’ll create the serializers.py file  and paste in the code. All we’re doing here is  
# adding the profile_id and profile_image fields, so  I just provided you with the code under the video.
# Now that we’ve created the file, let’s overwrite the default USER_DETAILS_SERIALIZER in settings.py.
# https://dj-rest-auth.readthedocs.io/en/latest/faq.html
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )