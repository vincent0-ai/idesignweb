"""
Global template context processors for idesignweb.
Provides company information, contact details, navigation, and service links.
"""

import datetime

def global_context(request):
    return {
        'site_title': 'Idesignweb',
        'site_tagline': 'We Build Websites That Grow Your Business',
        'founder_name': 'Timothy Owino',
        'founder_title': 'Technician and Lead Developer',
        'company_phone': '0115709680',
        'company_email': 'otienotimothy198@gmail.com',
        'company_location': 'Remote (We work with you, from anywhere)',
        'current_year': datetime.datetime.now().year,
        'main_nav_items': [
            {'label': 'Services', 'url_name': 'public:services_hub', 'numeral': '01'},
            {'label': 'Work', 'url_name': 'public:work_list', 'numeral': '02'},
            {'label': 'About', 'url_name': 'public:about', 'numeral': '03'},
            {'label': 'Insights', 'url_name': 'public:insights_list', 'numeral': '04'},
            {'label': 'Contact', 'url_name': 'public:contact', 'numeral': '05'},
        ],
        'service_links': [
            {'title': 'Web Development', 'slug': 'web-development', 'num': '01'},
            {'title': 'Graphic Design', 'slug': 'graphic-design', 'num': '02'},
            {'title': 'Video Editing', 'slug': 'video-editing', 'num': '03'},
            {'title': 'Cybersecurity', 'slug': 'cybersecurity', 'num': '04'},
        ]
    }
