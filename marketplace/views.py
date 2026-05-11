from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Category, Comment
from .forms import ItemForm, CommentForm
from django.db.models import Q

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
            messages.success(request, 'Your comment has been added.')
            return redirect('item_detail', pk=item.pk)
    else:
        form = CommentForm()

    return render(request, 'marketplace/item_detail.html', {
        'item': item,
        'comments': comments,
        'form': form
    })

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Item successfully created!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'marketplace/item_form.html', {'form': form, 'title': 'Create New Item'})

@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item successfully updated!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'marketplace/item_form.html', {'form': form, 'title': 'Edit Item'})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item successfully deleted!')
        return redirect('index')
    return render(request, 'marketplace/item_confirm_delete.html', {'item': item})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
