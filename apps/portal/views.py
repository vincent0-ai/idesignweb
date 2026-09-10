"""
Member Portal views for idesignweb.
Gated behind authentication, with noindex, nofollow headers applied by middleware.
Manages dashboard, communications, project spaces, asset library, and support tickets.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    announcements = list(db.announcements.find({}).sort('created_at', -1))
    return render(request, 'portal/communications.html', {
        'announcements': announcements,
        'active_section': 'communications'
    })

@login_required(login_url='/login/')
def projects_view(request):
    db = get_db()
    username = request.user.username
    query = {} if request.user.is_staff else {'client_username': username}
    projects = list(db.projects.find(query).sort('updated_at', -1))
    return render(request, 'portal/projects.html', {
        'projects': projects,
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

