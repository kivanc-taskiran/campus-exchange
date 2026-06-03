from django.urls import path
from . import views

urlpatterns = [
    # Ana sayfa
    path('', views.index, name='index'),

    # İlan işlemleri
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/new/', views.item_create, name='item_create'),
    path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('item/<int:pk>/sold/', views.item_mark_sold, name='item_mark_sold'),

    # Mesajlaşma sistemi
    path('inbox/', views.inbox, name='inbox'),
    path('messages/start/<int:item_pk>/', views.start_conversation, name='start_conversation'),
    path('messages/<int:pk>/', views.conversation_detail, name='conversation_detail'),

    # Kullanıcı kaydı
    path('register/', views.register, name='register'),
]
