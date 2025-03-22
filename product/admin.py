from django.contrib import admin
from product.models import Category, Product, Review, ProductImage

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ProductImage)
