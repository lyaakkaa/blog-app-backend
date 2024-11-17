from rest_framework import serializers
from .models import User, Topic, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'avatar': {'required': False} 
        }

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
