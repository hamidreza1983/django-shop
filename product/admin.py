from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(ProductAttribute)
admin.site.register(ProductComment)
admin.site.register(ProductReplay)
admin.site.register(ProductsColor)
admin.site.register(ProductScore)
admin.site.register(Attribute)
admin.site.register(Guarantee)

# Register your models here.
