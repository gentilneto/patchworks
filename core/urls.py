from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.produtos, name='produtos'),
    path('avaliacoes/', views.avaliacoes, name='avaliacoes'),
    path('contato/', views.contato, name='contato'),
    path('api/cep/', views.api_consultar_cep, name='api_consultar_cep'),
    path('api/frete/cotar/', views.api_cotar_frete, name='api_cotar_frete'),
    path('api/melhorenvio/autorizar/', views.melhorenvio_autorizar, name='melhorenvio_autorizar'),
    path('api/melhorenvio/callback/', views.melhorenvio_callback, name='melhorenvio_callback'),
]
