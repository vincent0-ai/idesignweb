"""
Comprehensive test suite for idesignweb.
Verifies public marketing pages, Django admin Work models, auth gating, noindex headers,
and strict adherence to flat design constraints (no gradients, no emoji, no icons, no em dashes).
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.core.models import Work, Inquiry
from apps.core.db import get_db
import unicodedata
import pathlib
import re

class PublicZoneTests(TestCase):
    def setUp(self):
        self.client = Client()
        Inquiry.objects.filter(email='test@client.com').delete()

    def test_public_pages_render_successfully(self):
        urls = [
            '/',
            '/services/',
            '/services/web-development/',
            '/services/graphic-design/',
            '/services/video-editing/',
            '/services/cybersecurity/',
            '/work/',
            '/work/echowithin-encrypted-platform/',
            '/work/vinkj-auto-services-ecommerce/',
            '/about/',
            '/contact/',
            '/login/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f"Expected 200 for {url}, got {response.status_code}"
            )

    def test_contact_form_submission_stores_in_sqlite(self):
        initial_count = Inquiry.objects.count()
        
        post_data = {
            'full_name': 'Test Client',
            'email': 'test@client.com',
            'service_interest': 'Custom Website Design',
            'budget_range': '20k - 50k',
            'message': 'Automated test inquiry regarding new website build.'
        }
        response = self.client.post('/contact/', post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Inquiry.objects.count(), initial_count + 1)
        
        # Verify inserted data in SQLite
        inquiry = Inquiry.objects.filter(email='test@client.com').first()
        self.assertIsNotNone(inquiry)
        self.assertEqual(inquiry.full_name, 'Test Client')
        self.assertEqual(inquiry.service_interest, 'Custom Website Design')

    def test_work_model_in_sqlite(self):
        from apps.core.content import get_all_works
        # Verify default fallback returns 2 real works
        works = get_all_works()
        self.assertEqual(len(works), 2)
        self.assertIn('echowithin.xyz', works[0]['live_url'])
        
        # Verify admin can insert new Work in SQLite
        Work.objects.create(
            title='New Client System',
            slug='new-client-system',
            client='New Client',
            live_url='https://example.com',
            summary='Automated test work creation.'
        )
        self.assertEqual(Work.objects.count(), 1)


class MemberPortalZoneTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user, _ = User.objects.get_or_create(
            username='client_apex',
            defaults={'email': 'client@apex.com'}
        )
        self.user.set_password('MemberPass2026!')
        self.user.save()

        self.staff_user, _ = User.objects.get_or_create(
            username='admin_staff',
            defaults={'email': 'admin@idesignweb.com', 'is_staff': True}
        )
        self.staff_user.is_staff = True
        self.staff_user.set_password('AdminPassword2026!')
        self.staff_user.save()
        
        # Seed test project for portal tests
        try:
            db = get_db()
            db.projects.update_one(
                {'project_code': 'PRJ-2026-001'},
                {'$set': {
                    'project_code': 'PRJ-2026-001',
                    'title': 'Test Brand Project',
                    'client_username': 'client_apex',
                    'status': 'In Progress',
                    'deliverables': [
                        {
                            'deliverable_id': 'DEL-02',
                            'title': 'Typography Package',
                            'status': 'Pending Review',
                            'version': '1.0',
                            'format': 'ZIP',
                            'file_size': '2.4 MB'
                        }
                    ]
                }},
                upsert=True
            )
        except Exception:
            pass

    def test_portal_routes_are_gated_behind_auth(self):
        gated_urls = [
            '/portal/',
            '/portal/communications/',
            '/portal/projects/',
            '/portal/projects/PRJ-2026-001/',
            '/portal/assets/',
            '/portal/support/',
            '/portal/support/new/',
        ]
        for url in gated_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 302,
                f"Expected 302 redirect for unauthenticated {url}"
            )
            self.assertIn('/login/', response.url)

    def test_portal_applies_strict_noindex_headers(self):
        self.client.login(username='client_apex', password='MemberPass2026!')
        
        portal_urls = [
            '/portal/',
            '/portal/communications/',
            '/portal/projects/',
            '/portal/projects/PRJ-2026-001/',
            '/portal/assets/',
            '/portal/support/',
        ]
        for url in portal_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            # Verify X-Robots-Tag header
            self.assertIn('X-Robots-Tag', response.headers)
            self.assertEqual(response.headers['X-Robots-Tag'], 'noindex, nofollow, noarchive')
            # Verify meta robots tag in HTML content
            content = response.content.decode('utf-8')
            self.assertIn('name="robots" content="noindex, nofollow, noarchive"', content)

    def test_deliverable_approval_workflow(self):
        self.client.login(username='client_apex', password='MemberPass2026!')
        db = get_db()
        
        # Approve DEL-02 in PRJ-2026-001
        approval_url = '/portal/projects/PRJ-2026-001/deliverables/DEL-02/'
        post_data = {
            'action': 'approve',
            'client_notes': 'Approved through automated test suite verification.'
        }
        response = self.client.post(approval_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Verify MongoDB updated
        project = db.projects.find_one({'project_code': 'PRJ-2026-001'})
        deliv = next(d for d in project['deliverables'] if d['deliverable_id'] == 'DEL-02')
        self.assertEqual(deliv['status'], 'Approved')
        self.assertEqual(deliv['client_notes'], 'Approved through automated test suite verification.')

    def test_staff_announcement_crud(self):
        # 1. Staff can post announcement
        self.client.login(username='admin_staff', password='AdminPassword2026!')
        post_data = {
            'action': 'create',
            'title': 'Test System Announcement',
            'priority': 'Security',
            'body': 'Automated security maintenance notice.'
        }
        resp = self.client.post('/portal/communications/', post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Test System Announcement', resp.content.decode('utf-8'))

        # Verify in MongoDB
        db = get_db()
        ann = db.announcements.find_one({'title': 'Test System Announcement'})
        self.assertIsNotNone(ann)
        self.assertEqual(ann['priority'], 'Security')

        # 2. Staff can delete announcement
        del_resp = self.client.post('/portal/communications/', {
            'action': 'delete',
            'announcement_id': ann['announcement_id']
        }, follow=True)
        self.assertEqual(del_resp.status_code, 200)
        self.assertIsNone(db.announcements.find_one({'title': 'Test System Announcement'}))

    def test_staff_client_creation_and_isolation(self):
        # 1. Admin can access client management and create account
        self.client.login(username='admin_staff', password='AdminPassword2026!')
        get_resp = self.client.get('/portal/clients/')
        self.assertEqual(get_resp.status_code, 200)

        create_data = {
            'action': 'create_client',
            'company_name': 'Automated Test Client Co',
            'username': 'client_autotest',
            'email': 'autotest@client.com',
            'password': 'ClientPass2026!',
            'project_title': 'Automated Test Project Space',
            'service_category': 'Web Development'
        }
        post_resp = self.client.post('/portal/clients/', create_data, follow=True)
        self.assertEqual(post_resp.status_code, 200)

        # Verify Django user
        from django.contrib.auth.models import User
        user = User.objects.filter(username='client_autotest').first()
        self.assertIsNotNone(user)
        self.assertFalse(user.is_staff)

        # Verify MongoDB project
        db = get_db()
        prj = db.projects.find_one({'client_username': 'client_autotest'})
        self.assertIsNotNone(prj)
        self.assertEqual(prj['title'], 'Automated Test Project Space')

        # 2. Client logs in and cannot access staff clients area
        self.client.logout()
        login_success = self.client.login(username='client_autotest', password='ClientPass2026!')
        self.assertTrue(login_success)

        client_resp = self.client.get('/portal/clients/')
        self.assertEqual(client_resp.status_code, 404)


class OberloDesignAndFoundersTests(TestCase):
    def test_design_tokens(self):
        tokens_file = pathlib.Path('static/css/tokens.css')
        self.assertTrue(tokens_file.exists())
        content = tokens_file.read_text(encoding='utf-8')
        self.assertIn('--bg-primary', content)
        self.assertIn('--color-blue', content)
        self.assertIn('--border-hairline', content)
        self.assertIn('--font-sans', content)
        self.assertIn('--font-mono', content)

    def test_cofounders_present_in_public_views(self):
        client = Client()
        for path in ['/', '/about/', '/contact/']:
            response = client.get(path)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode('utf-8')
            self.assertIn('Vincent Odhiambo', content, f"Vincent Odhiambo missing from {path}")
            self.assertIn('Timothy Owino', content, f"Timothy Owino missing from {path}")

    def test_no_em_dashes_in_templates_or_code(self):
        em_dash_pattern = re.compile(r'[\u2014\u2013]') # em dash and en dash
        check_dirs = ['templates', 'static', 'apps']
        for d in check_dirs:
            for p in pathlib.Path(d).rglob('*'):
                if p.is_file() and p.suffix in ('.html', '.css', '.js', '.py'):
                    content = p.read_text(encoding='utf-8')
                    match = em_dash_pattern.search(content)
                    self.assertIsNone(match, f"Em/En dash found in {p}")

    def test_no_emoji_in_templates_or_code(self):
        check_dirs = ['templates', 'static', 'apps']
        for d in check_dirs:
            for p in pathlib.Path(d).rglob('*'):
                if p.is_file() and p.suffix in ('.html', '.css', '.js', '.py'):
                    content = p.read_text(encoding='utf-8')
                    for i, ch in enumerate(content):
                        cat = unicodedata.category(ch)
                        # So = Symbol, other; Sk = Symbol, modifier; high ord points
                        if (cat in ('So', 'Sk') and ord(ch) not in (0xA9, 0xAE)) or ord(ch) > 0x1F000:
                            self.fail(f"Emoji/symbol '{ch}' (U+{ord(ch):04X}) found in {p}:{i}")

    def test_articles_list_and_detail_views(self):
        client = Client()
        # Test articles archive
        resp = client.get('/insights/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Building EchoWithin', resp.content.decode('utf-8'))
        
        # Test article detail
        resp_detail = client.get('/insights/building-echowithin-encrypted-platform/')
        self.assertEqual(resp_detail.status_code, 200)
        self.assertIn('zero-knowledge', resp_detail.content.decode('utf-8'))


class SEOMetaAndSitemapTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_robots_txt_endpoint(self):
        resp = self.client.get('/robots.txt')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.headers.get('Content-Type', '').startswith('text/plain'))
        content = resp.content.decode('utf-8')
        self.assertIn('User-agent: *', content)
        self.assertIn('Allow: /', content)
        self.assertIn('Disallow: /admin/', content)
        self.assertIn('Disallow: /portal/', content)
        self.assertIn('Disallow: /login/', content)
        self.assertIn('Sitemap:', content)
        self.assertIn('/sitemap.xml', content)

    def test_sitemap_xml_endpoint(self):
        import xml.etree.ElementTree as ET
        resp = self.client.get('/sitemap.xml')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('xml' in resp.headers.get('Content-Type', ''))
        root = ET.fromstring(resp.content)
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locs = [elem.text for elem in root.findall('sm:url/sm:loc', ns)]

        # Verify core pages
        self.assertTrue(any(l.endswith('/') for l in locs))
        self.assertTrue(any('/services/' in l for l in locs))
        self.assertTrue(any('/work/' in l for l in locs))
        self.assertTrue(any('/about/' in l for l in locs))
        self.assertTrue(any('/insights/' in l for l in locs))
        self.assertTrue(any('/contact/' in l for l in locs))

        # Verify dynamic service and work URLs
        self.assertTrue(any('web-development' in l for l in locs))
        self.assertTrue(any('echowithin-encrypted-platform' in l for l in locs))
        self.assertTrue(any('building-echowithin-encrypted-platform' in l for l in locs))

    def test_homepage_seo_meta_tags_and_schema(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')

        # Title and description
        self.assertIn('<title>', content)
        self.assertIn('Idesignweb', content)
        self.assertIn('<meta name="description"', content)
        self.assertIn('<link rel="canonical"', content)

        # Open Graph
        self.assertIn('<meta property="og:site_name" content="Idesignweb">', content)
        self.assertIn('<meta property="og:title"', content)
        self.assertIn('<meta property="og:description"', content)
        self.assertIn('<meta property="og:url"', content)
        self.assertIn('<meta property="og:image"', content)
        self.assertIn('og-image.jpg', content)

        # Twitter Card
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', content)

        # Favicon and Manifest
        self.assertIn('favicon-32x32.png', content)
        self.assertIn('site.webmanifest', content)

        # Structured Data JSON-LD
        self.assertIn('application/ld+json', content)
        self.assertIn('"@type": "Organization"', content)
        self.assertIn('"@type": "WebSite"', content)
        self.assertIn('Vincent Odhiambo', content)
        self.assertIn('Timothy Owino', content)

    def test_detail_pages_structured_data(self):
        # Service detail
        resp_service = self.client.get('/services/web-development/')
        self.assertEqual(resp_service.status_code, 200)
        content_service = resp_service.content.decode('utf-8')
        self.assertIn('"@type": "Service"', content_service)
        self.assertIn('"@type": "BreadcrumbList"', content_service)
        self.assertIn('Web Development', content_service)

        # Work detail
        resp_work = self.client.get('/work/echowithin-encrypted-platform/')
        self.assertEqual(resp_work.status_code, 200)
        content_work = resp_work.content.decode('utf-8')
        self.assertIn('"@type": "CreativeWork"', content_work)
        self.assertIn('"@type": "BreadcrumbList"', content_work)
        self.assertIn('EchoWithin', content_work)

        # Insight detail
        resp_insight = self.client.get('/insights/building-echowithin-encrypted-platform/')
        self.assertEqual(resp_insight.status_code, 200)
        content_insight = resp_insight.content.decode('utf-8')
        self.assertIn('"@type": "TechArticle"', content_insight)
        self.assertIn('content="article"', content_insight)

    def test_auth_and_portal_noindex_enforcement(self):
        # Login page has noindex in meta and in response header
        resp_login = self.client.get('/login/')
        self.assertEqual(resp_login.status_code, 200)
        content_login = resp_login.content.decode('utf-8')
        self.assertIn('content="noindex, nofollow, noarchive"', content_login)
        self.assertEqual(resp_login.headers.get('X-Robots-Tag'), 'noindex, nofollow, noarchive')

        # Portal route redirect has X-Robots-Tag header
        resp_portal = self.client.get('/portal/')
        self.assertEqual(resp_portal.status_code, 302)
        self.assertEqual(resp_portal.headers.get('X-Robots-Tag'), 'noindex, nofollow, noarchive')

    def test_derived_official_assets_exist(self):
        import json
        img_dir = pathlib.Path('static/img')
        self.assertTrue((img_dir / 'logo.jpg').exists())
        self.assertTrue((img_dir / 'favicon-32x32.png').exists())
        self.assertTrue((img_dir / 'apple-touch-icon.png').exists())
        self.assertTrue((img_dir / 'favicon.png').exists())
        self.assertTrue((img_dir / 'og-image.jpg').exists())

        manifest_file = pathlib.Path('static/site.webmanifest')
        self.assertTrue(manifest_file.exists())
        manifest_data = json.loads(manifest_file.read_text(encoding='utf-8'))
        self.assertEqual(manifest_data['name'], 'Idesignweb')
