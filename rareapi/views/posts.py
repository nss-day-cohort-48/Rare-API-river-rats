from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post
from rareapi.models import Category
from rareapi.models import RareUser



class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['label']


class PostSerializer(serializers.ModelSerializer):
    rare_user = PostUserSerializer(many=False)
    category_id = PostCategorySerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'rare_user', 'category_id', 'title',
                  'publication_date', 'image_url', 'content', 'approved']


class PostView(ViewSet):

    def create(self, request):
        """Handle POST operations for posts"""

        rare_user = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.category_id = Category.objects.get(pk=request.data["category"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post"""

        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        rare_user = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.category_id = Category.objects.get(pk=request.data["category"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to events resource

        Returns:
            Response -- JSON serialized list of events
        """
        # Get the current authenticated user
        rare_user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.all()

        for post in posts:

            post.joined = category_id in post.category_id.all()

        # Support filtering posts by category
        category = self.request.query_params.get('category_id', None)
        if category is not None:
            posts = posts.filter(category=type)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)
