import random
import os
from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.urls import reverse
from django.core.validators import RegexValidator
from django.conf import settings






def get_filenam_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	print(instance)
	print(filename)
	new_filename = random.randint(1,9999999999)
	name, ext = get_filenam_ext(filename)
	final_filename = '{new_filename}{ext}'.format(new_filename= new_filename, ext=ext)
	return "blog/{new_filename}/{final_filename}".format(
		new_filename= new_filename, 
		final_filename=final_filename)




User = settings.AUTH_USER_MODEL
class BlogPost(models.Model):
	user = models.ForeignKey(User, default = 1,blank=True, null=True, on_delete = models.SET_NULL)
	title = models.CharField(max_length= 120)
	slug  = models.SlugField(blank=True, unique=True)
	description = models.TextField(null=True, blank=True, max_length= 1200)
	image = models.ImageField(upload_to = upload_image_path,null=True, blank=True)
	
	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return "/blog/{slug}/".format(slug=self.slug)

	def get_edit_url(self):
		return "/blog/{slug}/edit".format(slug=self.slug)

	def get_delete_url(self):
		return "/blog/{slug}/delete".format(slug=self.slug)

def blog_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(blog_pre_save_receiver, sender=BlogPost)	






class Contact(models.Model):
	first_name = models.CharField(max_length= 50)
	last_name = models.CharField(max_length= 50)
	email  = models.EmailField(unique=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	message = models.TextField(max_length = 200)

	def __str__(self):
		return self.first_name



	