from django.contrib import admin

# Register your models here.
from home.models import Category , Product


class CategoryAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)

admin.site.register(Category)
admin.site.register(Product,ProductAdmin)