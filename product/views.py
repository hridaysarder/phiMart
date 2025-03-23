from product.models import Product, Category, Review, ProductImage
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from product.permissions import IsReviewAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
    - Allows authenthicated admin to create,update, and delete product
    - Allows user to browse and filter products
    - Support searching by name,description, and category
    - Support ordering by price and updated_at
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(operation_summary='User can retrive all the product')
    def list(self, request, *args, **kwargs):
        """Retrive all the products"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Create a product by admin',
        operation_description='This allow admin to create a product',
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category_id')

        if category_id is not None:
            queryset = Product.objects.filter(category_id=category_id)
        return queryset


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}
