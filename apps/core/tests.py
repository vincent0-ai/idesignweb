"""
Comprehensive test suite for idesignweb.
Verifies public pages, auth gating, noindex headers, deliverable approval, contact submission,
and strict adherence to flat design constraints (no gradients, no emoji, no icons, no em dashes).
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.core.db import get_db
import unicodedata
import pathlib
import re

class PublicZoneTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_public_pages_render_successfully(self):
        urls = [
            '/',
            '/services/',
            '/services/graphic-design/',
            '/services/video-editing/',
            '/services/web-development/',
            '/services/cybersecurity/',
            '/work/',
            '/work/nordic-furniture-brand-system/',
            '/about/',
            '/insights/',
            '/insights/principles-of-hairline-ui-design/',
            '/contact/',
            '/login/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f"Expected 200 for {url}, got {response.status_code}"
            )

    def test_contact_form_submission_stores_in_mongodb(self):
        db = get_db()
        initial_count = db.inquiries.count_documents({})
        
        post_data = {
            'full_name': 'Test Client',
            'email': 'test@client.com',
            'service_interest': 'Web Development',
            'budget_range': '25k - 50k',
            'message': 'Automated test inquiry regarding systems architecture.'
        }
        response = self.client.post('/contact/', post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        new_count = db.inquiries.count_documents({})
        self.assertEqual(new_count, initial_count + 1)
        
        # Verify inserted data
        inquiry = db.inquiries.find_one({'email': 'test@client.com'})
        self.assertIsNotNone(inquiry)
        self.assertEqual(inquiry['full_name'], 'Test Client')
        self.assertEqual(inquiry['service_interest'], 'Web Development')


class MemberPortalZoneTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Ensure test user exists in SQLite
        self.user, _ = User.objects.get_or_create(
            username='client_apex',
            defaults={'email': 'client@apex.com'}
        )
        self.user.set_password('MemberPass2026!')
        self.user.save()

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


class DesignConstraintsAuditTests(TestCase):
    def test_no_gradients_in_css(self):
        css_dir = pathlib.Path('static/css')
        gradient_pattern = re.compile(r'(linear-gradient|radial-gradient|conic-gradient)', re.IGNORECASE)
        for css_file in css_dir.glob('*.css'):
            content = css_file.read_text(encoding='utf-8')
            match = gradient_pattern.search(content)
            self.assertIsNone(match, f"Gradient found in {css_file}: {match}")

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

    def test_no_svg_icons_in_templates(self):
        svg_pattern = re.compile(r'<svg', re.IGNORECASE)
        for p in pathlib.Path('templates').rglob('*.html'):
            content = p.read_text(encoding='utf-8')
            match = svg_pattern.search(content)
            self.assertIsNone(match, f"SVG element found in {p}")
