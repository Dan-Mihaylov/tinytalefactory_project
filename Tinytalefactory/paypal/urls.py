from django.urls import path
from . import views


urlpatterns = [
    path('success/', views.SuccessView.as_view(), name='payment-success'),
    path('cancel/', views.CancelView.as_view(), name='payment-cancel'),
]
