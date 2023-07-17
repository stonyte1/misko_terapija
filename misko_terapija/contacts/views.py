from django.shortcuts import render


def contacts(requests):
    return render(requests, 'contacts/contacts.html', {'contact': 'contact'})
