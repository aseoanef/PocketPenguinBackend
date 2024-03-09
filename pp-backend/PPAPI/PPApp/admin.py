from django.contrib import admin

# Register your models here.
from .models import Shop_list
from .models import User
from .models import Products
from .models import Family
from .models import Chat
from .models import ProductsinLists

admin.site.register(ProductsinLists)
admin.site.register(Shop_list)
admin.site.register(User)
admin.site.register(Products)
admin.site.register(Family)
admin.site.register(Chat)



