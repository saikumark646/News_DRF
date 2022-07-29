from django.urls import path
from news_app.api.func_api_views import article_list_create_api_view, article_detail_api_view

from news_app.api.class_api_views import ArticleListCreateView, ArticleDetailView

from news_app.api.class_api_views import JournalistcreateListView, JournalistDetailView

urlpatterns = [
    # func based views
    # path('article/', article_list_create_api_view,name='article_list_create_api_view'),
    # path('article/<int:pk>/', article_detail_api_view,name='article_detail_api_view')


    # class based views
    path('article/', ArticleListCreateView.as_view(),
         name='ArticleListCreateView'),

    path('article/<int:pk>/', ArticleDetailView.as_view(),
         name='Article-Detail'),

    path('jour/', JournalistcreateListView.as_view(),
         name='JournalistcreateListView'),

    path('jour/<int:pk>/', JournalistDetailView.as_view(),
         name='JournalistDetailView')
]
