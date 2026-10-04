"""
Global template context processors for idesignweb.
Provides company information, contact details, navigation, and service links.
"""

import datetime

def global_context(request):
    try:
        base_url = request.build_absolute_uri('/')[:-1]
        canonical_url = request.build_absolute_uri(request.path)
        default_og_image = request.build_absolute_uri('/static/img/og-image.jpg')
        site_logo_url = request.build_absolute_uri('/static/img/logo.jpg')
    except Exception:
        base_url = 'https://idesignweb.co.ke'
        canonical_url = 'https://idesignweb.co.ke/'
        default_og_image = 'https://idesignweb.co.ke/static/img/og-image.jpg'
        site_logo_url = 'https://idesignweb.co.ke/static/img/logo.jpg'

    return {
        'site_title': 'Idesignweb',
        'site_tagline': 'High-Performance Web Engineering & Cybersecurity',
        'site_domain': 'idesignweb.co.ke',
        'site_base_url': base_url,
        'site_logo_url': site_logo_url,
        'canonical_url': canonical_url,
        'default_meta_title': 'Idesignweb : Web Development, Cybersecurity & Design Studio',
        'default_meta_description': 'Idesignweb builds high-performing web applications, e-commerce stores, bulletproof cybersecurity defense, and distinctive brand systems. Founded by Timothy Owino with co-founder Vincent Odhiambo. Nairobi, Kenya & Global.',
        'default_meta_keywords': 'web development Nairobi, web design Kenya, cybersecurity audits, e-commerce development, full stack engineering, Timothy Owino, Vincent Odhiambo, brand identity design',
        'default_og_image': default_og_image,
        'geo_region': 'KE',
        'geo_placename': 'Nairobi',
        'founder_name': 'Timothy Owino & Vincent Odhiambo',
        'founder_title': 'Leadership',
        'founders': [
            {
                'name': 'Timothy Owino',
                'title_badge': 'FOUNDER',
                'role': 'Founder, Creative Director & Full-Stack Developer',
                'short_role': 'Creative Direction & Full-Stack Development',
                'bio': 'Founder of Idesignweb. Passionate about seamless user experiences, responsive frontend engineering, brand identity systems, and commercial video storytelling. Timothy turns strategic business vision into intuitive, visually unforgettable digital products.',
                'skills': ['Full-Stack Development', 'UI/UX Interface Design', 'Brand Identity Systems', 'Commercial Video Editing', 'SEO & Performance'],
                'phone': '+254115709680',
                'email': 'otienotimothy198@gmail.com',
            },
            {
                'name': 'Vincent Odhiambo',
                'title_badge': 'CO-FOUNDER',
                'role': 'Co-Founder, Lead Software Engineer & Cybersecurity Analyst',
                'short_role': 'Software Engineering & Cybersecurity',
                'bio': 'Co-Founder of Idesignweb. Specializing in backend system architectures, web application development, penetration testing, and security hardening. Vincent ensures every platform is resilient against vulnerabilities, scalable, and built on rock-solid foundations.',
                'skills': ['Web Systems Programming', 'Cybersecurity & Audits', 'Infrastructure Hardening', 'Database Architecture', 'Penetration Testing'],
                'phone': '+254768072566',
                'email': 'vinnyochi13249@gmail.com',
            }
        ],
        'company_phone': '+254115709680',
        'company_email': 'otienotimothy198@gmail.com',
        'company_location': 'Nairobi, Kenya / Remote Globally',
        'current_year': datetime.datetime.now().year,
        'main_nav_items': [
            {'label': 'Capabilities', 'url_name': 'public:services_hub', 'numeral': '01'},
            {'label': 'Work', 'url_name': 'public:work_list', 'numeral': '02'},
            {'label': 'Founders & About', 'url_name': 'public:about', 'numeral': '03'},
            {'label': 'Insights', 'url_name': 'public:insights_list', 'numeral': '04'},
            {'label': 'Contact', 'url_name': 'public:contact', 'numeral': '05'},
        ],
        'service_links': [
            {'title': 'Web Development', 'slug': 'web-development', 'num': '01'},
            {'title': 'Cybersecurity', 'slug': 'cybersecurity', 'num': '02'},
            {'title': 'Graphic Design', 'slug': 'graphic-design', 'num': '03'},
            {'title': 'Video Editing', 'slug': 'video-editing', 'num': '04'},
        ]
    }
