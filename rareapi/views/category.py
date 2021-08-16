"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category


class CategoryView(ViewSet):
    """The view for the Category model
    methods:
        list: returns a list of all Categories
        retrieve: returns a single category based on id
    """

    def retrieve(self, request, pk):
        """Retrieves a single Category
        Args:
            request (Request): the request object
            pk (int): the id requested in the url
        Returns:
            Response: serialized categorytype object
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Gets all categories in the database
        Args:
            request (Request): the request object
        Returns:
            Response: serialized list of all categories
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, context={'request': request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized category instance
        """

        # Create a new Python instance of the Category class
        # and set its properties from what was sent in the
        # body of the request from the client.
        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a category
        Returns:
            Response -- Empty body with 204 status code
        """
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Category, get the category record
        # from the database whose primary key is `pk`
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]

        category.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single category
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer returns __all__ fields
    """
    class Meta:
        model = Category
        fields = '__all__'