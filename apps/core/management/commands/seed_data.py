"""
Management command to populate MongoDB and SQLite with initial data for idesignweb.
Ensures zero emoji, zero em dashes, and complete flat design consistency.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.db import get_db, init_indexes
import datetime

class Command(BaseCommand):
    help = 'Seeds initial services, case studies, insights, portal data, and demo user'

    def handle(self, *args, **options):
        self.stdout.write('Initializing indexes...')
        init_indexes()
        
        db = get_db()
        now = datetime.datetime.now(datetime.timezone.utc)
        
        # 1. Seed Services (01-04)
        self.stdout.write('Seeding services collection...')
        db.services.delete_many({})
        services_data = [
            {
                'slug': 'graphic-design',
                'service_number': '01',
                'title': 'Graphic Design',
                'tagline': 'Visual identities, typography systems, and print architecture.',
                'overview': 'We build comprehensive visual identity systems, poster series, and editorial structures founded on rigorous typographic discipline and balanced layout grids.',
                'deliverables': [
                    'Brand identity guidelines and token specifications',
                    'Poster series and high-impact physical collateral',
                    'Custom display typography and typographic hierarchies',
                    'Packaging systems and technical specifications'
                ],
                'process_steps': [
                    {
                        'step_number': '01',
                        'title': 'Typography and Grid Audit',
                        'description': 'Evaluating core proportions, reading distance, and medium constraints.'
                    },
                    {
                        'step_number': '02',
                        'title': 'System Formulation',
                        'description': 'Drafting modular typographic pairings, spatial rules, and baseline alignments.'
                    },
                    {
                        'step_number': '03',
                        'title': 'Deliverable Production',
                        'description': 'Finalizing vector packages, print-ready files, and mechanical specifications.'
                    }
                ],
                'featured': True,
                'sort_order': 1,
                'updated_at': now
            },
            {
                'slug': 'video-editing',
                'service_number': '02',
                'title': 'Video Editing',
                'tagline': 'Post-production, motion graphics, and narrative editing.',
                'overview': 'Precision editorial assembly for commercial, documentary, and product narratives. We combine structured pacing with subtle motion design and disciplined color grading.',
                'deliverables': [
                    'Master assembly cuts and multi-format adaptations',
                    'Motion typography and kinetic informational graphics',
                    'Sound mixing, dialogue balancing, and acoustic mastering',
                    'Color grading tailored for calibrated digital displays'
                ],
                'process_steps': [
                    {
                        'step_number': '01',
                        'title': 'Rhythm and Cut Assembly',
                        'description': 'Structuring chronological narrative flow, dialogue density, and thematic timing.'
                    },
                    {
                        'step_number': '02',
                        'title': 'Motion Integration',
                        'description': 'Applying frame-accurate kinetic typography and informational overlays.'
                    },
                    {
                        'step_number': '03',
                        'title': 'Master Mastering',
                        'description': 'Color pass, audio master leveling, and high-bitrate output delivery.'
                    }
                ],
                'featured': True,
                'sort_order': 2,
                'updated_at': now
            },
            {
                'slug': 'web-development',
                'service_number': '03',
                'title': 'Web Development',
                'tagline': 'Engineered digital platforms, clean codebases, and performant systems.',
                'overview': 'Modern web solutions constructed without unnecessary bloat. Fast loading, strictly typed, accessible, and structured for long-term maintainability.',
                'deliverables': [
                    'Semantic server-rendered and progressive web applications',
                    'Bespoke content management pipelines and custom admin tools',
                    'High-efficiency relational and document storage integrations',
                    'Lighthouse 100 performance benchmarks and full accessibility audits'
                ],
                'process_steps': [
                    {
                        'step_number': '01',
                        'title': 'Architecture and Schema Blueprint',
                        'description': 'Formulating clean data contracts, routing structures, and caching layers.'
                    },
                    {
                        'step_number': '02',
                        'title': 'Component Engineering',
                        'description': 'Constructing accessible HTML, lightweight CSS, and modular script layers.'
                    },
                    {
                        'step_number': '03',
                        'title': 'Testing and Verification',
                        'description': 'Rigorous latency testing, security review, and cross-browser verification.'
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
                'tagline': 'Vulnerability assessments, infrastructure hardening, and defensive auditing.',
                'overview': 'Systematic threat modeling and technical assessment to protect web infrastructure, client data repositories, and digital workflow pipelines against modern adversaries.',
                'deliverables': [
                    'Comprehensive penetration testing and web application vulnerability audits',
                    'Infrastructure configuration hardening and credential lifecycle policies',
                    'Network traffic analysis and threat perimeter modeling',
                    'Compliance documentation and incident response playbooks'
                ],
                'process_steps': [
                    {
                        'step_number': '01',
                        'title': 'Perimeter Reconnaissance',
                        'description': 'Mapping external attack surfaces, exposed services, and configuration drift.'
                    },
                    {
                        'step_number': '02',
                        'title': 'Defensive Hardening',
                        'description': 'Closing exploit vectors, enforcing zero-trust policies, and patching endpoints.'
                    },
                    {
                        'step_number': '03',
                        'title': 'Formal Verification',
                        'description': 'Delivering technical remediation reports and ongoing defensive telemetry.'
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
                'slug': 'nordic-furniture-brand-system',
                'title': 'Nordic Furniture Visual Identity',
                'client': 'Klar Form',
                'category': 'Graphic Design',
                'year': '2026',
                'summary': 'A complete typographic framework and packaging architecture for an architectural furniture studio.',
                'challenge': 'The client required a brand identity that avoided decorative excess while commanding immediate authority in gallery and retail environments.',
                'solution': 'Engineered a modular hairline grid system, custom numeral styles, and a monochrome structural packaging palette.',
                'results': [
                    {'metric': '+48%', 'label': 'Increase in direct architect inquiries'},
                    {'metric': '100%', 'label': 'Packaging material standardization across product lines'},
                    {'metric': '03', 'label': 'International design awards received'}
                ],
                'deliverables_summary': 'Identity manual, mechanical packaging blueprints, poster catalog series.',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'kinetic-documentary-short',
                'title': 'Industrial Architecture Motion Short',
                'client': 'Brutal Arch Review',
                'category': 'Video Editing',
                'year': '2026',
                'summary': 'Six-minute architectural documentary examining concrete forms across Central Europe.',
                'challenge': 'Translating massive static concrete structures into compelling cinematic progression without intrusive music or exaggerated pacing.',
                'solution': 'Developed an austere cutting rhythm based on architectural vanishing points, augmented with ambient sound field balancing and minimalist typographic chapter titles.',
                'results': [
                    {'metric': '240K', 'label': 'Organic festival and digital stream views'},
                    {'metric': '84%', 'label': 'Full completion rate on digital platforms'},
                    {'metric': '4K', 'label': 'Native HDR master delivery specification'}
                ],
                'deliverables_summary': 'Master 4K theatrical cut, high-bitrate streaming deliverable, archival master.',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'high-throughput-fintech-interface',
                'title': 'High-Throughput Financial Analytics Platform',
                'client': 'Aura Ledger',
                'category': 'Web Development',
                'year': '2026',
                'summary': 'Real-time settlement interface handling dense tabular transaction streams with zero visual lag.',
                'challenge': 'Eliminating layout shifts and rendering latency for high-frequency algorithmic traders monitoring millions of ledger entries.',
                'solution': 'Constructed a custom server-rendered layout with targeted vanilla DOM updates and tabular numeric alignment.',
                'results': [
                    {'metric': '18ms', 'label': 'Median server response time under peak load'},
                    {'metric': '0.00', 'label': 'Cumulative Layout Shift (CLS) score'},
                    {'metric': '60fps', 'label': 'Sustained display rendering rate'}
                ],
                'deliverables_summary': 'Platform codebase, database indexing blueprint, component documentation.',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'zero-trust-cloud-infrastructure-audit',
                'title': 'Zero-Trust Infrastructure Hardening',
                'client': 'Vector Vault',
                'category': 'Cybersecurity',
                'year': '2026',
                'summary': 'Comprehensive vulnerability assessment and attack surface remediation for an enterprise data vault.',
                'challenge': 'Complex legacy firewall rules and distributed IAM roles left undocumented privilege escalation pathways.',
                'solution': 'Executed automated and manual penetration testing routines, followed by strict least-privilege role consolidation and endpoint hardening.',
                'results': [
                    {'metric': '100%', 'label': 'Critical vulnerabilities identified and resolved'},
                    {'metric': '-72%', 'label': 'Reduction in external exposed surface area'},
                    {'metric': 'ISO', 'label': 'Certification readiness achieved ahead of schedule'}
                ],
                'deliverables_summary': 'Threat matrix report, remediation scripts, executive defense summary.',
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
                'slug': 'principles-of-hairline-ui-design',
                'title': 'Principles of Hairline Interface Design',
                'excerpt': 'Why removing decorative shadows and gradients yields faster, more authoritative interfaces.',
                'content': (
                    'Visual clarity in digital product design often degrades through the accumulation of decorative treatments: '
                    'subtle gradients, diffuse shadows, and unnecessary icon flourishes. When these elements are eliminated, '
                    'structure and typography must perform the structural communication.\n\n'
                    'A hairline border (0.5px to 1px) creates exact spatial boundaries without introducing visual weight. '
                    'Paired with disciplined tabular numerals and a restricted typographic hierarchy, interfaces communicate '
                    'data density cleanly and with institutional authority.'
                ),
                'author': 'idesignweb Architecture',
                'reading_time': '4 min read',
                'category': 'Design Systems',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'securing-modern-web-workloads',
                'title': 'Securing Modern Web Workloads Without Cognitive Friction',
                'excerpt': 'Strategic defense mechanisms that protect member portals without encumbering legitimate users.',
                'content': (
                    'Gated digital platforms require uncompromising perimeter defenses. However, complex defense configurations '
                    'frequently introduce friction that damages operational velocity.\n\n'
                    'By deploying strict HTTP security headers, mandatory noindex directives on authenticated routes, '
                    'and rate-limited session validation at the routing layer, systems achieve robust threat isolation '
                    'while preserving rapid user interactions.'
                ),
                'author': 'idesignweb Security Team',
                'reading_time': '6 min read',
                'category': 'Cybersecurity',
                'published_at': now,
                'is_published': True
            },
            {
                'slug': 'typographic-motion-in-brand-systems',
                'title': 'Typographic Motion in Brand Systems',
                'excerpt': 'How disciplined kinetic typography reinforces corporate identity across video and interactive media.',
                'content': (
                    'Kinetic typography should never exist solely for spectacle. In a disciplined brand system, motion communicates '
                    'cadence, hierarchy, and relationship between concepts.\n\n'
                    'By constraining motion curves to linear or crisp cubic bezier transitions and maintaining rigid baseline alignment, '
                    'typographic movement amplifies the message rather than distracting from it.'
                ),
                'author': 'idesignweb Motion Group',
                'reading_time': '5 min read',
                'category': 'Video & Motion',
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
                'title': 'Scheduled Infrastructure Upgrade Notice',
                'body': 'Platform database optimization is scheduled for Sunday at 02:00 UTC. No deliverable approval workflows will be interrupted.',
                'priority': 'Normal',
                'audience': 'all',
                'date_str': '2026-09-12',
                'created_at': now,
                'active': True
            },
            {
                'title': 'Asset Library Version 2.0 Released',
                'body': 'The client asset library now features direct checksum verification and batch archive downloads for approved vector packages.',
                'priority': 'Info',
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
                'title': 'E-Commerce Core Web Architecture',
                'service_category': 'Web Development',
                'status': 'In Progress',
                'progress_percent': 70,
                'start_date': '2026-08-01',
                'target_date': '2026-10-15',
                'deliverables': [
                    {
                        'deliverable_id': 'DEL-01',
                        'title': 'System Information Architecture and Data Contracts',
                        'version': '1.0',
                        'status': 'Approved',
                        'due_date': '2026-08-20',
                        'client_notes': 'Confirmed and approved by technical director.'
                    },
                    {
                        'deliverable_id': 'DEL-02',
                        'title': 'Core Layout Templates and Component System',
                        'version': '2.0',
                        'status': 'In Review',
                        'due_date': '2026-09-15',
                        'client_notes': 'Pending final client review of responsive breakpoints.'
                    },
                    {
                        'deliverable_id': 'DEL-03',
                        'title': 'Backend Data Store and Caching Integration',
                        'version': '0.9',
                        'status': 'Draft',
                        'due_date': '2026-10-01',
                        'client_notes': 'Internal testing in progress.'
                    }
                ],
                'created_at': now,
                'updated_at': now
            },
            {
                'project_code': 'PRJ-2026-002',
                'client_username': 'client_apex',
                'title': 'Identity and Typographic Design Guidelines',
                'service_category': 'Graphic Design',
                'status': 'In Review',
                'progress_percent': 90,
                'start_date': '2026-08-15',
                'target_date': '2026-09-25',
                'deliverables': [
                    {
                        'deliverable_id': 'DEL-04',
                        'title': 'Primary Vector Wordmark and Monogram System',
                        'version': '1.2',
                        'status': 'Approved',
                        'due_date': '2026-08-30',
                        'client_notes': 'Approved without revision.'
                    },
                    {
                        'deliverable_id': 'DEL-05',
                        'title': 'Brand Manual and Mechanical Print Specifications',
                        'version': '1.0',
                        'status': 'In Review',
                        'due_date': '2026-09-20',
                        'client_notes': 'Client review underway.'
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
                'name': 'Primary Brand Wordmark Vector Suite',
                'category': 'Identity',
                'format': 'SVG, PDF',
                'size': '2.4 MB',
                'version': '1.2',
                'updated_date': '2026-09-02'
            },
            {
                'client_username': 'client_apex',
                'asset_code': 'AST-02',
                'name': 'Typography Specification and Token Map',
                'category': 'Design Tokens',
                'format': 'JSON, PDF',
                'size': '420 KB',
                'version': '1.0',
                'updated_date': '2026-09-04'
            },
            {
                'client_username': 'client_apex',
                'asset_code': 'AST-03',
                'name': 'Motion Title Kit and Video Presets',
                'category': 'Video Assets',
                'format': 'ZIP, ProRes',
                'size': '184 MB',
                'version': '1.1',
                'updated_date': '2026-09-05'
            },
            {
                'client_username': 'client_apex',
                'asset_code': 'AST-04',
                'name': 'Infrastructure Vulnerability Assessment Report',
                'category': 'Security Audit',
                'format': 'Encrypted PDF',
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
                'subject': 'Clarification on web font licensing scope',
                'priority': 'Medium',
                'status': 'Resolved',
                'created_at': now - datetime.timedelta(days=5),
                'updated_at': now - datetime.timedelta(days=4),
                'messages': [
                    {
                        'sender': 'client_apex',
                        'role': 'client',
                        'text': 'Does the enterprise license cover internal subdomains for staging environments?',
                        'date_str': '2026-09-05 10:14'
                    },
                    {
                        'sender': 'idesignweb Support',
                        'role': 'staff',
                        'text': 'Yes, the enterprise typography license encompasses all development, staging, and production subdomains.',
                        'date_str': '2026-09-05 11:30'
                    }
                ]
            },
            {
                'ticket_id': 'TCK-1002',
                'client_username': 'client_apex',
                'subject': 'Request for secondary video cut in 9:16 aspect ratio',
                'priority': 'High',
                'status': 'In Progress',
                'created_at': now - datetime.timedelta(days=1),
                'updated_at': now,
                'messages': [
                    {
                        'sender': 'client_apex',
                        'role': 'client',
                        'text': 'We require a vertical 9:16 cut of the industrial architecture film for digital showcase displays.',
                        'date_str': '2026-09-09 14:20'
                    },
                    {
                        'sender': 'idesignweb Support',
                        'role': 'staff',
                        'text': 'Reframing sequence underway. Render expected in the deliverable space by tomorrow 16:00 UTC.',
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
