# idesignweb Discovery Document

Date: 2026-09-10
Status: Pending Confirmation

---

## 1. Repo State

- Workspace Path: `c:\Users\DevTech\Desktop\Projects\idesignweb`
- Repository Status: Clean, fresh directory. No existing files, git repository, or pre-existing code.
- Environment and System Capabilities:
  - Operating System: Windows
  - Python Runtime: Python 3.13.13
  - Storage Service: MongoDB Server (Service name: `MongoDB`) is installed and currently running on `127.0.0.1:27017`. Verified via socket probe.
  - Python Packages: Global environment has `pymongo` 4.15.4 available. Django is not yet installed globally.
- Dependency Isolation Strategy:
  - As per dependency management standards, we will use a dedicated virtual environment (`.venv`) inside the project directory with `pip` and a version-locked `requirements.txt`.
  - No frontend package manager or Node.js toolchain is needed.

---

## 2. Stack and Architectural Analysis

### Frontend Architecture
- Core Technologies: Semantic HTML5, pure CSS3, vanilla JavaScript (ES6+).
- Frameworks: None. No React, Vue, Tailwind, Bootstrap, or other CSS/JS libraries.
- Iconography and Visual Assets:
  - Zero icon fonts (no FontAwesome, no Material Icons).
  - Zero SVG icon packages.
  - Visual navigation and indicators rely strictly on typographic scale, weights (Regular and Bold), tabular numerals (e.g. `01`, `02`), and hairline borders.
- Styling Constraints (Strict Enforcement):
  - Zero gradients anywhere in backgrounds, buttons, borders, or text.
  - Zero emoji anywhere in UI copy, markup, or code comments.
  - Zero em dashes anywhere in UI copy, placeholder text, or generated content.
  - Flat surfaces only: solid fills, hairline borders (0.5px to 1px), zero drop shadows except functional browser focus states.
  - Accent Color: Single accent color used exclusively for primary Call-To-Action (CTA) elements.
- JavaScript Organization:
  - A shared core script (`static/js/main.js`) loaded across all pages for global accessibility, mobile navigation toggle, modal dialog focus management, and notification dismissals.
  - Modular, targeted page scripts (e.g., `static/js/portal.js` for member portal interactions such as ticket filtering, deliverable approval triggers, and asset search).
  - No build step or bundler. Vanilla browser-native execution.

### Backend Architecture (Django + MongoDB Bridge)
Django's built-in ORM is architected around SQL relational databases. Bridging Django with MongoDB offers three primary architectural avenues:

#### Option A: Djongo
- How it works: A SQL-to-MongoDB query compiler that plugs into Django ORM backend settings.
- Advantages: In theory, allows standard Django models and migrations to translate to MongoDB.
- Tradeoffs and Risks:
  - Severely outdated and incompatible with modern Django (versions 4.x and 5.x) and Python 3.11+.
  - Highly prone to crashes during schema migrations, introspection, and complex queries.
  - Verdict: Not recommended.

#### Option B: MongoEngine
- How it works: A standalone Python Object-Document Mapper (ODM) for MongoDB.
- Advantages: Provides declarative Document schemas and validation.
- Tradeoffs and Risks:
  - Does not integrate with Django's native authentication, sessions, or admin without `django-mongoengine`, which is unmaintained and incompatible with modern Django releases.
  - Adds another abstraction layer over MongoDB.
  - Verdict: Adds complexity without standard Django compatibility.

#### Option C: PyMongo Direct Repository Layer (Recommended)
- How it works:
  - Leverage official `pymongo` with a clean, centralized database connection and repository service layer (e.g., `apps/core/db.py`).
  - Native MongoDB operations with zero ORM overhead, full support for Python 3.13, and total query flexibility (aggregation pipelines, indexing, nested document structures).
- Bridging Approaches for Auth and Sessions:
  - **Sub-option C1 (Hybrid Engine):**
    - SQLite side-store handles Django internal requirements: `django.contrib.auth`, `django.contrib.sessions`, and `django.contrib.admin`.
    - All business logic, public marketing content, member portal projects, announcements, assets, and tickets reside in MongoDB collections via PyMongo.
    - Advantages: Standard Django Admin works out-of-the-box for staff/user administration. Django session security and password hashing are native. Clean separation of concerns.
  - **Sub-option C2 (Pure MongoDB Engine):**
    - Pure MongoDB storage for everything.
    - Custom authentication and session management implemented via PyMongo and Django custom session backend (`SessionBase` storing session documents in MongoDB `sessions` collection).
    - Password hashing handled securely using `django.contrib.auth.hashers`.
    - Advantages: Single database engine across the entire stack.
    - Disadvantage: Standard Django Admin cannot inspect non-relational tables without custom dashboard views.
- Proposal: We propose Sub-option C1 for production stability and rapid staff administration, or Sub-option C2 if a single database engine (pure MongoDB) is strictly required by the user.

---

## 3. Auth and Zone Requirements

### Public Marketing Zone
- Access: Unrestricted, open to public visitors.
- Indexing: Fully indexable with canonical tags, meta descriptions, and sitemap.
- Pages:
  1. Home (`/`): Full-bleed hero, 3-stat metric row, 01-04 numbered service cards grid, process section, primary CTA.
  2. Services Hub (`/services/`): Overview of capabilities with links to individual service practices.
  3. Service Detail - Graphic Design (`/services/graphic-design/`): Posters, brand identity, editorial design, typography systems.
  4. Service Detail - Video Editing (`/services/video-editing/`): Post-production, motion graphics, narrative cuts, color grading.
  5. Service Detail - Web Development (`/services/web-development/`): Modern websites, web applications, performance, clean architectures.
  6. Service Detail - Cybersecurity (`/services/cybersecurity/`): Vulnerability assessment, penetration testing, compliance, hardening.
  7. Work / Case Studies (`/work/`): Portfolio grid, client projects, problem-solution-result format.
  8. Case Study Detail (`/work/<slug>/`): In-depth deliverable metrics and client impact.
  9. About (`/about/`): Company background, team philosophy, operational standards.
  10. Insights / Blog (`/insights/`): Editorial articles, technical writeups, industry observations.
  11. Insight Detail (`/insights/<slug>/`): Longform reading layout.
  12. Contact (`/contact/`): Structured inquiry form (writes to MongoDB `inquiries` collection).
  13. Login (`/login/`): Authentication entry point to member zone.

### Member Portal Zone
- Access: Strict authentication required. Unauthenticated requests redirect to `/login/` with `next` parameter.
- Robots and Privacy Directive: Every member portal response includes headers and meta tag `<meta name="robots" content="noindex, nofollow">`.
- Gated Sections:
  1. Dashboard (`/portal/`): Summary metrics, active projects count, unread announcements, recent deliverables.
  2. Communications / Announcements (`/portal/communications/`): Firm announcements, release notes, scheduled maintenance bulletins.
  3. Project Spaces (`/portal/projects/` and `/portal/projects/<project_id>/`):
     - Deliverables list with status tags (Draft, In Review, Approved, Revision Requested).
     - Interactive approval workflow (client can approve or request revisions with feedback).
  4. Asset Library (`/portal/assets/`): Searchable directory of client brand assets, source files, exports, and design guidelines.
  5. Support / Tickets (`/portal/support/` and `/portal/support/new/`): Issue submission, priority selector, status tracker, comment history.
  6. Logout (`/logout/`): Secure session invalidation and redirect to public homepage.

---

## 4. Content Model and MongoDB Collections

### Dynamic vs. Static Classification
- **Static Content**:
  - Site layout, navigation items, footer legal statements, design system tokens, company core philosophy.
- **Dynamic Content (Stored in MongoDB)**:
  - Services catalog and service details.
  - Case studies and portfolio records.
  - Insights / blog articles.
  - Member announcements.
  - Client project spaces, milestones, and deliverables.
  - Digital asset library metadata.
  - Support tickets and status logs.
  - Public contact inquiries.

### MongoDB Collections Schema

#### 1. `services`
```json
{
  "_id": "ObjectId",
  "slug": "graphic-design",
  "service_number": "01",
  "title": "Graphic Design",
  "tagline": "Visual identities and typographic systems for digital and physical media.",
  "overview": "Detailed practice overview...",
  "deliverables": [
    "Brand identity and logo systems",
    "Typographic guidelines and design tokens",
    "Editorial layouts and poster series",
    "Digital design assets"
  ],
  "process_steps": [
    { "step_number": "01", "title": "Research and Analysis", "description": "Auditing category landscape..." },
    { "step_number": "02", "title": "Concept Generation", "description": "Formulating visual directions..." },
    { "step_number": "03", "title": "Refinement and Delivery", "description": "Final vector production and guidelines..." }
  ],
  "featured": true,
  "sort_order": 1,
  "updated_at": "ISODate"
}
```

#### 2. `case_studies`
```json
{
  "_id": "ObjectId",
  "slug": "nordic-furniture-identity",
  "title": "Nordic Furniture Visual Identity",
  "client": "Klar Form",
  "category": "Graphic Design",
  "year": "2026",
  "summary": "Complete brand identity and packaging system for an architectural furniture manufacturer.",
  "challenge": "Client required a unified visual language without decorative excess.",
  "solution": "Developed a modular typographic hierarchy and strict monochrome packaging system.",
  "results": [
    { "metric": "+42%", "label": "Direct retail inquiries" },
    { "metric": "100%", "label": "Packaging material standardization" }
  ],
  "deliverables_summary": "Brand manual, packaging templates, exhibition posters.",
  "published_at": "ISODate",
  "is_published": true
}
```

#### 3. `posts` (Insights / Blog)
```json
{
  "_id": "ObjectId",
  "slug": "principles-of-hairline-ui-design",
  "title": "Principles of Hairline Interface Design",
  "excerpt": "Why removing decorative shadows and gradients produces faster, more authoritative interfaces.",
  "content": "Full article body in markdown or clean HTML...",
  "author": "idesignweb Editorial",
  "reading_time": "5 min read",
  "category": "Design Systems",
  "published_at": "ISODate",
  "is_published": true
}
```

#### 4. `announcements` (Member Portal)
```json
{
  "_id": "ObjectId",
  "title": "Scheduled Infrastructure Upgrade",
  "body": "System maintenance scheduled for Sunday at 02:00 UTC. No service interruption expected for active deliverables.",
  "priority": "normal",
  "audience": "all",
  "created_at": "ISODate",
  "active": true
}
```

#### 5. `projects` (Member Portal)
```json
{
  "_id": "ObjectId",
  "project_code": "PRJ-2026-001",
  "client_username": "client_apex",
  "title": "E-Commerce Core Web Architecture",
  "service_category": "Web Development",
  "status": "In Progress",
  "progress_percent": 65,
  "start_date": "2026-08-01",
  "target_date": "2026-10-15",
  "deliverables": [
    {
      "deliverable_id": "DEL-01",
      "title": "Information Architecture and Sitemap",
      "version": "1.0",
      "status": "Approved",
      "due_date": "2026-08-20",
      "file_url": "/static/uploads/deliverables/del_01_ia.pdf",
      "client_notes": "Approved without modifications."
    },
    {
      "deliverable_id": "DEL-02",
      "title": "Frontend Template Architecture",
      "version": "2.1",
      "status": "In Review",
      "due_date": "2026-09-15",
      "file_url": "/static/uploads/deliverables/del_02_templates.zip",
      "client_notes": ""
    }
  ],
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

#### 6. `assets` (Member Portal Library)
```json
{
  "_id": "ObjectId",
  "client_username": "client_apex",
  "asset_name": "Primary Wordmark Vector",
  "asset_category": "Logos",
  "file_format": "SVG / PDF",
  "file_size": "1.2 MB",
  "file_url": "/static/uploads/assets/wordmark_vector.zip",
  "version": "1.0",
  "uploaded_at": "ISODate"
}
```

#### 7. `tickets` (Member Portal Support)
```json
{
  "_id": "ObjectId",
  "ticket_id": "TCK-1048",
  "client_username": "client_apex",
  "subject": "Asset Export Request for Q4 Print Run",
  "priority": "High",
  "status": "Open",
  "messages": [
    {
      "sender": "client_apex",
      "role": "client",
      "message": "We need the high-resolution vector exports for the autumn poster campaign.",
      "timestamp": "ISODate"
    },
    {
      "sender": "team",
      "role": "staff",
      "message": "Generating the print-ready CMYK PDF assets now. Will upload to Asset Library by 14:00.",
      "timestamp": "ISODate"
    }
  ],
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

#### 8. `inquiries` (Public Contact Form)
```json
{
  "_id": "ObjectId",
  "full_name": "Marcus Vance",
  "email": "marcus@example.com",
  "service_interest": "Web Development",
  "budget_range": "10k-25k",
  "message": "Inquiry regarding architectural overhaul of existing platform.",
  "status": "New",
  "submitted_at": "ISODate"
}
```

---

## 5. Next Steps Upon Confirmation

Once this discovery document is reviewed and confirmed:
1. Initialize virtual environment and lock dependencies (`Django`, `pymongo`, `python-dotenv`).
2. Establish clean Django project layout (`config/`, `apps/core/`, `apps/public/`, `apps/portal/`).
3. Build shared template component shell (base HTML, typography scale, hairline card primitives, header/footer navigation).
4. Implement MongoDB connection module with seeding script for initial services, case studies, insights, and demo member portal data.
5. Construct public zone pages followed by member portal zone with strict `noindex` headers.
6. Verify design constraints at every step (no gradients, no emoji, no icons, no em dashes, flat hairline surfaces).
