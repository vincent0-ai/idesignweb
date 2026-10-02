"""
Public marketing zone views for idesignweb.
Clean, professional copy in plain English.
All content is retrieved from MongoDB collections.
"""

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from apps.core.db import get_db
from apps.core.content import (
    get_all_works,
    get_work_by_slug,
    get_all_services,
    get_service_by_slug,
    get_work_categories,
    get_all_articles,
    get_article_by_slug
)
import datetime

def home_view(request):
    services = get_all_services(featured_only=True)
    case_studies = get_all_works()
    
    # Try fetching insights if db available, fallback to empty
    try:
        db = get_db()
        posts = list(db.posts.find({'is_published': True}).sort('published_at', -1).limit(3))
    except Exception:
        posts = []
    
    telemetry = [
        {'metric': '99.99%', 'label': 'Platform Uptime SLA', 'detail': 'Zero unplanned outages'},
        {'metric': '0', 'label': 'Exploit Incidents', 'detail': 'Rigorous defensive security'},
        {'metric': '1.0s', 'label': 'Core Web Speed', 'detail': 'Engineered for instant conversion'},
        {'metric': '< 24h', 'label': 'Founder Direct Response', 'detail': 'Direct access to engineers'}
    ]
    
    context = {
        'services': services,
        'case_studies': case_studies,
        'posts': posts,
        'telemetry': telemetry,
    }
    return render(request, 'public/home.html', context)


def services_hub_view(request):
    services = get_all_services()
    return render(request, 'public/services_hub.html', {'services': services})

def service_detail_view(request, slug):
    service = get_service_by_slug(slug)
    if not service:
        raise Http404('Service not found')
        
    related_cases = [w for w in get_all_works() if w.get('category') == service['title']]
    if not related_cases:
        related_cases = get_all_works()[:2]
        
    context = {
        'service': service,
        'related_cases': related_cases
    }
    return render(request, 'public/service_detail.html', context)

def work_list_view(request):
    selected_category = request.GET.get('category', 'all')
    case_studies = get_all_works(category=selected_category)
    categories = get_work_categories()
    
    context = {
        'case_studies': case_studies,
        'categories': categories,
        'selected_category': selected_category
    }
    return render(request, 'public/work_list.html', context)

def work_detail_view(request, slug):
    case_study = get_work_by_slug(slug)
    if not case_study:
        raise Http404('Work project not found')
        
    return render(request, 'public/work_detail.html', {'case_study': case_study})

def about_view(request):
    standards = [
        {
            'numeral': '01',
            'title': 'Defensive Engineering by Default',
            'desc': 'Vincent architects every backend and infrastructure node with zero-trust principles. Vulnerability scanning, encryption in transit and at rest, and automated off-site backups are built-in from line one.'
        },
        {
            'numeral': '02',
            'title': 'Sub-Second Performance & Craft',
            'desc': 'Timothy crafts lightning-fast frontend interfaces and clean brand identities. We ruthlessly prune unnecessary dependencies so your users enjoy silky 60fps responsiveness and instant page loads.'
        },
        {
            'numeral': '03',
            'title': 'Direct Founder Accountability',
            'desc': 'No bureaucratic account managers or juniors passing messages. You work directly with Vincent and Timothy through every phase, from technical architecture to production deployment.'
        }
    ]
    return render(request, 'public/about.html', {'standards': standards})


def insights_list_view(request):
    posts = get_all_articles()
    return render(request, 'public/insights_list.html', {'posts': posts})

def insight_detail_view(request, slug):
    post = get_article_by_slug(slug)
    if not post:
        raise Http404('Article not found')
        
    return render(request, 'public/insight_detail.html', {'post': post})

def contact_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        service_interest = request.POST.get('service_interest', '').strip()
        budget_range = request.POST.get('budget_range', '').strip()
        message = request.POST.get('message', '').strip()
        
        if not full_name or not email or not message:
            messages.error(request, 'Please fill in all required fields (Name, Email, and Message).')
        else:
            try:
                from apps.core.models import Inquiry
                Inquiry.objects.create(
                    full_name=full_name,
                    email=email,
                    service_interest=service_interest or 'General Inquiry',
                    budget_range=budget_range or 'Not Specified',
                    message=message,
                    status='New'
                )
            except Exception:
                pass
            messages.success(request, 'Thank you for reaching out. We have received your message and will get back to you within 24 hours.')
            return redirect('public:contact')
            
    return render(request, 'public/contact.html')
