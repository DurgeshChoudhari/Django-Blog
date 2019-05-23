from django.contrib import admin
from .models import BlogPost, Contact

# Register your models here.

class  ProductAdmin(admin.ModelAdmin):
	"""docstring for  ProductAdmin"""
	display = ['__str__', 'first_name']
	class meta:
		model = Contact		



admin.site.register(Contact, ProductAdmin)
admin.site.register(BlogPost)
