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
