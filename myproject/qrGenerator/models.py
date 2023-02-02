from django.db import models

# Create your models here.



class User(models.Model):
    name= models.CharField(max_length=30 ,blank = True)
    id= models.CharField(max_length=30, blank=True, primary_key = True) #unique_field
    items=models.ManyToManyField("Item") #changed the parameter to string representation as the Item class is declared later


    def __str__(self):
      return self.name
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Item(models.Model):
    id= models.CharField(max_length=30, blank=True, primary_key = True)
    title= models.TextField(max_length=30)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)#each item can only have one owner
    description = models.TextField(max_length=100)
    estimated_price=models.CharField(max_length=10)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"




