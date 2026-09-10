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
    case_studies = list(db.case_studies.find({'is_published': True}).sort('published_at', -1).limit(2))
    posts = list(db.posts.find({'is_published': True}).sort('published_at', -1).limit(3))
    
    stats = [
        {'metric': '100+', 'label': 'Completed Client Projects'},
        {'metric': '99.9%', 'label': 'Website Uptime Guarantee'},
        {'metric': '24h', 'label': 'Support Response Time'}
    ]
    
    process_steps = [
        {
            'step_number': '01',
            'title': 'Discovery and Planning',
            'description': 'We discuss your business goals, target audience, and project requirements to create a clear, realistic plan.'
        },
        {
            'step_number': '02',
            'title': 'Design and Development',
            'description': 'We craft your brand visuals, video edits, website, or security safeguards with regular check-ins along the way.'
        },
        {
            'step_number': '03',
            'title': 'Launch and Support',
            'description': 'We deliver all final files or launch your website, providing ongoing support whenever you need help.'
        }
    ]
    
    context = {
        'services': services,
        'case_studies': case_studies,
        'posts': posts,
        'stats': stats,
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
            'title': 'Clarity and Focus',
            'desc': 'We keep things simple and easy to understand. Clean typography and clear layouts help your customers find what they need quickly.'
        },
        {
            'numeral': '02',
            'title': 'Speed and Quality',
            'desc': 'Fast-loading websites, high-definition videos, and prompt responses to your questions. We build things right the first time.'
        },
        {
            'numeral': '03',
            'title': 'Reliable Protection',
            'desc': 'Security is built into our websites from the start, protecting your business and customer information against online threats.'
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
