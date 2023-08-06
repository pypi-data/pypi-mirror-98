from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='index'),
    path('upload/', views.FileFieldView.as_view(), name='upload'),

]
