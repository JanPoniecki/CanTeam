from django.contrib import admin
from .models import User42, Product, Action, Sponsor

@admin.register(User42)
class Users42(admin.ModelAdmin):
	list_display=['name', 'balance', 'coffee_score']
	
@admin.register(Product)
class Products(admin.ModelAdmin):
	list_display=['name', 'price', 'scoops']
	
@admin.register(Action)
class Actions(admin.ModelAdmin):
	list_display=['user42', 'product', 'scoops', 'total']

@admin.register(Sponsor)
class Sponsors(admin.ModelAdmin):
	list_display=['user42']
