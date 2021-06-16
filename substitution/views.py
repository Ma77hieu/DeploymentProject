from django.shortcuts import render

from .services import Services


def results(request):
    """View managing the product search"""
    results = Services().search_a_prod(request)
    return render(request, results[0], results[1])


def details(request, product_id):
    """View managing the product detail page"""
    details = Services().details(request, product_id)
    return render(request, details[0], details[1])


def mesaliments(request):
    """view managing the access to a user's saved favorites alternatives"""
    favs = Services().mesaliments(request)
    return render(request, favs[0], favs[1])
