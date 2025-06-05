from django.contrib import admin
from . import models

# Register your models here.
class orderAdmin(admin.ModelAdmin):
  list_display = ['id', 'user_name', 'product_name', 'status', 'total_price']

  def user_name(self, obj):
    return obj.user.username
  
  def product_name(self, obj):
    return obj.product.name



admin.site.register(models.products)
admin.site.register(models.categories)
admin.site.register(models.contactUs)
admin.site.register(models.order, orderAdmin)
