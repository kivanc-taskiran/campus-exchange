from django.contrib import admin
from .models import Category, Item, Comment, Conversation, Message


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'owner', 'created_at', 'is_active', 'is_sold')
    list_filter = ('category', 'is_active', 'is_sold')
    search_fields = ('title', 'description')
    # Admin panelinden is_sold toggle edebilsin
    list_editable = ('is_sold',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'item', 'created_at')
    search_fields = ('content',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    # Konuşmaları listeler: hangi ilan, alıcı, satıcı
    list_display = ('item', 'buyer', 'seller', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('item__title', 'buyer__username', 'seller__username')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Tüm mesajları listeler
    list_display = ('sender', 'conversation', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('content', 'sender__username')
