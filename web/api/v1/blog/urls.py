from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('list/', views.ArticleListView.as_view({ 'get': 'list' }), name='articles'),
    path('detail/<int:id>/', views.ArticleDetailView.as_view(), name='detail')
]
