from django.urls import path
from forums import views

urlpatterns = [
    path('create/', views.PostCreateView.as_view()),
    path('detail/<int:pk>/', views.PostDetailView.as_view()),
    path('list/', views.PostListView.as_view()),
    path('list/<int:pk>/like/', views.like),
    path('list/<int:pk>/liked/', views.liked),
    path('detail/<int:pk>/like/', views.like),
    path('detail/<int:pk>/liked/', views.liked),
    path('update/<int:pk>/', views.PostUpdateView.as_view()),
    path('delete/<int:pk>/', views.PostDeleteView.as_view()),

    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('ratings/create/', views.RatingCreateApiView.as_view()),
]