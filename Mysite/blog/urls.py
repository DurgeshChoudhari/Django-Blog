from django.urls import path, include
from django.conf.urls import url
from .views import home_page, blog_list_view, blog_detail_view, create, update,about, delete,contact,login_page,user_logout, register_page


app_name = 'blog'

urlpatterns = [
    path('', home_page, name='home'),
    path(r'blog/create/', create, name='create'),
    path(r'blog/<str:slug>/', blog_detail_view, name='blog_detail_view'),
    path(r'blog/<str:slug>/edit', update, name='edit'),
    path(r'blog/<str:slug>/delete', delete, name='delete'),
    path(r'blog/', blog_list_view, name='blog'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    url(r'^login/$', login_page, name='login'),
    url(r'^register/$', register_page, name='register'),
    url(r'^logout/$', user_logout, name='logout'),

]
