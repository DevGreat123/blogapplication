from django.urls import path
from .views import SignUpView,CustomLoginView,HomePageView,BlogDetailView,BlogSearchView,AddCommentView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('home-page/', HomePageView.as_view(), name='home_page'),
    path('specfic-blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs-result/search/', BlogSearchView.as_view(), name='blog_search'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
]