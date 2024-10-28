from django.urls import path
from .views import view_edit_organization

urlpatterns = [
    path('organization/', view_edit_organization, name='view_edit_organization'),
]
