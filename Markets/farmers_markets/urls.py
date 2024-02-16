from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('markets/', views.MarketsListView.as_view(), name='markets'),
    path('market/<int:pk>', views.MarketsDetailView.as_view(), name='markets-detail'),
]