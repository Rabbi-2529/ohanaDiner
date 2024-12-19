from django.shortcuts import render
from .models import *
from django.db.models import Min
from django.db.models import Prefetch
from django.utils.text import slugify





def home(request):
    categories = Category.objects.all().prefetch_related('galleries')

    context = {
        'categories': categories
    }

    return render(request, 'frontend/index.html', context)


def menu_items(request, company_slug, company_id):
    company = Company.objects.filter(id=company_id).first()
    company.slug_name = slugify(company.name)

    menu_items = MenuItem.objects.filter(company=company)
    hot_deal_menu_items = menu_items.filter(hot_deal_status=True)

    # categories = Category.objects.all()
    # categories = Category.objects.prefetch_related('menu_items')

    # Filter menu items for the specific company
    menu_items_query = MenuItem.objects.filter(company_id=company_id)

    # Prefetch the filtered menu items for each category
    categories = Category.objects.prefetch_related(
        Prefetch('menu_items', queryset=menu_items_query)
    )

    if hot_deal_menu_items.exists():
        for hot_deal_menu_item in hot_deal_menu_items:
            hot_deal_menu_item.slug_name = slugify(hot_deal_menu_item.name)

    if menu_items.exists():
        for menu_item in menu_items:
            menu_item.slug_name = slugify(menu_item.name)

    for category in categories:
        for categoy_menu_item in category.menu_items.all():
            categoy_menu_item.slug_name = slugify(categoy_menu_item.name)

    for category in categories:
        for categoy_menu_item in category.menu_items.all():
            print('category menu_item with slug name: ', categoy_menu_item.slug_name)

    print('menu_items: ', menu_items)
    print('hot_deal_menu_items: ', hot_deal_menu_items)

    context = {
        'company': company,
        'categories': categories,
        'menu_items': menu_items,
        'hot_deal_menu_items': hot_deal_menu_items,
    }
    
    return render(request, 'frontend/menu_items.html', context)


def menu_single(request, menu_slug, company_id, menu_id):
    company = Company.objects.filter(id=company_id).first()
    menu_item = MenuItem.objects.filter(id=menu_id, company=company).first()
    menu_item.slug_name = slugify(menu_item.name)

    # categories = Category.objects.all()
    if menu_item:
        category = menu_item.category

    context = {
        'company': company,
        'category': category,
        'menu_item': menu_item
    }
    
    return render(request, 'frontend/menu_single.html', context)


def about(request):
    about_us = AboutUs.objects.all()
    company_profiles = CompanyProfile.objects.all()
    # owners = Owner.objects.all()
    # Get unique owners based on email
    unique_owners = (
        Owner.objects.values('email')
        .annotate(min_id=Min('id'))
        .order_by('email')
    )
    
    # Fetch the full owner objects using the IDs of the unique emails
    owners = Owner.objects.filter(id__in=[owner['min_id'] for owner in unique_owners])

    print('about_us section: ', about_us)

    context = {
        'about_us': about_us,
        'company_profiles': company_profiles,
        'owners': owners,
    }

    return render(request, 'frontend/about.html', context)


def contact(request):
   
    contacts = ContactUs.objects.select_related('company').all()
    return render(request, 'frontend/contact.html', {'contacts': contacts})
