from django.urls import path
from post import views
urlpatterns = [

    path('', views.index, name='index'),
    path('createpost/', views.create_post, name='createpost'),
    path('<uuid:post_id>', views.post_details, name='post_details'),
    path('<uuid:post_id>/like', views.post_like, name='post_like'),
]
