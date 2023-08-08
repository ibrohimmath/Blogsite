from django.urls import path 

from . import views 

urlpatterns = [
    path('about/', views.aboutView, name = 'about'),
    path('contact/', views.contactView, name = 'contact'),
    
    path('', views.index, name = 'index'),
    path('signup/', views.register, name = 'signup'),
    path('login/', views.login, name = 'login'),
    path('logut/', views.logout, name = 'logout'),

    path('article/create/', views.articleCreateView, name = 'article_create' ),
    path('article/edit/<int:id>/', views.articleUpdateView, name = 'article_update'),
    path('article/delete/<int:id>/', views.articleDeleteView, name = 'article_delete'),
    path('article/<int:id>/', views.articleDetailView, name = 'article_detail'),
    
    path('comment/<int:id>/new/', views.commentCreateView, name = 'comment'),
    path('reply/<int:id>/', views.replyView, name = 'reply'),
    
    path('tag/<str:tag>/', views.tagView, name = 'tag'),
]