from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list_view, name='list'),
    path('<int:pk>/', views.project_detail_view, name='detail'),
    path('create-project/', views.create_project_view, name='create'),
    path('<int:pk>/edit/', views.edit_project_view, name='edit'),
    path('<int:pk>/complete/', views.complete_project_view, name='complete'),
    path('<int:pk>/toggle-participate/', views.toggle_participate_view, name='toggle_participate'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('favorites/', views.favorite_projects_view, name='favorites'),
]