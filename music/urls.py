from django.urls import path
from . import views


app_name = 'music'

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:pk>/', views.detail, name='detail'),

    path('album/add/', views.AlbumCreate.as_view(), name='add-album'),

    path('album/<int:pk>/', views.AlbumUpdate.as_view(), name='update-album'),

    path('album/<int:pk>/delete', views.AlbumDelete.as_view(), name='delete-album'),

    path('song/add/', views.SongCreate.as_view(), name='add-song'),

    path('songs/', views.songs, name='songs'),

    path('song/<int:pk>/delete', views.SongDelete.as_view(), name='delete-song'),

    path('register/', views.register, name='register'),

    path('login_user/', views.login_user, name='login_user'),

    path('logout_user/', views.logout_user, name='logout_user'),
]