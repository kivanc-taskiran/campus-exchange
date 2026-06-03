from django.db import models
from django.contrib.auth.models import User


# ─────────────────────────────────────────────
# KATEGORİ MODELİ
# İlan kategorilerini temsil eder (ör: Kitap, Elektronik, Giyim)
# ─────────────────────────────────────────────
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


# ─────────────────────────────────────────────
# İLAN MODELİ
# ─────────────────────────────────────────────
class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    # İlan satıldı mı? Satıcı onayladıktan sonra True olur
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────
# YORUM MODELİ
# ─────────────────────────────────────────────
class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.item.title}"


# ─────────────────────────────────────────────
# KONUŞMA MODELİ
# Bir alıcı ile satıcı arasındaki mesajlaşma kanalı.
# Her ilan için her alıcıya özel tek bir konuşma açılır.
# ─────────────────────────────────────────────
class Conversation(models.Model):
    # Bu konuşma hangi ilan hakkında?
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    # Mesajı başlatan alıcı
    buyer = models.ForeignKey(User, related_name='buying_conversations', on_delete=models.CASCADE)
    # İlanın sahibi (satıcı)
    seller = models.ForeignKey(User, related_name='selling_conversations', on_delete=models.CASCADE)
    # Konuşmanın oluşturulma tarihi
    created_at = models.DateTimeField(auto_now_add=True)
    # Son mesaj tarihi (konuşma listesini sıralarken kullanılır)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Aynı ilan için aynı alıcı-satıcı çifti sadece 1 konuşma açabilir
        unique_together = ('item', 'buyer', 'seller')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.buyer.username} ↔ {self.seller.username} | {self.item.title}"


# ─────────────────────────────────────────────
# MESAJ MODELİ
# Bir konuşma içindeki tek bir mesajı temsil eder.
# ─────────────────────────────────────────────
class Message(models.Model):
    # Hangi konuşmaya ait?
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    # Mesajı gönderen kullanıcı
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # Mesajın içeriği
    content = models.TextField()
    # Gönderilme zamanı
    sent_at = models.DateTimeField(auto_now_add=True)
    # Alıcı tarafından okundu mu?
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:40]}"
