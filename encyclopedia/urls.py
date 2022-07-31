from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/",views.search,name="search"),
    path("wiki/<str:entry>/",views.wiki,name="wiki"),
    path('add/',views.add,name='add'),
    path('wiki/<str:entry>/edit/',views.edit,name='edit'),
    path('wiki/<str:entry>/delete/',views.delete,name='delete'),
    path('random/',views.random,name='random')
    

]
