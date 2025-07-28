from django.contrib import admin
from .models import CategoryDb,PlaceDb,ShopDb, Place_visited
# Register your models here.
admin.site.register(CategoryDb)
admin.site.register(PlaceDb)
admin.site.register(ShopDb)
admin.site.register(Place_visited)
