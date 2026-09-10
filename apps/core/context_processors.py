"""
Global template context processors for idesignweb.
Provides company information, navigation items, and design system variables.
"""

import datetime

def global_context(request):
    return {
        'site_title': 'idesignweb',
        'site_tagline': 'Digital Solutions Architecture',
        'current_year': datetime.datetime.now().year,
        'main_nav_items': [
            {'label': 'Services', 'url_name': 'public:services_hub', 'numeral': '01'},
            {'label': 'Work', 'url_name': 'public:work_list', 'numeral': '02'},
            {'label': 'About', 'url_name': 'public:about', 'numeral': '03'},
            {'label': 'Insights', 'url_name': 'public:insights_list', 'numeral': '04'},
            {'label': 'Contact', 'url_name': 'public:contact', 'numeral': '05'},
        ],
        'service_links': [
            {'title': 'Graphic Design', 'slug': 'graphic-design', 'num': '01'},
            {'title': 'Video Editing', 'slug': 'video-editing', 'num': '02'},
            {'title': 'Web Development', 'slug': 'web-development', 'num': '03'},
            {'title': 'Cybersecurity', 'slug': 'cybersecurity', 'num': '04'},
        ]
    }
