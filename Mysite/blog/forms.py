from django import forms

from .models import BlogPost
from django.contrib.auth import get_user_model
from .models import Contact


User = get_user_model()


# class BlogPostForm(forms.Form):
# 	title = forms.CharField()
# 	description = forms.CharField(widget=forms.Textarea)




class LoginForm(forms.Form):
	"""docstring for LoginForm"""
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class RegisterForm(forms.Form):
	"""docstring for LoginForm"""
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("Username already taken")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("Email already taken")
		return email


	def clean(self):
		data = self.cleaned_data
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password2 != password:
			raise forms.ValidationError("Password must match")
			print("Password not matched")
		return data

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		# fields = ('first_name', 'last_name', 'email', 'phone_number', 'message')
		fields = "__all__" 
		widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'First Name', 'title': 'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}),
            'message':forms.Textarea(attrs={'class':'form-control', 'size': '400', 'placeholder':'Message'}),
         }


class BlogPostModelForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ['title','description','image']
		widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','required': True, 'placeholder':'Title', 'title': 'Title'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'size': '400', 'placeholder':'Description'}),
              
         }
	def clean_title(self, *args, **kwargs):
		instance = self.instance

		title = self.cleaned_data.get('title')
		qs = BlogPost.objects.filter(title__iexact=title)
		if instance is not None:
			qs = qs.exclude(pk=instance.pk)
		if qs.exists():
			raise forms.ValidationError("This title already used")
		return title
