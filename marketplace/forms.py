# Django'nun form modülü
from django import forms
# Formlarda kullanacağımız modeller
from .models import Item, Comment


# ─────────────────────────────────────────────
# İLAN FORMU
# Kullanıcının ilan oluşturma/düzenleme ekranında dolduracağı form
# ModelForm → modelden otomatik alan üretir, doğrudan veritabanına kaydeder
# ─────────────────────────────────────────────
class ItemForm(forms.ModelForm):
    class Meta:
        # Bu form Item modelini temel alır
        model = Item
        # Kullanıcıya gösterilecek alanlar (owner ve created_at gibi alanlar hariç)
        fields = ['title', 'category', 'description', 'price', 'image']
        widgets = {
            # Açıklama alanını 4 satırlı büyük bir metin kutusu yap
            'description': forms.Textarea(attrs={'rows': 4}),
        }


# ─────────────────────────────────────────────
# YORUM FORMU
# İlan detay sayfasında yorum göndermek için kullanılır
# ─────────────────────────────────────────────
class CommentForm(forms.ModelForm):
    class Meta:
        # Bu form Comment modelini temel alır
        model = Comment
        # Kullanıcıdan sadece yorum içeriği istenir (item ve author view'da set edilir)
        fields = ['content']
        widgets = {
            # Yorum kutusunu 3 satırlı yap ve placeholder ekle
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask a question or comment...'}),
        }
