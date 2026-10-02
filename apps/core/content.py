"""
Core content module for Idesignweb.
Bridges Django ORM (SQLite database editable via /admin/) with lightweight code defaults.
Simple, clean, authentic data with zero metrics clutter.
"""

# Default authentic client projects (clean, simple, direct)
DEFAULT_WORKS = [
    {
        'slug': 'echowithin-encrypted-platform',
        'title': 'EchoWithin',
        'full_title': 'EchoWithin - Private Encrypted Notes & Social Bonds Platform',
        'client': 'EchoWithin',
        'category': 'Web Development',
        'year': '2026',
        'image_url': 'img/echowithin-platform.webp',
        'live_url': 'https://echowithin.xyz',
        'summary': 'A secure digital sanctuary engineered for envelope-encrypted personal notes, relationship bond milestones, and ephemeral whisper messaging.',
        'challenge': 'The founders required an uncompromisingly private digital space for sensitive personal journaling and relationship bonds. The system demanded zero-knowledge data security, envelope encryption at rest, and instant real-time synchronization across mobile and desktop browsers without sacrificing battery or load speed.',
        'solution': 'We architected a hardened full-stack platform featuring envelope encryption with client-side key handling, PIN-locked spaces, habit synchronization, 30-day mood check-ins, self-destructing whisper chats with session watermarks and capture alerts, and an integrated community publishing engine.',
        'deliverables_summary': 'Encrypted data architecture, responsive PWA web client, whisper messaging system, relationship habit trackers, automated security hardening.',
        'is_featured': True,
        'is_published': True
    },
    {
        'slug': 'vinkj-auto-services-ecommerce',
        'title': 'VIN-KJ Auto Services',
        'full_title': 'VIN-KJ Auto Services - E-Commerce & Service Booking Platform',
        'client': 'VIN-KJ Auto Services',
        'category': 'E-Commerce',
        'year': '2026',
        'image_url': 'img/vinkj-ecommerce.webp',
        'live_url': 'https://vinkj.com',
        'summary': 'A high-performance automotive service booking engine and spare parts e-commerce catalog engineered for fast search and instant scheduling.',
        'challenge': 'VIN-KJ, a premier automotive enhancement workshop in Nairobi, needed to streamline customer bookings for window tinting, PPF, wrapping, and detailing while enabling customers to instantly search and purchase automotive spare parts from a responsive mobile-first catalog.',
        'solution': 'We engineered a bespoke, ultra-fast web platform featuring instant unified search across services and spare parts, a date-and-time service booking engine, interactive scope filtering, and direct WhatsApp quote routing with local SEO optimization.',
        'deliverables_summary': 'Custom inventory and services catalog, real-time live search engine, appointment booking engine, local SEO optimization, responsive mobile UI.',
        'is_featured': True,
        'is_published': True
    }
]

# Studio Capabilities
SERVICES = [
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
        'sort_order': 1
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
        'sort_order': 2
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
        'sort_order': 3
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
        'sort_order': 4
    }
]

def _work_to_dict(w):
    """Normalize ORM model or dict into a standard dictionary."""
    if hasattr(w, 'title'):
        return {
            'slug': w.slug,
            'title': w.title,
            'full_title': getattr(w, 'full_title', '') or w.title,
            'client': w.client,
            'category': w.category,
            'year': w.year,
            'image_url': w.image_url,
            'live_url': w.live_url,
            'summary': w.summary,
            'challenge': w.challenge,
            'solution': w.solution,
            'deliverables_summary': w.deliverables_summary,
            'is_featured': w.is_featured,
            'is_published': w.is_published,
        }
    return w

def get_all_works(category=None, featured_only=False):
    """
    Retrieve all published works.
    Queries Django ORM (SQLite) first if records exist; falls back to DEFAULT_WORKS.
    """
    try:
        from apps.core.models import Work
        qs = Work.objects.filter(is_published=True)
        if featured_only:
            qs = qs.filter(is_featured=True)
        if category and category != 'all':
            qs = qs.filter(category__iexact=category)
        
        orm_works = list(qs)
        if orm_works:
            return [_work_to_dict(w) for w in orm_works]
    except Exception:
        pass

    # Fallback to code defaults
    items = list(DEFAULT_WORKS)
    if featured_only:
        items = [w for w in items if w.get('is_featured', True)]
    if category and category != 'all':
        items = [w for w in items if w.get('category', '').lower() == category.lower()]
    return items

def get_work_by_slug(slug):
    """Find a single work project by its slug from DB or fallback."""
    try:
        from apps.core.models import Work
        work_obj = Work.objects.filter(slug=slug, is_published=True).first()
        if work_obj:
            return _work_to_dict(work_obj)
    except Exception:
        pass

    for w in DEFAULT_WORKS:
        if w.get('slug') == slug:
            return w
    return None

def get_all_services(featured_only=False):
    """Retrieve studio service offerings."""
    if featured_only:
        return [s for s in SERVICES if s.get('featured', False)]
    return list(SERVICES)

def get_service_by_slug(slug):
    """Find a single service by its slug."""
    for s in SERVICES:
        if s.get('slug') == slug:
            return s
    return None

def get_work_categories():
    """Distinct categories for work projects."""
    works = get_all_works()
    cats = []
    for w in works:
        cat = w.get('category')
        if cat and cat not in cats:
            cats.append(cat)
    return cats


# ==============================================================================
# Editorial Articles & Technical Insights
# ==============================================================================

DEFAULT_ARTICLES = [
    {
        'title': 'Building EchoWithin: From a Simple Blog to an Encrypted Social Platform',
        'slug': 'building-echowithin-encrypted-platform',
        'category': 'Engineering & Architecture',
        'author': 'Vincent Odhiambo & Timothy Owino',
        'reading_time': '3 min read',
        'summary': 'What started as a straightforward blogging engine quickly evolved into a multi-layered private social platform. Here is how we tackled zero-knowledge security, envelope encryption at rest, and cross-device synchronization without degrading battery life or speed.',
        'content': """Building EchoWithin was one of the most demanding yet rewarding projects we have engineered at Idesignweb.

### The Evolution: Scope Expansion

The platform was originally scoped as a clean, focused digital publishing blog. However, as the project progressed, the product vision expanded significantly. The client required a digital sanctuary that could combine multiple distinct modes of interaction under one cohesive interface: long-form publishing, direct messaging, relationship bonds, private encrypted notes, interest-driven community spaces, and interactive games.

With each new layer, architectural complexity grew exponentially. We were no longer building a read-heavy blog; we were now architecting a high-concurrency real-time application where personal privacy was the non-negotiable core.

### Engineering Private Data in Shared Spaces

The central technical challenge was ensuring user data remained strictly confidential across fundamentally different surfaces:
- In public community discussions, identities and personal notes had to stay completely isolated.
- In private bonds, two users needed selective, shared visibility into mutual goals, daily check-ins, and collaborative games without exposing the rest of their account.
- In private notes, data had to be inaccessible even to database administrators.

To achieve this, the architecture demanded zero-knowledge data security with envelope encryption at rest. Keys are isolated per record and per user session, ensuring that neither server breaches nor database snapshots can expose decrypted content.

### Security vs. Performance Tradeoffs

Real-world security always introduces friction. Envelope encryption and client-side cryptographic handshakes are computationally expensive, especially on low-powered mobile hardware.

Our core challenge was achieving instant, real-time synchronization across desktop and mobile browsers without draining the user's battery or degrading initial page load times. We addressed this through:
- Streamlined cryptographic routines optimized for WebAssembly and modern browser crypto primitives.
- Lightweight diff-based state sync over WebSockets instead of heavy full-payload polling.
- Aggressive client caching for non-sensitive interface assets while keeping decrypted payload memory ephemeral.

### Where the Platform Stands Today

EchoWithin is currently in active staging and deployment, undergoing continuous penetration testing, edge-case vulnerability assessments, and active security monitoring.

It stands as a blueprint for how modern social platforms can deliver deep community interactivity without treating personal user privacy as an afterthought.""",
        'is_published': True,
    }
]

def _article_to_dict(art):
    return {
        'id': art.id,
        'title': art.title,
        'slug': art.slug,
        'category': art.category,
        'author': art.author,
        'reading_time': art.reading_time,
        'summary': art.summary,
        'excerpt': art.excerpt,
        'content': art.content,
        'rendered_content': art.rendered_content,
        'published_at': art.published_at,
        'is_published': art.is_published,
    }

def get_all_articles():
    """Retrieve all published editorial articles from SQLite ORM or fallback."""
    try:
        from apps.core.models import Article
        qs = Article.objects.filter(is_published=True).order_by('-published_at')
        orm_articles = list(qs)
        if orm_articles:
            return [_article_to_dict(a) for a in orm_articles]
    except Exception:
        pass

    return list(DEFAULT_ARTICLES)

def get_article_by_slug(slug):
    """Retrieve a single article by its slug from DB or fallback."""
    try:
        from apps.core.models import Article
        art = Article.objects.filter(slug=slug, is_published=True).first()
        if art:
            return _article_to_dict(art)
    except Exception:
        pass

    for a in DEFAULT_ARTICLES:
        if a.get('slug') == slug:
            copy = dict(a)
            if 'rendered_content' not in copy:
                import html, re
                blocks = re.split(r'\n\s*\n', copy.get('content', '').strip())
                html_blocks = []
                for block in blocks:
                    lines = [line.strip() for line in block.split('\n') if line.strip()]
                    if not lines: continue
                    first = lines[0]
                    if first.startswith('### '):
                        html_blocks.append(f'<h3 style="font-size: 1.35rem; font-weight: 700; margin-top: var(--space-2xl); margin-bottom: var(--space-sm); color: var(--text-main); line-height: 1.3;">{html.escape(first[4:])}</h3>')
                    elif first.startswith('## '):
                        html_blocks.append(f'<h2 style="font-size: 1.6rem; font-weight: 700; margin-top: var(--space-2xl); margin-bottom: var(--space-sm); color: var(--text-main); line-height: 1.3;">{html.escape(first[3:])}</h2>')
                    elif all(l.startswith('- ') for l in lines):
                        items = "".join(f'<li style="margin-bottom: 6px;">{html.escape(l[2:])}</li>' for l in lines)
                        html_blocks.append(f'<ul style="padding-left: 24px; margin-bottom: var(--space-lg); line-height: 1.75; color: var(--text-body);">{items}</ul>')
                    else:
                        para = '<br>'.join(html.escape(l) for l in lines)
                        html_blocks.append(f'<p style="margin-bottom: var(--space-lg); line-height: 1.8; color: var(--text-body);">{para}</p>')
                copy['rendered_content'] = '\n'.join(html_blocks)
            return copy
    return None
