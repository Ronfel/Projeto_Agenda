from typing import Any, Dict

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from contact.forms import CategoryForm
from contact.models import Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def category_create(request):
    form_action = reverse('category_create')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        context = {
         'form': form,
         'site_title': 'New Category - ',
         'form_action': form_action

        }
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
            messages.info(request, "Categoria criada com sucesso")
            return redirect('index')

        return render(
            request,
            'contact/category_create.html',
            context=context)
    

    context = {
        'form': CategoryForm(),
        'site_title': 'New Category - ',
        'form_action': form_action

    }
    return render(
        request,
        'contact/category_create.html',
        context=context)

@login_required(login_url='login')
def category_update(request, category_id):
    if request.user.is_superuser:
        category = get_object_or_404(Category, pk=category_id, show=True)
    else:
        category = get_object_or_404(Category, pk=category_id, show=True, owner=request.user)
    form_action = reverse('category_update', args=(category_id,))
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        context = {
         'form': form,
         'site_title': 'Edit Category - ',
         'form_action': form_action

        }
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.info(request, "Categoria editada com sucesso")
            return redirect('index')

        return render(
            request,
            'contact/category_create.html',
            context=context)
    

    context = {
        'form': CategoryForm(instance=category),
        'site_title': 'Edit Category - ',
        'form_action': form_action

    }
    return render(
        request,
        'contact/category_create.html',
        context=context)

@login_required(login_url='login')
def category_delete(request, category_id):
    if request.user.is_superuser:
        category = get_object_or_404(Category, pk=category_id, show=True)
    else:
        category = get_object_or_404(Category, pk=category_id, show=True, owner=request.user)

    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        category.delete()
        return redirect('index')

    return render(
        request,
        'contact/category.html',
        {
            'category': category,
            'confirmation': confirmation,
        }
    )