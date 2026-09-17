from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from contact.models import Contact
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):

    if request.user.is_superuser:
        contacts = Contact.objects\
                .all()\
                .filter(show=True)
    else:
        contacts = Contact.objects\
                .all()\
                .filter(show=True)\
                .filter(owner=request.user)
        
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - '
    }

    return render(
        request,
        'contact/index.html',
        context=context)

@login_required(login_url='login')
def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('index')
    if request.user.is_superuser:
        contacts = Contact.objects\
                .all()\
                .filter(show=True)\
                .filter(Q(first_name__icontains=search_value) |
                        Q(last_name__icontains =search_value))
    else:
        contacts = Contact.objects\
                .all()\
                .filter(show=True)\
                .filter(owner=request.user)\
                .filter(Q(first_name__icontains=search_value) |
                        Q(last_name__icontains =search_value))

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Search - ',
        'search_value': search_value
    }

    return render(
        request,
        'contact/index.html',
        context=context)

@login_required(login_url='login')
def contact(request, contact_id):
    single_contact = get_object_or_404(
        Contact, pk=contact_id, show=True)
    site_title = f'{single_contact.first_name} {single_contact.last_name} - '

    context = {
        'contact': single_contact,
        'site_title': site_title
    }

    return render(
        request,
        'contact/contact.html',
        context=context)

