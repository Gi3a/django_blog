#CORE URLS.PY

from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # path('', views.home, name = 'home'),
    # path('detail/<int:id>', views.detail_page, name = 'detail_page'),
    path('', views.HomeListView.as_view(), name = 'home'),
    path('detail/<int:pk>', views.HomeDetailView.as_view(), name = 'detail_page'),
    path('edit/', views.ArticleCreateView.as_view(), name = 'edit'),
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name = 'update'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name = 'delete'),
    path('login/', views.ProjectLoginView.as_view(), name = 'login'),
    path('join/', views.ProjectJoinView.as_view(), name = 'join'),
    path('logout', views.ProjectLogout.as_view(), name = 'logout'),
]
