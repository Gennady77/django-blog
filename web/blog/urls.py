from django.urls import path

from main.views import TemplateAPIView

app_name = 'blog'


urlpatterns = [
    path('blog/', TemplateAPIView.as_view(template_name='blog/post_list.html'), name='blog-list'),
    path('blog/detail/', TemplateAPIView.as_view(template_name='blog/post_detail.html'), name='blog-detail'),
]
