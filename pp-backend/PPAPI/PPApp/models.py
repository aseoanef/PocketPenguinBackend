from django.db import models
# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=50, blank=True)
    price = models.FloatField(null=True)


    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price

        }


class Family(models.Model):
    family_hash = models.CharField(max_length=30, unique=True)
    def to_json(self):
        return{
            "family_id":self.pk,
            "family_hash":self.family_hash,
        }

class User(models.Model):
    e_mail = models.CharField(max_length=260, unique=True)
    username = models.CharField(max_length=240)
    encrypted_password = models.CharField(max_length=120)
    family = models.ForeignKey('Family', on_delete=models.CASCADE, default='')
    user_token = models.CharField(max_length=45, unique=True, null=True, blank=True)
    imageUrl = models.CharField(max_length=500,null=False,default="https://raw.githubusercontent.com/GaelRGuerreiro/fotosPingu/main/pinguino10.jpg")
    def to_json(self):
        return {
            'username': self.username,
            'email': self.e_mail,
            'password': self.encrypted_password,
            'family': self.family.pk,
            'user_token': self.user_token,
            'imageUrl': self.imageUrl
        }


class Chat(models.Model):
    date = models.DateTimeField(auto_now=True)
    family = models.ForeignKey('Family', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=1000)
    def __str__(self):
        return self.message
    def to_json(self):
        return {
            "chat_id":self.pk,
            "date":self.date,
            "user":self.user.username,
            "message":self.message,
            "family":self.family.pk
        }


class Shop_list(models.Model):
    list_name = models.CharField(max_length=100)
    family = models.ForeignKey('Family', on_delete=models.CASCADE, default='')
    def to_json(self):
        return {
            "id": self.id,
            "name": self.list_name,
            "family": self.family.family_hash

        }


class ProductsinLists(models.Model):
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    list = models.ForeignKey(Shop_list, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=0)
    bought = models.BooleanField(default=False)
    def to_json(self):
        return {
            "productinlist_id":self.pk,
            "product_name":self.product.name,
            "list":self.list.pk,
            "quantity":self.quantity,
            "bought":self.bought,
        }






