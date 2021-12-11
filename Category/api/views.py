from .serializers import CategorySerializer
from ..models import Category
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(
    [
        "GET",
    ]
)
def categories_view(request):
    categories = Category.objects.all().order_by("-createdAt")
    serializer = CategorySerializer(categories, many=True, context={"request": request})
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)


@api_view(
    [
        "GET",
    ]
)
def single_category_view(request, pk):
    data = {}
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        data = {"success": False, "details": "Category not found"}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, context={"request": request})
    data = {"success": True, "data": serializer.data}
    return Response(data, status=status.HTTP_200_OK)
