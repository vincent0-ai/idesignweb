"""
Public marketing zone views for idesignweb.
Clean, professional copy in plain English.
All content is retrieved from MongoDB collections.
"""

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from apps.core.db import get_db
import datetime

def home_view(request):
    db = get_db()
    services = list(db.services.find({'featured': True}).sort('sort_order', 1))
    case_studies = list(db.case_studies.find({'is_published': True}).sort('published_at', -1).limit(4))
    posts = list(db.posts.find({'is_published': True}).sort('published_at', -1).limit(3))
    
    telemetry = [
        {'metric': '99.99%', 'label': 'Platform Uptime SLA', 'detail': 'Zero unplanned outages'},
        {'metric': '0', 'label': 'Exploit Incidents', 'detail': 'Rigorous defensive security'},
        {'metric': '1.1s', 'label': 'Core Web Speed', 'detail': 'Engineered for instant conversion'},
        {'metric': '< 24h', 'label': 'Founder Direct Response', 'detail': 'Direct access to engineers'}
    ]
    
    process_steps = [
        {
            'step_number': '01',
            'title': 'Architecture & Threat Surface Audit',
            'description': 'We dissect your brand goals, target customers, and operational bottlenecks. We map out full-stack specs and security safeguards before writing a single line of code.'
        },
        {
            'step_number': '02',
            'title': 'High-Performance Engineering & Design',
            'description': 'Vincent implements secure backend pipelines, database schemes, and penetration-tested code while Timothy designs fluid interfaces, brand identities, and motion media.'
        },
        {
            'step_number': '03',
            'title': 'Hardened Deployment & Ongoing Defense',
            'description': 'We push to production with automated off-site backups, SSL/TLS certificates, web application firewalls, and active monitoring to ensure your business stays protected 24/7.'
        }
    ]
    
    context = {
        'services': services,
        'case_studies': case_studies,
        'posts': posts,
        'telemetry': telemetry,
        'process_steps': process_steps,
    }
    return render(request, 'public/home.html', context)


def services_hub_view(request):
    db = get_db()
    services = list(db.services.find({}).sort('sort_order', 1))
    return render(request, 'public/services_hub.html', {'services': services})

def service_detail_view(request, slug):
    db = get_db()
    service = db.services.find_one({'slug': slug})
    if not service:
        raise Http404('Service not found')
        
    related_cases = list(db.case_studies.find({'category': service['title']}).limit(2))
    context = {
        'service': service,
        'related_cases': related_cases
    }
    return render(request, 'public/service_detail.html', context)

def work_list_view(request):
    db = get_db()
    selected_category = request.GET.get('category', 'all')
    query = {'is_published': True}
    if selected_category != 'all':
        query['category'] = selected_category
        
    case_studies = list(db.case_studies.find(query).sort('published_at', -1))
    categories = ['Graphic Design', 'Video Editing', 'Web Development', 'Cybersecurity']
    
    context = {
        'case_studies': case_studies,
        'categories': categories,
        'selected_category': selected_category
    }
    return render(request, 'public/work_list.html', context)

def work_detail_view(request, slug):
    db = get_db()
    case_study = db.case_studies.find_one({'slug': slug, 'is_published': True})
    if not case_study:
        raise Http404('Case study not found')
        
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
    db = get_db()
    posts = list(db.posts.find({'is_published': True}).sort('published_at', -1))
    return render(request, 'public/insights_list.html', {'posts': posts})

def insight_detail_view(request, slug):
    db = get_db()
    post = db.posts.find_one({'slug': slug, 'is_published': True})
    if not post:
        raise Http404('Article not found')
        
    return render(request, 'public/insight_detail.html', {'post': post})

def contact_view(request):
    db = get_db()
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        service_interest = request.POST.get('service_interest', '').strip()
        budget_range = request.POST.get('budget_range', '').strip()
        message = request.POST.get('message', '').strip()
        
        if not full_name or not email or not message:
            messages.error(request, 'Please fill in all required fields (Name, Email, and Message).')
        else:
            inquiry_doc = {
                'full_name': full_name,
                'email': email,
                'service_interest': service_interest or 'General Inquiry',
                'budget_range': budget_range or 'Not Specified',
                'message': message,
                'status': 'New',
                'submitted_at': datetime.datetime.now(datetime.timezone.utc)
            }
            db.inquiries.insert_one(inquiry_doc)
            messages.success(request, 'Thank you for reaching out. We have received your message and will get back to you within 24 hours.')
            return redirect('public:contact')
            
    return render(request, 'public/contact.html')
