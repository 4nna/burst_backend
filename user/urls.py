from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user.views import Register, Detail, Update, CountOnline

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('register/', Register.as_view(), name='register'),
    path('detail/', Detail.as_view(), name='detail'),
    path('update/', Update.as_view(), name='update'),
    path('online/', CountOnline.as_view(), name='count_online')
]
