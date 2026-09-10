"""
Public marketing zone views for idesignweb.
Renders home, services hub, service details, case studies, about, insights, and contact form.
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
        {'metric': '99.9%', 'label': 'System Reliability and Defense SLA'},
        {'metric': '100+', 'label': 'Production Deliverables Deployed'},
        {'metric': '18ms', 'label': 'Median Server Response Latency'}
    ]
    
    process_steps = [
        {
            'step_number': '01',
            'title': 'Reconnaissance and Systems Audit',
            'description': 'We evaluate your category landscape, existing codebase architecture, and security attack surfaces before writing code or drafting design systems.'
        },
        {
            'step_number': '02',
            'title': 'Disciplined Engineering and Assembly',
            'description': 'Building accessible semantic interfaces, motion typography sequences, and hardened cloud services using strict hairline design standards.'
        },
        {
            'step_number': '03',
            'title': 'Verification and Continuous Defense',
            'description': 'Every release passes rigorous latency benchmarks, automated test suites, and ongoing threat monitoring in dedicated client project spaces.'
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
        raise Http404('Service practice not found')
        
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
            'title': 'Zero Visual Noise',
            'desc': 'No gradients, no decorative shadows, and no generic emoji. We communicate strictly through typographic scale, weights, and hairline boundaries.'
        },
        {
            'numeral': '02',
            'title': 'Engineered Performance',
            'desc': 'Every digital deliverable is optimized for sub-50ms execution, accessibility compliance, and low resource overhead.'
        },
        {
            'numeral': '03',
            'title': 'Integrated Defense',
            'desc': 'Design and code are treated with the same rigor as infrastructure security. Vulnerability management is embedded in our workflow.'
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
        raise Http404('Insight article not found')
        
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
            messages.error(request, 'Please complete all required fields (Name, Email, and Message).')
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
            messages.success(request, 'Inquiry successfully registered. Our technical team will review your specifications within 24 hours.')
            return redirect('public:contact')
            
    return render(request, 'public/contact.html')
