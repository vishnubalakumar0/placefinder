from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    phone = models.IntegerField(null=True)


class CategoryDb(models.Model):
    categoryname = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryname
    



class PlaceDb(models.Model):
    place_name = models.CharField(max_length=100)

    def __str__(self):
        return self.place_name


class ShopDb(models.Model):
    shop_name= models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.IntegerField()
    remark = models.CharField(max_length=100)
    category_name = models.ForeignKey(CategoryDb,on_delete=models.CASCADE,null=True)
    place = models.ForeignKey(PlaceDb,on_delete=models.CASCADE, null=True)
    shopimage = models.ImageField(upload_to="images", null=True, blank=True)


    def __str__(self):
        return self.shop_name
    



class Place_visited(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True)
    time = models.TimeField()
    purpose  = models.CharField(max_length=100)
    category = models.ForeignKey(CategoryDb,on_delete=models.CASCADE, null=True)
    place = models.ForeignKey(PlaceDb,on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(ShopDb, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.purpose



