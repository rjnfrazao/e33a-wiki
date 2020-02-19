
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="encyclopedia_index"),
    path("<encyclopedia_name>", views.detail, name="encyclopedia_detail"),
    path("search/", views.search, name="encyclopedia_search"),
    path("add/", views.add, name="encyclopedia_add")

]
