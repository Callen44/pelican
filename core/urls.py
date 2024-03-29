from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('',views.index, name='index'),
    path('create/',views.create, name='create'),
    path('<int:pk>/update/',views.update, name = 'update'),
    path('<int:pk>/delete/',views.delete, name = 'delete'),
    path('<int:pk>/like',views.like, name = "like"),
    path('<int:pk>/<int:pid>/delete_comment',views.delete_comment, name="delete_comment")
]