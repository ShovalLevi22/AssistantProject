from . import views
from django.urls import path

app_name = 'main_app'

urlpatterns = [
    path('upload/', views.upload_file_view, name='upload'),
    path('', views.CommandListView.as_view(), name='home'),
    path('<str:action>/', views.do_action_view, name='command'),
]
