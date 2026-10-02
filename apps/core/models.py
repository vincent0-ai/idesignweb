from django.db import models

class Work(models.Model):
    """
    Client work projects displayed in the public Work gallery and Featured Work section.
    Simple, minimalist schema fully manageable via Django Admin.
    """
    title = models.CharField(max_length=200, help_text="Short project title, e.g. EchoWithin")
    full_title = models.CharField(
        max_length=250, 
        blank=True, 
        help_text="Editorial title, e.g. EchoWithin - Private Encrypted Notes & Social Bonds Platform"
    )
    slug = models.SlugField(max_length=200, unique=True, help_text="Unique URL identifier (e.g. echowithin-encrypted-platform)")
    client = models.CharField(max_length=150, help_text="Client name, e.g. EchoWithin or VIN-KJ Auto Services")
    category = models.CharField(
        max_length=100, 
        default='Web Development',
        choices=[
            ('Web Development', 'Web Development'),
            ('E-Commerce', 'E-Commerce'),
            ('Cybersecurity', 'Cybersecurity'),
            ('Graphic Design', 'Graphic Design'),
            ('Video Editing', 'Video Editing'),
        ]
    )
    year = models.CharField(max_length=10, default='2026')
    live_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Direct link to client live website (e.g. https://echowithin.xyz or https://vinkj.com)"
    )
    image_url = models.CharField(
        max_length=300, 
        default='img/echowithin-platform.webp',
        help_text="Static image path (e.g. img/echowithin-platform.webp) or full external URL"
    )
    summary = models.TextField(help_text="Short teaser description shown on cards")
    challenge = models.TextField(blank=True, help_text="The client challenge")
    solution = models.TextField(blank=True, help_text="The technical solution delivered")
    deliverables_summary = models.TextField(blank=True, help_text="Summary of completed deliverables")
    
    is_featured = models.BooleanField(default=True, help_text="Show on homepage under Featured Work")
    is_published = models.BooleanField(default=True, help_text="Show publicly on the website")
    sort_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = 'Work Project'
        verbose_name_plural = 'Work Projects'

    def __str__(self):
        return f"{self.title} ({self.client})"

    @property
    def display_title(self):
        return self.full_title if self.full_title else self.title


class Inquiry(models.Model):
    """
    Prospective client inquiries submitted through the public contact form.
    Reviewable and manageable via Django Admin.
    """
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    service_interest = models.CharField(max_length=150, default='General Inquiry')
    budget_range = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    status = models.CharField(
        max_length=50, 
        default='New',
        choices=[
            ('New', 'New'), 
            ('In Review', 'In Review'), 
            ('Contacted', 'Contacted'), 
            ('Closed', 'Closed')
        ]
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'

    def __str__(self):
        return f"{self.full_name} ({self.service_interest}) - {self.submitted_at.strftime('%Y-%m-%d')}"


class Article(models.Model):
    """
    Editorial essays, technical case reflections, and studio insights.
    Easily created, updated, and managed via Django Admin.
    """
    title = models.CharField(max_length=250, help_text="Article title")
    slug = models.SlugField(max_length=250, unique=True, help_text="URL slug (e.g. building-echowithin-platform)")
    category = models.CharField(
        max_length=100, 
        default='Engineering & Architecture',
        choices=[
            ('Engineering & Architecture', 'Engineering & Architecture'),
            ('Web Development', 'Web Development'),
            ('Cybersecurity', 'Cybersecurity'),
            ('Design Systems', 'Design Systems'),
            ('Studio Notes', 'Studio Notes'),
        ]
    )
    author = models.CharField(max_length=150, default='Vincent Odhiambo & Timothy Owino')
    reading_time = models.CharField(max_length=50, default='4 min read')
    summary = models.TextField(help_text="Introductory summary / lead excerpt shown on card feeds")
    content = models.TextField(help_text="Complete article body. Supports clean multi-line paragraphs and section headers (### Header).")
    is_published = models.BooleanField(default=True, help_text="Display publicly on the website")
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

    @property
    def excerpt(self):
        return self.summary

    @property
    def rendered_content(self):
        import html
        import re
        if not self.content:
            return ""
        
        blocks = re.split(r'\n\s*\n', self.content.strip())
        html_blocks = []
        
        for block in blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            if not lines:
                continue
            first = lines[0]
            
            if first.startswith('### '):
                heading_text = html.escape(first[4:])
                html_blocks.append(f'<h3 style="font-size: 1.35rem; font-weight: 700; margin-top: var(--space-2xl); margin-bottom: var(--space-sm); color: var(--text-main); line-height: 1.3;">{heading_text}</h3>')
            elif first.startswith('## '):
                heading_text = html.escape(first[3:])
                html_blocks.append(f'<h2 style="font-size: 1.6rem; font-weight: 700; margin-top: var(--space-2xl); margin-bottom: var(--space-sm); color: var(--text-main); line-height: 1.3;">{heading_text}</h2>')
            elif all(line.startswith('- ') or line.startswith('* ') for line in lines):
                items = []
                for line in lines:
                    item_text = html.escape(line[2:])
                    item_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_text)
                    items.append(f'<li style="margin-bottom: 6px;">{item_text}</li>')
                html_blocks.append(f'<ul style="padding-left: 24px; margin-bottom: var(--space-lg); line-height: 1.75; color: var(--text-body);">{"".join(items)}</ul>')
            else:
                para_text = '<br>'.join(html.escape(line) for line in lines)
                para_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', para_text)
                html_blocks.append(f'<p style="margin-bottom: var(--space-lg); line-height: 1.8; color: var(--text-body);">{para_text}</p>')
                
        return '\n'.join(html_blocks)
