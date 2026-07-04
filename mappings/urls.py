from django.urls import path

from mappings import views

urlpatterns = [
    path('', views.MappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:pk>/', views.MappingManageView.as_view(), name='mapping-manage'),
]
