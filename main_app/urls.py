from . import views
from django.urls import path

app_name = 'main_app'

urlpatterns = [
    path('upload/', views.upload_file_view, name='upload'),
    # path('upload/', views.UploadView.as_view(), name='upload'),
    path('<str:action>/', views.do_action_view, name='action'),


]
