from django.urls import path

from . import views

app_name = 'mutapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('metadata/<int:pk>/', views.DetailViewMeta.as_view(), name='metadata'),
    path('mutation/<int:pk>/', views.DetailViewMut.as_view(), name='mutation'),
    path('queryname/', views.query_by_name, name='queryname'),
    path('querymutation/', views.query_by_mutation, name='querymutation'),

]