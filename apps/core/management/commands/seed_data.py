"""
Management command to seed MongoDB and SQLite for Idesignweb.
Content adapted from company brand materials and Squarespace inspired architecture.
Zero emoji, zero em dashes, and complete flat design consistency.
Safe, idempotent upserts: does not wipe production customer data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.db import get_db, init_indexes
from apps.core.models import Work, Article
import datetime
import os

class Command(BaseCommand):
    help = 'Seeds services, case studies, articles, and optionally demo portal spaces'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean-demo',
            action='store_true',
            help='Purges dummy demo client portal records (client_apex, demo projects, tickets, assets)'
        )

    def handle(self, *args, **options):
        # 0. Superuser Account Initialization (Configurable via Environment)
        admin_pass = os.getenv('DJANGO_SUPERUSER_PASSWORD') or os.getenv('ADMIN_PASSWORD')
        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME') or os.getenv('ADMIN_USERNAME')
        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL') or os.getenv('ADMIN_EMAIL') or 'admin@idesignweb.co.ke'
        
        # Sanitize email in case domain is missing (e.g. admin@idesignweb -> admin@idesignweb.co.ke)
        if not admin_email or '@' not in admin_email or '.' not in admin_email.split('@')[-1]:
            admin_email = f"{admin_email.split('@')[0]}@idesignweb.co.ke"

        if admin_pass and admin_username:
            self.stdout.write(f'Configuring administrator account from environment: {admin_username}...')
            admin_user = User.objects.filter(username=admin_username).first()
            if not admin_user:
                admin_user = User.objects.create_user(
                    username=admin_username,
                    email=admin_email,
                    password=admin_pass
                )
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.save()
                self.stdout.write(self.style.SUCCESS(f'Created superuser from env: {admin_username} ({admin_email})'))
            else:
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.email = admin_email
                admin_user.set_password(admin_pass)
                admin_user.save()
                self.stdout.write(self.style.SUCCESS(f'Updated administrator credentials from env: {admin_username}'))
        else:
            self.stdout.write('No DJANGO_SUPERUSER_PASSWORD / USERNAME set in environment. Skipping administrator creation.')

        self.stdout.write('Initializing indexes...')
        init_indexes()
        
        db = get_db()
        now = datetime.datetime.now(datetime.timezone.utc)
        clean_demo = options.get('clean_demo', False)

        # Optional Clean Demo Data
        if clean_demo:
            self.stdout.write('Purging demo client portal records...')
            User.objects.filter(username='client_apex').delete()
            db.projects.delete_many({'client_username': 'client_apex'})
            db.assets.delete_many({'client_username': 'client_apex'})
            db.tickets.delete_many({'client_username': 'client_apex'})
            db.announcements.delete_many({
                'title': {
                    '$in': [
                        'Scheduled Routine Server Maintenance This Sunday',
                        'High Resolution File Downloads Available in Asset Library'
                    ]
                }
            })
            self.stdout.write(self.style.SUCCESS('Purged demo client records.'))

        # 1. Seed Core Public Services (Idempotent upsert)
        self.stdout.write('Ensuring public services catalog...')
        services_data = [
            {
                'slug': 'web-development',
                'service_number': '01',
                'title': 'Web Development',
                'tagline': 'Smart websites, online stores, and customer portals that grow your business.',
                'overview': 'We build high-performing, mobile-friendly websites that help you attract customers, build trust, and increase sales. From custom business landing pages to full e-commerce stores with secure payment processing, every site is fast, modern, and search engine optimized.',
                'deliverables': [
                    'Custom website design tailored to your brand',
                    'Mobile-responsive development looking perfect on all screens',
                    'E-commerce stores with secure payment integrations',
                    'Website management, content updates, and routine backups',
                    'Search engine optimization (SEO) and speed tuning'
                ],
                'featured': True,
                'sort_order': 1,
                'updated_at': now
            },
            {
                'slug': 'graphic-design',
                'service_number': '02',
                'title': 'Graphic Design',
                'tagline': 'Brand identity, logos, poster design, and print marketing collateral.',
                'overview': 'A strong visual identity sets your business apart from competitors. We design unique logos, brand style guides, promotional posters, business cards, and digital marketing graphics that build immediate credibility with your audience.',
                'deliverables': [
                    'Unique logo design and complete brand guidelines',
                    'Promotional posters, flyers, and event graphics',
                    'Business cards and print-ready stationery',
                    'Social media banners and advertising graphics'
                ],
                'featured': True,
                'sort_order': 2,
                'updated_at': now
            },
            {
                'slug': 'video-editing',
                'service_number': '03',
                'title': 'Video Editing',
                'tagline': 'Commercials, social media videos, YouTube content, and motion titles.',
                'overview': 'Engage your audience with professional video content. We transform raw footage into compelling stories with sharp cuts, clean audio balancing, animated title cards, and color grading tailored for web and social platforms.',
                'deliverables': [
                    'Promotional business videos and commercial edits',
                    'Social media clips formatted for Instagram, TikTok, and YouTube',
                    'Motion graphics and animated text overlays',
                    'Audio cleanup, background music mixing, and color grading'
                ],
                'featured': True,
                'sort_order': 3,
                'updated_at': now
            },
            {
                'slug': 'cybersecurity',
                'service_number': '04',
                'title': 'Cybersecurity',
                'tagline': 'Website security checks, malware defense, server hardening, and backups.',
                'overview': 'Keep your website, customer data, and online reputation safe from cyber attacks. We conduct vulnerability reviews, fix security loopholes, set up automated backups, and protect your server against unauthorized access.',
                'deliverables': [
                    'Website security audits and vulnerability checks',
                    'Malware scanning and rapid cleanup',
                    'SSL configuration, firewall setup, and server hardening',
                    'Automated regular backups and continuous uptime monitoring'
                ],
                'featured': True,
                'sort_order': 4,
                'updated_at': now
            }
        ]
        for s in services_data:
            db.services.update_one({'slug': s['slug']}, {'$set': s}, upsert=True)

        # 2. Seed Work / Case Studies (Idempotent upsert & ORM sync)
        self.stdout.write('Ensuring case studies in MongoDB and SQLite...')
        case_studies_data = [
            {
                'slug': 'echowithin-encrypted-platform',
                'title': 'EchoWithin - Private Encrypted Notes & Social Bonds Platform',
                'client': 'EchoWithin',
                'category': 'Web Development',
                'year': '2026',
                'image_url': 'img/echowithin-platform.webp',
                'live_url': 'https://echowithin.xyz',
                'summary': 'A secure digital sanctuary engineered for envelope-encrypted personal notes, relationship bond milestones, and ephemeral whisper messaging.',
                'challenge': 'The founders required an uncompromisingly private digital space for sensitive personal journaling and relationship bonds. The system demanded zero-knowledge data security, envelope encryption at rest, and instant real-time synchronization across mobile and desktop browsers without sacrificing battery or load speed.',
                'solution': 'We architected a hardened full-stack platform featuring envelope encryption with client-side key handling, PIN-locked spaces, habit synchronization, 30-day mood check-ins, self-destructing whisper chats with session watermarks and capture alerts, and an integrated community publishing engine.',
                'results': [
                    {'metric': '0', 'label': 'Unencrypted data leaks'},
                    {'metric': '1.0s', 'label': 'Core web speed index'},
                    {'metric': '100%', 'label': 'Mobile responsiveness'}
                ],
                'deliverables_summary': 'Encrypted data architecture, responsive PWA web client, whisper messaging system, relationship habit trackers, automated security hardening.',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'vinkj-auto-services-ecommerce',
                'title': 'VIN-KJ Auto Services - E-Commerce & Service Booking Platform',
                'client': 'VIN-KJ Auto Services',
                'category': 'E-Commerce',
                'year': '2026',
                'image_url': 'img/vinkj-ecommerce.webp',
                'live_url': 'https://vinkj.com',
                'summary': 'A high-performance automotive service booking engine and spare parts e-commerce catalog engineered for fast search and instant scheduling.',
                'challenge': 'VIN-KJ, a premier automotive enhancement workshop in Nairobi, needed to streamline customer bookings for window tinting, PPF, wrapping, and detailing while enabling customers to instantly search and purchase automotive spare parts from a responsive mobile-first catalog.',
                'solution': 'We engineered a bespoke, ultra-fast web platform featuring instant unified search across services and spare parts, a date-and-time service booking engine, interactive scope filtering, and direct WhatsApp quote routing with local SEO optimization.',
                'results': [
                    {'metric': '< 1.2s', 'label': 'Search & catalog latency'},
                    {'metric': '+58%', 'label': 'Online booking conversion'},
                    {'metric': '100%', 'label': 'Mobile-first usability'}
                ],
                'deliverables_summary': 'Custom inventory and services catalog, real-time live search engine, appointment booking engine, local SEO optimization, responsive mobile UI.',
                'published_at': now,
                'is_published': True
            }
        ]
        for cs in case_studies_data:
            db.case_studies.update_one({'slug': cs['slug']}, {'$set': cs}, upsert=True)
            Work.objects.update_or_create(
                slug=cs['slug'],
                defaults={
                    'title': cs['title'].split(' - ')[0],
                    'full_title': cs['title'],
                    'client': cs['client'],
                    'category': cs['category'],
                    'year': cs['year'],
                    'image_url': cs['image_url'],
                    'live_url': cs['live_url'],
                    'summary': cs['summary'],
                    'challenge': cs['challenge'],
                    'solution': cs['solution'],
                    'deliverables_summary': cs.get('deliverables_summary', ''),
                    'is_featured': True,
                    'is_published': True,
                }
            )

        # 3. Seed Insights / Articles (Idempotent upsert & ORM sync)
        self.stdout.write('Ensuring articles in MongoDB and SQLite...')
        posts_data = [
            {
                'slug': 'why-every-business-needs-a-website',
                'title': '4 Reasons Every Business Needs a Professional Website',
                'excerpt': 'From 24/7 visibility to customer trust, a modern website is your most powerful tool for business growth.',
                'content': (
                    'In today\'s digital world, your website is often the very first interaction a customer has with your business. '
                    'Having a professional website works for you around the clock, showcasing your services even while you sleep.\n\n'
                    'First, it provides 24/7 online presence, making your business visible to customers anytime and anywhere. '
                    'Second, it lets you reach more customers locally and globally, expanding your market far beyond foot traffic.\n\n'
                    'Third, it builds credibility and trust. Customers expect legitimate businesses to have a clean, modern online home. '
                    'And fourth, it directly increases sales by turning casual visitors into paying customers.'
                ),
                'author': 'Timothy Owino',
                'reading_time': '3 min read',
                'category': 'Business Growth',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'why-website-speed-matters',
                'title': 'Why Fast-Loading Websites Convert More Customers',
                'excerpt': 'A delay of just two seconds can cause over half your mobile visitors to leave. Here is how clean design keeps them engaged.',
                'content': (
                    'Mobile visitors expect websites to load instantly. When a site takes too long to appear, potential buyers click back to search results '
                    'and buy from your competitors instead.\n\n'
                    'At Idesignweb, we prioritize clean code and optimized media. By avoiding bloated plugins and heavy animations, '
                    'our websites load rapidly on all mobile networks, resulting in higher search rankings and happier customers.'
                ),
                'author': 'Vincent Odhiambo',
                'reading_time': '3 min read',
                'category': 'Web Development',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'essential-website-security-tips',
                'title': 'Simple Steps to Protect Your Website from Online Threats',
                'excerpt': 'Practical, non-technical steps any business owner can take to keep their website and customer information secure.',
                'content': (
                    'Keeping your website secure does not have to be complicated. Most security breaches happen because of simple oversights '
                    'like outdated software, weak passwords, or lack of automated backups.\n\n'
                    'By keeping your server software updated, enabling HTTPS encryption certificates, and scheduling automated daily backups, '
                    'you can protect your online store or company website from unexpected downtime.'
                ),
                'author': 'Vincent Odhiambo',
                'reading_time': '4 min read',
                'category': 'Cybersecurity',
                'published_at': now,
                'is_published': True
            }
        ]
        for p in posts_data:
            db.posts.update_one({'slug': p['slug']}, {'$set': p}, upsert=True)
            Article.objects.update_or_create(
                slug=p['slug'],
                defaults={
                    'title': p['title'],
                    'category': p['category'],
                    'author': p['author'],
                    'reading_time': p['reading_time'],
                    'summary': p['excerpt'],
                    'content': p['content'],
                    'is_published': True,
                }
            )

        self.stdout.write(self.style.SUCCESS('Platform initialization completed.'))

