from typing import Any, Dict

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from contact.forms import ContactForm
from contact.models import Contact
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def create(request):
    form_action = reverse('create')
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        context = {
         'form': form,
         'site_title': 'New Contact - ',
         'form_action': form_action

        }
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            messages.info(request, "Contato criado com sucesso")
            return redirect('index')

        return render(
            request,
            'contact/create.html',
            context=context)
    

    context = {
        'form': ContactForm(),
        'site_title': 'New Contact - ',
        'form_action': form_action

    }
    return render(
        request,
        'contact/create.html',
        context=context)

@login_required(login_url='login')
def update(request, contact_id):
    if request.user.is_superuser:
        contact = get_object_or_404(Contact, pk=contact_id, show=True)
    else:
        contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
    form_action = reverse('update', args=(contact_id,))
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        context = {
         'form': form,
         'site_title': 'Edit Contact - ',
         'form_action': form_action

        }
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            messages.info(request, "Contato editado com sucesso")
            return redirect('index')

        return render(
            request,
            'contact/create.html',
            context=context)
    

    context = {
        'form': ContactForm(instance=contact),
        'site_title': 'Edit Contact - ',
        'form_action': form_action

    }
    return render(
        request,
        'contact/create.html',
        context=context)

@login_required(login_url='login')
def delete(request, contact_id):
    if request.user.is_superuser:
        contact = get_object_or_404(Contact, pk=contact_id, show=True)
    else:
        contact = get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)

    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('index')

    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )