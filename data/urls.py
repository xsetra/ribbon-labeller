from django.urls import path
from data import views

app_name = 'data'

urlpatterns = [
    path('', views.index, name='home'),
    path('label/', views.label, name='label'),
    path('save/labels/', views.save_labels, name='save_labels'),
    path('label/score/', views.label_score, name='label_score'),
]