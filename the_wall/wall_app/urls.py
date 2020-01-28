from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register), #POST
    path('success', views.success), #GET
    path('logout', views.logout), #GET
    path('login', views.login), #POST
    path('new_message', views.new_message), #POST
    path('new_comment/<int:id>', views.new_comment), #POST
    path('message/<int:id>/delete', views.delete_message), #POST
    path('comment/<int:id>/delete', views.delete_comment)
]