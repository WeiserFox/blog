from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.Home.as_view()),
    path('home', views.Home.as_view()),
    path('post', views.Post.as_view()),
    path('about', views.About.as_view()),
    path('contacts', views.Contacts.as_view()),
    path('authorization', views.Auth.as_view()),
    path('register/', views.Register.as_view()),
    path('logout/', views.Logout.as_view()),
    path('profile', views.Profile.as_view()),
    path('rename', views.Rename.as_view()),
    path('repassword', views.ChangePassword.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
