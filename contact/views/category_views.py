from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from contact.models import Contact, Category
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def categories(request):

    categories = Category.objects\
                .all()
        
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Categorias - '
    }

    return render(
        request,
        'contact/categories.html',
        context=context)

@login_required(login_url='login')
def category(request, category_id):
    single_category = get_object_or_404(
        Category, pk=category_id)
    site_title = f'{single_category.name} - '

    context = {
        'category': single_category,
        'site_title': site_title
    }

    return render(
        request,
        'contact/category.html',
        context=context)