from rest_framework import serializers
from .models import User, Topic, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'avatar': {'required': False},
            'age': {'required': False, 'allow_null': True},
            'location': {'required': False}
        }
    def get_avatar(self, obj):
        request = self.context.get('request')  # Access the current request from the context
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']  

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()  
    topic = TopicSerializer()  

    class Meta:
        model = Post
        fields = ['id', 'pub_date', 'rating', 'commentary', 'is_liked', 'like_count', 'user', 'topic'] 
