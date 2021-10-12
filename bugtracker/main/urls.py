from django.urls import path
from .views import *

from rest_framework.authtoken.views import obtain_auth_token
#Не сработал Unable to log in with provided credentials.
urlpatterns = [
    path('auth/', AuthPageView.as_view()),
    path('manage/', ManagePageView.as_view()),
    path('tasks/', AllTasksPageView.as_view()),
    path('tasks/<int:pk>/', TaskPageView.as_view()),
    ]