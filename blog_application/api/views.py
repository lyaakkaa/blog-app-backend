from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import User, Topic, Post
from .serializers import UserSerializer, TopicSerializer, PostSerializer
import logging
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializers import UserSerializer
from rest_framework_jwt.settings import api_settings 
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'], url_path='posts')
    def user_posts(self, request, pk=None):
        user = self.get_object()
        posts = Post.objects.filter(user=user)  # Get all posts for the specific user
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.get_object()  # This retrieves the user by the ID provided in the URL (e.g., /api/users/1/)

        # Proceed with the update for the user with the given ID in the URL
        partial = kwargs.pop('partial', False)  # Handles PATCH for partial updates
        serializer = self.get_serializer(user, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, partial=True)

    @action(detail=True, methods=['post'], url_path='toggle_favorite')
    def toggle_favorite(self, request, pk=None):
        user = self.get_object()  # The user whose favorites list we're modifying
        favorite_user_id = request.data.get('favorite_user_id')

        # Check if the favorite_user_id was provided
        if not favorite_user_id:
            return Response({'error': 'You must provide a favorite_user_id.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite_user = User.objects.get(id=favorite_user_id)  # The user being added or removed from favorites
        except User.DoesNotExist:
            return Response({'error': 'The user you are trying to add/remove does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is not adding/removing themselves
        if user.id == favorite_user.id:
            return Response({'error': 'You cannot add/remove yourself as a favorite.'}, status=status.HTTP_400_BAD_REQUEST)

        # Toggle the favorite status: if the user is already in favorites, remove them; otherwise, add them
        if favorite_user in user.favorite_users.all():
            user.favorite_users.remove(favorite_user)
            user.save()
            return Response({'message': 'User removed from favorites successfully.'}, status=status.HTTP_200_OK)
        else:
            user.favorite_users.add(favorite_user)
            user.save()
            return Response({'message': 'User added to favorites successfully.'}, status=status.HTTP_200_OK)


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.is_liked = not post.is_liked  
        post.like_count += 1 if post.is_liked else -1  
        post.save()
        return Response({'like_count': post.like_count, 'is_liked': post.is_liked})



logger = logging.getLogger(__name__)
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class SignInView(APIView):
    def post(self, request):
        try:
            login = request.data.get('login')
            password = request.data.get('password')

            print(f"Received login: {login}, password: {password}")

            # Attempt to authenticate the user
            user = User.objects.filter(login=login).first()
            if user and user.password == password:  
                token = jwt_encode_handler(
                    {'userID': user.id, 'exp_time': int((datetime.now() + timedelta(days=1)).timestamp())})

                return Response({
                    'token': str(token),
                    'id': user.id,
                }, status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed('Invalid credentials')

        except Exception as e:
            logger.error(f"An error occurred in SignInView: {str(e)}")
            return Response({'error': 'Internal Server Error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Check if the login is already taken
            existing_user = User.objects.filter(login=request.data['login']).exists()
            if existing_user:
                return Response({'error': 'Login already taken. Please choose a different login.'}, status=400)


            user = serializer.save()

            token = jwt_encode_handler(
                {'userID': user.id, 'exp_time': int((datetime.now() + timedelta(days=1)).timestamp())})

            return Response({
                'token': str(token),
                'id': user.id,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)