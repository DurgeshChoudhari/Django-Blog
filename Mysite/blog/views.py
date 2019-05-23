from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import BlogPost
from .forms import BlogPostModelForm, LoginForm, RegisterForm, ContactForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
 
from django.contrib.auth import authenticate, login, get_user_model,logout
from django import forms
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def home_page(request):
	return  render(request, "blog/home_page.html", {})


def about(request):
	return  render(request, "blog/about.html", {})

def login_page(request):
	form = LoginForm(request.POST or None)
	context = {
		"form": form
		# "error": "Username and password not matched"
	}
	
	# print(request.user.is_authenticated())
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request, username = username, password = password)
		print(request.user.is_authenticated)
		print("authenticate")
		if user is not None:
			print(request.user.is_authenticated)
			login(request, user)

			return  redirect("../")
			print("Success")
			# return  render(request, 'apnabazar/list.html', context)

		else:
			print("Error")
			context["error"] = "Inavalid user"
			return render(request, 'auth/login.html', context)
	return render(request, 'auth/login.html', context)

def user_logout(request):
	# if request.method == "POST":
	logout(request)
	return  redirect("/login")
	# return HttpResponseRedirect(reverse('login_page'))
		# form = LoginForm(request.POST or None)
		# context = {
		# 	"form": form
		# }
	# return render(request, 'auth/login.html')

User = get_user_model()


def register_page(request):
	form = RegisterForm(request.POST or None)
	context = {
		"form": form
	}
	# print("user loged in")
	# print(request.user.is_authenticated())
	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		email = form.cleaned_data.get("email")
		password = form.cleaned_data.get("password")
		new_user = User.objects.create_user(username,email,password)
		print(new_user)
	
		# user = authenticate(request, username = username, password = password)
		# print(request.user.is_authenticated)
		# if user is not None:
		# 	print(request.user.is_authenticated)
		# 	login(request, user) 

		# 	return  redirect("/login")
		# else:
		# 	print("Error")
  
	return render(request, 'auth/register.html', context)


def contact(request):
	

	if request.method =="POST":
		form = ContactForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'Sent')

	else:
		form = ContactForm()
	context = {
	'form': form
	}
	return render(request, "blog/contact.html", context)


def blog_list_view(request):
	queryset = BlogPost.objects.all()
	blog_count = len(BlogPost.objects.all())
	template_name = 'blog/list.html'
	context = {
		'object_list': queryset,
		'count' : blog_count
	}
	return  render(request, template_name, context)

@login_required(login_url='/login/')
def blog_detail_view(request, slug):
	# queryset = BlogPost.objects.get(id=3)
	template_name = "blog/detail.html"
	queryset = get_object_or_404(BlogPost, slug=slug)
	
	context = {
		'object_list': queryset
	}
	return  render(request, template_name, context)

@login_required(login_url='/login/')
def create(request):
	form = BlogPostModelForm(request.POST, request.FILES)
	context = {'form': form}
	template_name = "blog/create.html"

	if request.method== "POST":
		form = BlogPostModelForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit= False)
			obj.user = request.user
			obj.save()
			form = BlogPostModelForm()		
	else:
		form=BlogPostModelForm()
		print("ELse part")
		return  render(request, template_name, {'form': form})
	print('without if else')
	return  render(request, template_name, {'form': form})

@login_required(login_url='/login/')
def update(request, slug):
	template_name = "blog/create.html"
	obj = get_object_or_404(BlogPost, slug=slug)
	form = BlogPostModelForm(request.POST, instance = obj)
	if form.is_valid():
		form.save()
		return redirect("/blog/")
	context = {
		'form': form, 
		"title":f"Update {obj.title}"
	}
	return  render(request, template_name, context)			

@login_required(login_url='/login/')
def delete(request, slug):
	template_name = "blog/delete.html"
	obj = get_object_or_404(BlogPost, slug=slug)
	if request.method =="POST":
		obj.delete()	
		return redirect("/blog")
	context = {
		'object_list': obj
	}
	return  render(request, template_name, context)