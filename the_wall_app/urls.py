from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/register', views.register_user),
    path('user/login', views.login_user),
    path('wall', views.wall),
    path('user/post_message', views.post_message),
    path('user/post_comment/<int:post_id>', views.post_comment),
    path('user/update_comment/<int:comment_id>', views.update_comment),
    path('user/logout', views.logout_user),
    path('comment/<int:comment_id>/edit', views.edit_comment),
    path('comment/<int:comment_id>/delete', views.delete_comment),
]
