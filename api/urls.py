from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.getRoutes),
    path("profiles/", views.getProfiles),
    path('profile/<str:pk>', views.getProfile),
    path("posts/", views.getPosts),
    path("post/<str:pk>", views.getPost),
    path('like_post/<str:pk>/', views.likePost),
    path('remove_post/<str:pk>', views.removePost),

    path('users/token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),

]