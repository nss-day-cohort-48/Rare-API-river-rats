from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, RareUser, Comment

class CommentView(ViewSet):
    """RARE Comments"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized comment instance
        """

        # Uses the token passed in the `Authorization` header
        
        author = RareUser.objects.get(user=request.auth.user)


        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]
        comment.post_id = request.data["post"]
        comment.author = author
        

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)


        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment
        Returns:
            Response -- JSON serialized comment instance
        """
        try:
            
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a comment
        Returns:
            Response -- Empty body with 204 status code
        """
        author = RareUser.objects.get(user=request.auth.user)


        comment = Comment()
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]
        comment.post = request.data["post"]
        comment.author = author

        post = Post.objects.get(pk=request.data["postId"])
        comment.post = post
        comment.save()


        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to comments resource
        Returns:
            Response -- JSON serialized list of comments
        """
        comment = Comment.objects.all()


        post = self.request.query_params.get('post', None)  # <<not sure about 'post' here
        if post is not None:
            comment = comment.filter(post__id=post)

        serializer = CommentSerializer(
            comment, many=True, context={'request': request})
        return Response(serializer.data)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments
    Arguments:
        serializer type
    """
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author','content', 'created_on')
        # depth = 1
