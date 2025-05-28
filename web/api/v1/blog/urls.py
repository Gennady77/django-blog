from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('list/', views.ArticleListView.as_view({ 'get': 'list' }), name='articles'),
    path('detail/<int:id>/', views.ArticleDetailView.as_view(), name='detail'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('comment/<int:article_id>/', views.CommentListView.as_view(), name='comment_list'),
    path('comment/<int:article_id>/<int:parent_id>/', views.CommentAnswerListView.as_view(), name='comment_answer_list')
]
