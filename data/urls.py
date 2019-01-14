from django.urls import path
from data import views

app_name = 'data'

urlpatterns = [
    path('', views.index, name='home'),
    path('label/', views.label, name='label'),
    path('save/labels/', views.save_labels, name='save_labels'),
    path('label/score/', views.label_score, name='label_score'),
    path('upload/dataset/', views.upload_dataset, name='upload_dataset'),
    path('train/model/', views.train_model, name='train_model'),

    path('train/aspect/', views.train_model_aspect, name='train_aspect'),
    path('predict/aspect/', views.predict_aspect, name='predict_aspect'),
    path('test/aspect/', views.test_model_aspect, name='test_aspect'),

    path('train/polarity/', views.train_model_polarity, name='train_pol'),
    path('predict/polarity/', views.predict_polarity, name='predict_pol'),
    path('test/polarity/', views.test_model_polarity, name='test_pol'),
]
