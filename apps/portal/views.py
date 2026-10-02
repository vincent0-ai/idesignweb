"""
Member Portal views for idesignweb.
Gated behind authentication, with noindex, nofollow headers applied by middleware.
Manages dashboard, communications, project spaces, asset library, and support tickets.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404
from apps.core.db import get_db
import datetime

def login_view(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')

    next_url = request.GET.get('next', 'portal:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Authentication verified. Welcome to the member portal, {user.username}.')
            if next_url.startswith('/'):
                return redirect(next_url)
            return redirect('portal:dashboard')
        else:
            messages.error(request, 'Invalid credentials. Access denied.')

    return render(request, 'portal/login.html', {'next': next_url})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Session terminated. You have been logged out.')
    return redirect('public:home')

@login_required(login_url='/login/')
def dashboard_view(request):
    db = get_db()
    username = request.user.username
    is_staff = request.user.is_staff

    # Fetch client projects
    query = {} if is_staff else {'client_username': username}
    projects = list(db.projects.find(query).sort('updated_at', -1))

    # Calculate deliverable metrics
    total_deliverables = 0
    pending_review_count = 0
    for prj in projects:
        for deliv in prj.get('deliverables', []):
            total_deliverables += 1
            if deliv.get('status') == 'In Review':
                pending_review_count += 1

    # Fetch active announcements
    announcements = list(db.announcements.find({'active': True}).sort('created_at', -1).limit(3))

    # Fetch recent tickets
    ticket_query = {} if is_staff else {'client_username': username}
    tickets = list(db.tickets.find(ticket_query).sort('updated_at', -1).limit(3))

    context = {
        'projects': projects,
        'pending_review_count': pending_review_count,
        'total_deliverables': total_deliverables,
        'announcements': announcements,
        'tickets': tickets,
        'active_section': 'dashboard',
    }
    return render(request, 'portal/dashboard.html', context)

@login_required(login_url='/login/')
def communications_view(request):
    db = get_db()
    
    # Handle Staff Announcement Actions
    if request.method == 'POST' and request.user.is_staff:
        action = request.POST.get('action')
        now = datetime.datetime.now(datetime.timezone.utc)
        
        if action == 'create':
            title = request.POST.get('title', '').strip()
            body = request.POST.get('body', '').strip()
            priority = request.POST.get('priority', 'Notice').strip()
            
            if not title or not body:
                messages.error(request, 'Title and message body are required to publish an announcement.')
            else:
                ann_id = f'ANN-{int(datetime.datetime.now().timestamp())}'
                date_str = datetime.datetime.now().strftime('%b %d, %Y')
                db.announcements.insert_one({
                    'announcement_id': ann_id,
                    'title': title,
                    'body': body,
                    'priority': priority,
                    'active': True,
                    'author': request.user.username,
                    'created_at': now,
                    'date_str': date_str,
                })
                messages.success(request, f'Announcement "{title}" published to member portal.')
                return redirect('portal:communications')

        elif action == 'delete':
            ann_id = request.POST.get('announcement_id', '').strip()
            if ann_id:
                db.announcements.delete_one({'announcement_id': ann_id})
                messages.success(request, 'Announcement removed.')
                return redirect('portal:communications')

    announcements = list(db.announcements.find({}).sort('created_at', -1))
    return render(request, 'portal/communications.html', {
        'announcements': announcements,
        'active_section': 'communications'
    })

@login_required(login_url='/login/')
def projects_view(request):
    db = get_db()
    username = request.user.username

    # Handle Staff Project Creation
    if request.method == 'POST' and request.user.is_staff:
        action = request.POST.get('action')
        if action == 'create_project':
            client_username = request.POST.get('client_username', '').strip()
            title = request.POST.get('title', '').strip()
            service_category = request.POST.get('service_category', 'Web Development').strip()
            target_date = request.POST.get('target_date', 'Ongoing').strip()

            if not client_username or not title:
                messages.error(request, 'Client username and project title are required.')
            else:
                clean_code = client_username.replace('client_', '').upper()[:4]
                project_code = f"PRJ-{clean_code}-{int(datetime.datetime.now().timestamp()) % 1000}"
                now = datetime.datetime.now(datetime.timezone.utc)

                db.projects.insert_one({
                    'project_code': project_code,
                    'title': title,
                    'client_username': client_username,
                    'service_category': service_category,
                    'status': 'In Review',
                    'start_date': datetime.datetime.now().strftime('%b %Y'),
                    'target_date': target_date or 'Ongoing',
                    'progress_percent': 10,
                    'deliverables': [
                        {
                            'deliverable_id': 'DEL-01',
                            'title': 'Project Kickoff & Specification Review',
                            'status': 'In Review',
                            'preview_url': '',
                            'asset_type': 'Specification',
                            'client_notes': ''
                        }
                    ],
                    'created_at': now,
                    'updated_at': now
                })
                messages.success(request, f'Project space "{title}" ({project_code}) created for {client_username}.')
                return redirect('portal:project_detail', project_code=project_code)

    query = {} if request.user.is_staff else {'client_username': username}
    projects = list(db.projects.find(query).sort('updated_at', -1))
    
    client_users = []
    if request.user.is_staff:
        client_users = list(User.objects.filter(is_staff=False).order_by('username'))

    return render(request, 'portal/projects.html', {
        'projects': projects,
        'client_users': client_users,
        'active_section': 'projects'
    })

@login_required(login_url='/login/')
def project_detail_view(request, project_code):
    db = get_db()
    username = request.user.username
    query = {'project_code': project_code}
    if not request.user.is_staff:
        query['client_username'] = username

    project = db.projects.find_one(query)
    if not project:
        raise Http404('Project space not found')

    # Handle Staff Deliverable & Progress Updates
    if request.method == 'POST' and request.user.is_staff:
        action = request.POST.get('action')
        now = datetime.datetime.now(datetime.timezone.utc)

        if action == 'add_deliverable':
            title = request.POST.get('title', '').strip()
            asset_type = request.POST.get('asset_type', 'Deliverable').strip()
            preview_url = request.POST.get('preview_url', '').strip()

            if not title:
                messages.error(request, 'Deliverable title is required.')
            else:
                deliverables = project.get('deliverables', [])
                del_count = len(deliverables) + 1
                del_id = f"DEL-0{del_count}" if del_count < 10 else f"DEL-{del_count}"
                new_del = {
                    'deliverable_id': del_id,
                    'title': title,
                    'status': 'In Review',
                    'preview_url': preview_url,
                    'asset_type': asset_type,
                    'client_notes': ''
                }
                deliverables.append(new_del)
                db.projects.update_one(
                    {'_id': project['_id']},
                    {'$set': {'deliverables': deliverables, 'updated_at': now}}
                )
                messages.success(request, f'Deliverable "{title}" ({del_id}) added.')
                return redirect('portal:project_detail', project_code=project_code)

        elif action == 'update_project':
            status = request.POST.get('status', project.get('status', 'In Review'))
            try:
                progress = int(request.POST.get('progress_percent', project.get('progress_percent', 0)))
            except ValueError:
                progress = project.get('progress_percent', 0)
            target_date = request.POST.get('target_date', project.get('target_date', 'Ongoing'))

            db.projects.update_one(
                {'_id': project['_id']},
                {'$set': {
                    'status': status,
                    'progress_percent': min(100, max(0, progress)),
                    'target_date': target_date,
                    'updated_at': now
                }}
            )
            messages.success(request, 'Project progress and milestone status updated.')
            return redirect('portal:project_detail', project_code=project_code)

    return render(request, 'portal/project_detail.html', {
        'project': project,
        'active_section': 'projects'
    })

@login_required(login_url='/login/')
def deliverable_action_view(request, project_code, deliverable_id):
    if request.method != 'POST':
        return redirect('portal:project_detail', project_code=project_code)

    action = request.POST.get('action') # 'approve' or 'revise'
    notes = request.POST.get('client_notes', '').strip()
    new_status = 'Approved' if action == 'approve' else 'Revision Requested'

    db = get_db()
    username = request.user.username
    query = {'project_code': project_code}
    if not request.user.is_staff:
        query['client_username'] = username

    project = db.projects.find_one(query)
    if not project:
        raise Http404('Project space not found')

    # Update the specific deliverable
    deliverables = project.get('deliverables', [])
    updated = False
    for d in deliverables:
        if d.get('deliverable_id') == deliverable_id:
            d['status'] = new_status
            if notes:
                d['client_notes'] = notes
            updated = True
            break

    if updated:
        db.projects.update_one(
            {'_id': project['_id']},
            {'$set': {'deliverables': deliverables, 'updated_at': datetime.datetime.now(datetime.timezone.utc)}}
        )
        messages.success(request, f'Deliverable {deliverable_id} status updated to {new_status}.')
    else:
        messages.error(request, f'Deliverable {deliverable_id} not found in project.')

    return redirect('portal:project_detail', project_code=project_code)

@login_required(login_url='/login/')
def asset_library_view(request):
    db = get_db()
    username = request.user.username
    category_filter = request.GET.get('category', 'all')

    query = {} if request.user.is_staff else {'client_username': username}
    if category_filter != 'all':
        query['category'] = category_filter

    assets = list(db.assets.find(query).sort('updated_date', -1))
    categories = ['Identity', 'Design Tokens', 'Video Assets', 'Security Audit']

    return render(request, 'portal/assets.html', {
        'assets': assets,
        'categories': categories,
        'selected_category': category_filter,
        'active_section': 'assets'
    })

@login_required(login_url='/login/')
def tickets_view(request):
    db = get_db()
    username = request.user.username
    query = {} if request.user.is_staff else {'client_username': username}
    tickets = list(db.tickets.find(query).sort('updated_at', -1))

    return render(request, 'portal/tickets.html', {
        'tickets': tickets,
        'active_section': 'support'
    })

@login_required(login_url='/login/')
def ticket_detail_view(request, ticket_id):
    db = get_db()
    username = request.user.username
    query = {'ticket_id': ticket_id}
    if not request.user.is_staff:
        query['client_username'] = username

    ticket = db.tickets.find_one(query)
    if not ticket:
        raise Http404('Ticket not found')

    if request.method == 'POST':
        reply_text = request.POST.get('reply_text', '').strip()
        status_update = request.POST.get('status', '').strip()

        update_fields = {'updated_at': datetime.datetime.now(datetime.timezone.utc)}
        if request.user.is_staff and status_update in ['Open', 'In Progress', 'Resolved']:
            update_fields['status'] = status_update

        update_ops = {'$set': update_fields}
        if reply_text:
            new_msg = {
                'sender': username,
                'role': 'staff' if request.user.is_staff else 'client',
                'text': reply_text,
                'date_str': datetime.datetime.now().strftime('%b %d, %Y at %I:%M %p')
            }
            update_ops['$push'] = {'messages': new_msg}

        db.tickets.update_one({'_id': ticket['_id']}, update_ops)
        messages.success(request, 'Support ticket updated.')
        return redirect('portal:ticket_detail', ticket_id=ticket_id)

    return render(request, 'portal/ticket_detail.html', {
        'ticket': ticket,
        'active_section': 'support'
    })

@login_required(login_url='/login/')
def create_ticket_view(request):
    db = get_db()
    username = request.user.username

    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        priority = request.POST.get('priority', 'Medium')
        message = request.POST.get('message', '').strip()

        if not subject or not message:
            messages.error(request, 'Subject and message are required.')
        else:
            ticket_count = db.tickets.count_documents({}) + 1001
            new_ticket_id = f'TCK-{ticket_count}'
            now = datetime.datetime.now(datetime.timezone.utc)
            date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

            ticket_doc = {
                'ticket_id': new_ticket_id,
                'client_username': username,
                'subject': subject,
                'priority': priority,
                'status': 'Open',
                'created_at': now,
                'updated_at': now,
                'messages': [
                    {
                        'sender': username,
                        'role': 'client',
                        'text': message,
                        'date_str': date_str
                    }
                ]
            }
            db.tickets.insert_one(ticket_doc)
            messages.success(request, f'Support ticket {new_ticket_id} created.')
            return redirect('portal:ticket_detail', ticket_id=new_ticket_id)

    return render(request, 'portal/create_ticket.html', {'active_section': 'support'})

@login_required(login_url='/login/')
def inquiries_view(request):
    if not request.user.is_staff:
        raise Http404('Access restricted to staff members.')
    db = get_db()
    inquiries = list(db.inquiries.find({}).sort('submitted_at', -1))
    return render(request, 'portal/inquiries.html', {
        'inquiries': inquiries,
        'active_section': 'inquiries'
    })

@login_required(login_url='/login/')
def clients_view(request):
    """
    Staff-only Client Account Management View.
    Allows administrators to:
    1. View all client accounts, their linked project spaces, and status.
    2. Provision new client accounts with credentials and optional auto-created project space.
    3. Activate, deactivate, or reset passwords for client accounts.
    """
    if not request.user.is_staff:
        raise Http404('Access restricted to staff administrators.')

    db = get_db()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_client':
            username = request.POST.get('username', '').strip().lower()
            company_name = request.POST.get('company_name', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            project_title = request.POST.get('project_title', '').strip()
            service_category = request.POST.get('service_category', 'Web Development').strip()

            if not username or not password or not email or not company_name:
                messages.error(request, 'Username, company/client name, email, and password are all required.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, f'Username "{username}" is already taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, f'An account with email "{email}" already exists.')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=company_name,
                    is_staff=False
                )

                # Provision an initial project space if title was provided
                if project_title:
                    clean_code = username.replace('client_', '').upper()[:4]
                    project_code = f"PRJ-{clean_code}-{int(datetime.datetime.now().timestamp()) % 1000}"
                    now = datetime.datetime.now(datetime.timezone.utc)
                    db.projects.insert_one({
                        'project_code': project_code,
                        'title': project_title,
                        'client_username': username,
                        'service_category': service_category,
                        'status': 'In Review',
                        'start_date': datetime.datetime.now().strftime('%b %Y'),
                        'target_date': 'Ongoing',
                        'progress_percent': 10,
                        'deliverables': [
                            {
                                'deliverable_id': 'DEL-01',
                                'title': 'Project Onboarding & Requirements Specification',
                                'status': 'In Review',
                                'preview_url': '',
                                'asset_type': 'Specification',
                                'client_notes': ''
                            }
                        ],
                        'created_at': now,
                        'updated_at': now
                    })

                messages.success(
                    request,
                    f'Client account for "{company_name}" ({username}) created successfully! '
                    f'The client can now log in at /login/ using password: {password}'
                )
                return redirect('portal:clients')

        elif action == 'toggle_status':
            target_username = request.POST.get('target_username', '').strip()
            target_user = User.objects.filter(username=target_username, is_staff=False).first()
            if target_user:
                target_user.is_active = not target_user.is_active
                target_user.save()
                state = 'activated' if target_user.is_active else 'deactivated'
                messages.success(request, f'Client account "{target_username}" has been {state}.')
                return redirect('portal:clients')

        elif action == 'reset_password':
            target_username = request.POST.get('target_username', '').strip()
            new_password = request.POST.get('new_password', '').strip()
            if not new_password:
                messages.error(request, 'A new password is required.')
            else:
                target_user = User.objects.filter(username=target_username, is_staff=False).first()
                if target_user:
                    target_user.set_password(new_password)
                    target_user.save()
                    messages.success(request, f'Password for "{target_username}" updated to: {new_password}')
                    return redirect('portal:clients')

    # GET request - load clients
    clients = list(User.objects.filter(is_staff=False).order_by('-date_joined'))
    for c in clients:
        c.project_count = db.projects.count_documents({'client_username': c.username})
        c.ticket_count = db.tickets.count_documents({'client_username': c.username})

    # Support prefilling from contact inquiry conversion
    prefill = {
        'company_name': request.GET.get('name', ''),
        'email': request.GET.get('email', ''),
        'service_category': request.GET.get('service', 'Web Development'),
    }
    if prefill['email']:
        raw_prefix = prefill['email'].split('@')[0].lower()
        suggested = ''.join(c for c in raw_prefix if c.isalnum() or c == '_')
        prefill['username'] = f'client_{suggested}'
    else:
        prefill['username'] = ''

    return render(request, 'portal/clients.html', {
        'clients': clients,
        'prefill': prefill,
        'active_section': 'clients'
    })


