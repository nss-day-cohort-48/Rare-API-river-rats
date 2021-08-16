"""View module for handling requests about tags"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Tag


class TagView(ViewSet):
    """The view for the Tag model
    methods:
        list: returns a list of all Categories
        retrieve: returns a single tag type based on id
    """

    def retrieve(self, request, pk):
        """Retrieves a single Tag
        Args:
            request (Request): the request object
            pk (int): the id requested in the url
        Returns:
            Response: serialized tag object
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(
                tag, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Gets all tags in the database
        Args:
            request (Request): the request object
        Returns:
            Response: serialized list of all tags
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(
            tags, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized tag instance
        """

        # Create a new Python instance of the Tag class
        # and set its properties from what was sent in the
        # body of the request from the client.
        tag = Tag()
        tag.label = request.data["label"]

        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a tag
        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Tag, get the tag record
        # from the database whose primary key is `pk`
        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]

        tag.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tag
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TagSerializer(serializers.ModelSerializer):
    """Tag model serializer returns __all__ fields
    """
    class Meta:
        model = Tag
        fields = '__all__'