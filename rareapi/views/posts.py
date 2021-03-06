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
        fields = ['id', 'first_name', 'last_name', 'email']


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']


class PostSerializer(serializers.ModelSerializer):
    rare_user = PostUserSerializer(many=False)
    category = PostCategorySerializer(many=False)

    class Meta:
        model = Post
        fields = ['id', 'rare_user', 'category', 'title',
                  'publication_date', 'image_url', 'content', 'approved']


class PostView(ViewSet):

    def create(self, request):
        """Handle POST operations for posts"""

        rare_user = RareUser.objects.get(user=request.auth.user)
        category_id = Category.objects.get(pk=request.data["category_id"])

        post = Post()
        post.rare_user = rare_user
        post.category = category_id
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]

        # rare_user = RareUser.objects.get(user=request.auth.user)

        # category_id = Category.objects.filter(
        #     pk=request.data["category_id"]).first()

        # post = Post()
        # post.rare_user = rare_user
        # post.category_id = category_id
        # post.title = request.data["title"]
        # post.publication_date = "2021-08-19"
        # post.image_url = request.data["image_url"]
        # post.content = request.data["content"]
        # post.approved = True
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
        post.rare_user = rare_user
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
        """Handle GET requests to posts resource

        Returns:
            Response -- JSON serialized list of posts
        """
        # Get the current authenticated user
        rare_user = RareUser.objects.get(user=request.auth.user)
        if rare_user is not None:
            posts = Post.objects.filter(rare_user=rare_user)

        else:

            posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)

        #     posts = Post.objects.all()
        #     for post in posts:
        #         post.joined = category_id in post.category_id.all()
        #         category = self.request.query_params.get('category', None)
        #         if category is not None:
        #             posts = posts.filter(category=type)
        # serializer = PostSerializer(
        #     posts, many=True, context={'request': request})
        # return Response(serializer.data)
