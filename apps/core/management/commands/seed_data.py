"""
Management command to seed MongoDB and SQLite for Idesignweb.
Content adapted from company brand materials and Squarespace inspired architecture.
Zero emoji, zero em dashes, and complete flat design consistency.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.db import get_db, init_indexes
import datetime

class Command(BaseCommand):
    help = 'Seeds services, case studies, articles, and portal spaces adapted from company brief'

    def handle(self, *args, **options):
        self.stdout.write('Initializing indexes...')
        init_indexes()
        
        db = get_db()
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # 1. Seed Services (Web Development, Graphic Design, Video Editing, Cybersecurity)
        self.stdout.write('Seeding services collection...')
        db.services.delete_many({})
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
                'process_steps': [
                    {
                        'step_number': '01',
                        'title': 'Discovery and Sitemap',
                        'description': 'We discuss your business goals, target customers, and page structure to create a tailored blueprint.'
                    },
                    {
                        'step_number': '02',
                        'title': 'Design and Development',
                        'description': 'We craft custom layouts and write clean, fast code tested on mobile phones, tablets, and desktops.'
                    },
                    {
                        'step_number': '03',
                        'title': 'Launch and Maintenance',
                        'description': 'We launch your website live, connect your domain, and provide ongoing support whenever you need help.'
                    }
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
                'process_steps': [
                    {
                        'step_number': '01',
                        'title': 'Brand Consultation',
                        'description': 'We identify your brand personality, color preferences, and market positioning.'
                    },
                    {
                        'step_number': '02',
                        'title': 'Concept Creation',
                        'description': 'We create visual concepts, logo options, and typography layouts for your review.'
                    },
                    {
                        'step_number': '03',
                        'title': 'Final Vector Delivery',
                        'description': 'We deliver all final vector and print-ready files ready for web and physical production.'
                    }
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
                'process_steps': [
                    {
                        'step_number': '01',
                        'title': 'Footage Review',
                        'description': 'We review your raw recordings and organize the best shots for the storyline.'
                    },
                    {
                        'step_number': '02',
                        'title': 'Timeline Assembly',
                        'description': 'We cut the story to rhythm, sync audio, and share an initial cut for your feedback.'
                    },
                    {
                        'step_number': '03',
                        'title': 'Master Polish',
                        'description': 'We finalize colors, master sound levels, and deliver high-definition video files.'
                    }
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
                'process_steps': [
                    {
                        'step_number': '01',
                        'title': 'Security Audit',
                        'description': 'We inspect your website code and server settings for vulnerabilities and outdated software.'
                    },
                    {
                        'step_number': '02',
                        'title': 'Protection Implementation',
                        'description': 'We patch loopholes, configure firewalls, and install automated defense safeguards.'
                    },
                    {
                        'step_number': '03',
                        'title': 'Ongoing Monitoring',
                        'description': 'We keep your website backed up and monitored against unexpected attacks or downtime.'
                    }
                ],
                'featured': True,
                'sort_order': 4,
                'updated_at': now
            }
        ]
        db.services.insert_many(services_data)
        
        # 2. Seed Case Studies
        self.stdout.write('Seeding case_studies collection...')
        db.case_studies.delete_many({})
        case_studies_data = [
            {
                'slug': 'klar-form-modern-website',
                'title': 'Responsive E-Commerce Platform for Klar Form',
                'client': 'Klar Form',
                'category': 'Web Development',
                'year': '2026',
                'summary': 'A fast, mobile-friendly online store with instant product search and secure payment checkout.',
                'challenge': 'Klar Form was losing customers because their previous website took too long to load on mobile phones.',
                'solution': 'We built a modern responsive store with clean layouts, fast image loading, and a simple 2-step checkout.',
                'results': [
                    {'metric': '1.1s', 'label': 'Average mobile page load time'},
                    {'metric': '+42%', 'label': 'Increase in completed online sales'},
                    {'metric': '100%', 'label': 'Mobile responsiveness rating'}
                ],
                'deliverables_summary': 'Custom website, online store setup, payment gateway, SEO configuration.',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'nordic-furniture-brand-system',
                'title': 'Brand Identity and Logo Suite for Furniture Studio',
                'client': 'Klar Form Studio',
                'category': 'Graphic Design',
                'year': '2026',
                'summary': 'A complete visual identity redesign including logo suite, packaging templates, and promotional posters.',
                'challenge': 'The client needed an elevated, professional brand image to sell into premium retail galleries.',
                'solution': 'We designed a memorable minimalist logo, unified color palette, and elegant print collateral.',
                'results': [
                    {'metric': '+55%', 'label': 'Increase in retail inquiries'},
                    {'metric': '100%', 'label': 'Standardized print packaging'},
                    {'metric': '03', 'label': 'Design showcase features'}
                ],
                'deliverables_summary': 'Vector logo package, brand guidelines PDF, poster series, business cards.',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'kinetic-documentary-short',
                'title': 'Promotional Film and Social Cutdowns for Architecture Firm',
                'client': 'Modern Spaces',
                'category': 'Video Editing',
                'year': '2026',
                'summary': 'A six-minute showcase film paired with 15-second vertical cuts for Instagram and YouTube campaigns.',
                'challenge': 'The client needed engaging video content to demonstrate their commercial architectural work to prospective clients.',
                'solution': 'We edited footage with crisp cuts, natural ambient soundscapes, clean text overlays, and 4K color correction.',
                'results': [
                    {'metric': '240K', 'label': 'Total views across video channels'},
                    {'metric': '82%', 'label': 'Average watch completion rate'},
                    {'metric': '4K', 'label': 'High resolution master delivered'}
                ],
                'deliverables_summary': 'Master 4K video, 4 social media cuts, sound mix, YouTube master files.',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'zero-trust-cloud-infrastructure-audit',
                'title': 'Website Security Hardening and Automated Backups',
                'client': 'Vertex Media',
                'category': 'Cybersecurity',
                'year': '2026',
                'summary': 'A comprehensive security checkup, malware cleanup, and automated daily backup system for a media platform.',
                'challenge': 'Vertex Media experienced spam injections and required security hardening to protect client accounts.',
                'solution': 'We patched outdated software, installed web application firewalls, and configured automated daily offsite backups.',
                'results': [
                    {'metric': '0', 'label': 'Vulnerabilities remaining'},
                    {'metric': '99.99%', 'label': 'Uptime maintained'},
                    {'metric': 'Daily', 'label': 'Automated backups verified'}
                ],
                'deliverables_summary': 'Security audit report, server patches, firewall configuration, backup system.',
                'published_at': now,
                'is_published': True
            }
        ]
        db.case_studies.insert_many(case_studies_data)
        
        # 3. Seed Insights (Blog Posts)
        self.stdout.write('Seeding posts collection...')
        db.posts.delete_many({})
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
                'author': 'Timothy Owino',
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
                'author': 'Timothy Owino',
                'reading_time': '4 min read',
                'category': 'Security Advice',
                'published_at': now,
                'is_published': True
            }
        ]
        db.posts.insert_many(posts_data)
        
        # 4. Seed Member Announcements
        self.stdout.write('Seeding announcements collection...')
        db.announcements.delete_many({})
        announcements_data = [
            {
                'title': 'Scheduled Routine Server Updates This Sunday',
                'body': 'We will perform routine server updates this Sunday at 2:00 AM UTC. Services will remain available, and all project files are safe.',
                'priority': 'Notice',
                'audience': 'all',
                'date_str': '2026-09-12',
                'created_at': now,
                'active': True
            },
            {
                'title': 'High Resolution File Downloads Available in Asset Library',
                'body': 'You can now preview and download all your approved logo packages and brand assets directly from your client member portal.',
                'priority': 'Update',
                'audience': 'all',
                'date_str': '2026-09-08',
                'created_at': now,
                'active': True
            }
        ]
        db.announcements.insert_many(announcements_data)
        
        # 5. Seed Member Project Spaces
        self.stdout.write('Seeding projects collection...')
        db.projects.delete_many({})
        projects_data = [
            {
                'project_code': 'PRJ-2026-001',
                'client_username': 'client_apex',
                'title': 'New Responsive E-Commerce Website',
                'service_category': 'Web Development',
                'status': 'In Progress',
                'progress_percent': 70,
                'start_date': '2026-08-01',
                'target_date': '2026-10-15',
                'deliverables': [
                    {
                        'deliverable_id': 'DEL-01',
                        'title': 'Website sitemap and page layouts',
                        'version': '1.0',
                        'status': 'Approved',
                        'due_date': '2026-08-20',
                        'client_notes': 'Approved by client.'
                    },
                    {
                        'deliverable_id': 'DEL-02',
                        'title': 'Homepage and product catalog templates',
                        'version': '2.0',
                        'status': 'In Review',
                        'due_date': '2026-09-15',
                        'client_notes': 'Please review mobile menu alignment.'
                    },
                    {
                        'deliverable_id': 'DEL-03',
                        'title': 'Online checkout and payment setup',
                        'version': '0.9',
                        'status': 'Draft',
                        'due_date': '2026-10-01',
                        'client_notes': ''
                    }
                ],
                'created_at': now,
                'updated_at': now
            },
            {
                'project_code': 'PRJ-2026-002',
                'client_username': 'client_apex',
                'title': 'Brand Identity and Style Guidelines',
                'service_category': 'Graphic Design',
                'status': 'In Review',
                'progress_percent': 90,
                'start_date': '2026-08-15',
                'target_date': '2026-09-25',
                'deliverables': [
                    {
                        'deliverable_id': 'DEL-04',
                        'title': 'Logo concepts and color palette',
                        'version': '1.2',
                        'status': 'Approved',
                        'due_date': '2026-08-30',
                        'client_notes': 'Approved option 2.'
                    },
                    {
                        'deliverable_id': 'DEL-05',
                        'title': 'Print collateral and social media banners',
                        'version': '1.0',
                        'status': 'In Review',
                        'due_date': '2026-09-20',
                        'client_notes': ''
                    }
                ],
                'created_at': now,
                'updated_at': now
            }
        ]
        db.projects.insert_many(projects_data)
        
        # 6. Seed Member Assets
        self.stdout.write('Seeding assets collection...')
        db.assets.delete_many({})
        assets_data = [
            {
                'client_username': 'client_apex',
                'asset_code': 'AST-01',
                'name': 'Main Brand Logo Vector Package',
                'category': 'Logos',
                'format': 'SVG, PNG',
                'size': '2.4 MB',
                'version': '1.2',
                'updated_date': '2026-09-02'
            },
            {
                'client_username': 'client_apex',
                'asset_code': 'AST-02',
                'name': 'Brand Color Palette and Font Guide',
                'category': 'Style Guide',
                'format': 'PDF',
                'size': '420 KB',
                'version': '1.0',
                'updated_date': '2026-09-04'
            },
            {
                'client_username': 'client_apex',
                'asset_code': 'AST-03',
                'name': 'Promotional Video Intro Templates',
                'category': 'Video Templates',
                'format': 'MP4, MOV',
                'size': '184 MB',
                'version': '1.1',
                'updated_date': '2026-09-05'
            },
            {
                'client_username': 'client_apex',
                'asset_code': 'AST-04',
                'name': 'Website Security Checkup Summary',
                'category': 'Security Report',
                'format': 'PDF',
                'size': '1.8 MB',
                'version': '1.0',
                'updated_date': '2026-09-09'
            }
        ]
        db.assets.insert_many(assets_data)
        
        # 7. Seed Member Support Tickets
        self.stdout.write('Seeding tickets collection...')
        db.tickets.delete_many({})
        tickets_data = [
            {
                'ticket_id': 'TCK-1001',
                'client_username': 'client_apex',
                'subject': 'Question about logo file formats for print',
                'priority': 'Medium',
                'status': 'Resolved',
                'created_at': now - datetime.timedelta(days=5),
                'updated_at': now - datetime.timedelta(days=4),
                'messages': [
                    {
                        'sender': 'client_apex',
                        'role': 'client',
                        'text': 'Which logo file should our printing vendor use for our new business cards?',
                        'date_str': '2026-09-05 10:14'
                    },
                    {
                        'sender': 'Timothy Owino',
                        'role': 'staff',
                        'text': 'Please share the vector PDF or EPS file in your asset library with your printer for the highest quality.',
                        'date_str': '2026-09-05 11:30'
                    }
                ]
            },
            {
                'ticket_id': 'TCK-1002',
                'client_username': 'client_apex',
                'subject': 'Request for vertical video cut for Instagram',
                'priority': 'High',
                'status': 'In Progress',
                'created_at': now - datetime.timedelta(days=1),
                'updated_at': now,
                'messages': [
                    {
                        'sender': 'client_apex',
                        'role': 'client',
                        'text': 'Can we get a vertical 9:16 version of our promotional video for an Instagram story campaign?',
                        'date_str': '2026-09-09 14:20'
                    },
                    {
                        'sender': 'Timothy Owino',
                        'role': 'staff',
                        'text': 'Working on the vertical reframe now. We will upload it to your project space by tomorrow afternoon.',
                        'date_str': '2026-09-09 15:45'
                    }
                ]
            }
        ]
        db.tickets.insert_many(tickets_data)
        
        # 8. Seed SQLite Demo Users
        self.stdout.write('Seeding SQLite authentication users...')
        if not User.objects.filter(username='client_apex').exists():
            User.objects.create_user(
                username='client_apex',
                email='client@apex.com',
                password='MemberPass2026!',
                first_name='Apex',
                last_name='Corporation'
            )
            self.stdout.write('Created client user: client_apex')
            
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@idesignweb.com',
                password='AdminPass2026!'
            )
            self.stdout.write('Created admin user: admin')
            
        self.stdout.write(self.style.SUCCESS('All initial data seeded successfully.'))
