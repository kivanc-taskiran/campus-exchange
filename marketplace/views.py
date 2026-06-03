from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Item, Category, Comment, Conversation, Message
from .forms import ItemForm, CommentForm
from django.db.models import Q


# ─────────────────────────────────────────────
# ANA SAYFA
# ─────────────────────────────────────────────
def index(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', 0)

    items = Item.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.all()

    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id and int(category_id) > 0:
        items = items.filter(category_id=category_id)

    context = {
        'items': items,
        'categories': categories,
        'query': query,
        'category_id': int(category_id)
    }
    return render(request, 'marketplace/index.html', context)


# ─────────────────────────────────────────────
# İLAN DETAY SAYFASI + YORUM
# ─────────────────────────────────────────────
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    comments = item.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = item
            comment.author = request.user
            comment.save()
            messages.success(request, 'Yorumun eklendi!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = CommentForm()

    # Kullanıcının bu ilan için mevcut konuşması var mı?
    existing_conversation = None
    if request.user.is_authenticated and request.user != item.owner:
        existing_conversation = Conversation.objects.filter(
            item=item, buyer=request.user
        ).first()

    return render(request, 'marketplace/item_detail.html', {
        'item': item,
        'comments': comments,
        'form': form,
        'existing_conversation': existing_conversation,
    })


# ─────────────────────────────────────────────
# İLAN OLUŞTURMA
# ─────────────────────────────────────────────
@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'İlanın oluşturuldu!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'marketplace/item_form.html', {'form': form, 'title': 'Yeni İlan Ekle'})


# ─────────────────────────────────────────────
# İLAN DÜZENLEME
# ─────────────────────────────────────────────
@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'İlan güncellendi!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'marketplace/item_form.html', {'form': form, 'title': 'İlanı Düzenle'})


# ─────────────────────────────────────────────
# İLAN SİLME
# ─────────────────────────────────────────────
@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'İlan silindi!')
        return redirect('index')
    return render(request, 'marketplace/item_confirm_delete.html', {'item': item})


# ─────────────────────────────────────────────
# İLANI SATILDI OLARAK İŞARETLE
# Sadece satıcı yapabilir; nakit ödeme yüz yüze alındıktan sonra tıklanır
# ─────────────────────────────────────────────
@login_required
def item_mark_sold(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.is_sold = True
        item.is_active = False
        item.save()
        messages.success(request, f'"{item.title}" satıldı olarak işaretlendi!')
    return redirect('item_detail', pk=item.pk)


# ─────────────────────────────────────────────
# MESAJLAŞMA BAŞLAT
# Alıcı "Message Seller" butonuna bastığında konuşmayı oluşturur/açar
# ─────────────────────────────────────────────
@login_required
def start_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # Kendi ilanına mesaj gönderemez
    if request.user == item.owner:
        messages.warning(request, 'Kendi ilanına mesaj gönderemezsin.')
        return redirect('item_detail', pk=item_pk)

    # Mevcut konuşma varsa onu aç, yoksa yeni oluştur
    conversation, created = Conversation.objects.get_or_create(
        item=item,
        buyer=request.user,
        seller=item.owner,
    )
    return redirect('conversation_detail', pk=conversation.pk)


# ─────────────────────────────────────────────
# GELEN KUTUSU (INBOX)
# Kullanıcının tüm konuşmalarını listeler
# ─────────────────────────────────────────────
@login_required
def inbox(request):
    # Kullanıcının alıcı veya satıcı olduğu tüm konuşmalar
    conversations = Conversation.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).order_by('-updated_at')

    # Okunmamış mesaj sayısı (toplam)
    unread_count = Message.objects.filter(
        conversation__in=conversations,
        is_read=False
    ).exclude(sender=request.user).count()

    return render(request, 'marketplace/inbox.html', {
        'conversations': conversations,
        'unread_count': unread_count,
    })


# ─────────────────────────────────────────────
# KONUŞMA DETAYI
# Mesajları gösterir ve yeni mesaj göndermeye izin verir
# ─────────────────────────────────────────────
@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)

    # Sadece konuşmaya dahil olanlar görebilir
    if request.user not in [conversation.buyer, conversation.seller]:
        messages.error(request, 'Bu konuşmaya erişim izniniz yok.')
        return redirect('inbox')

    # Karşı tarafın mesajlarını okundu olarak işaretle
    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
            )
            # updated_at güncellenir (inbox sıralaması için)
            conversation.save()
            return redirect('conversation_detail', pk=pk)

    msgs = conversation.messages.all()
    return render(request, 'marketplace/conversation_detail.html', {
        'conversation': conversation,
        'msgs': msgs,
    })


# ─────────────────────────────────────────────
# KULLANICI KAYIT
# ─────────────────────────────────────────────
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Kayıt başarılı, hoş geldin!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
