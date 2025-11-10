from django.shortcuts import render, redirect,get_object_or_404
from datetime import datetime, date
import pandas as pd
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.cache import cache_control,never_cache
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from openpyxl.styles import NamedStyle
from django.contrib import messages
import xlwt
from itertools import chain
from collections import defaultdict
from django.db.models import Sum,F,Q, Prefetch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
from openpyxl import Workbook
from openpyxl.styles import Alignment
from django.utils.timezone import now, localtime
from django.core.mail import send_mail
from django.conf import settings
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
import os
from django.utils.dateparse import parse_date

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # ❌ Prevent login until admin approval
            user.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'logins/register.html', {'form': form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'logins/login.html', {'form': form})

@login_required
def approve_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    user.is_approved = True  
    user.is_active = True  
    user.save()

    return redirect('admin_dashboard')

@login_required
def reject_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    user.delete()  
    return redirect('admin_dashboard')

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.error(request, f"User {user.username} has been deleted.")
    return redirect('admin_dashboard')

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        password_form = UserPasswordEditForm(user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            return redirect('admin_dashboard')  
    else:
        user_form = UserEditForm(instance=user)
        password_form = UserPasswordEditForm(user)

    return render(request, 'logins/edit_user.html', {
        'user_form': user_form,
        'password_form': password_form,
        'user': user
    })

@login_required(login_url='login') 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if request.user.is_superuser:   
        # login_time = localtime(now()).strftime('%Y-%m-%d %I:%M:%S %p')        
        # send_mail(
        #     subject='Superuser Login Notification',
        #     message=f"Superuser {request.user.username} logged in at {login_time}.",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=['abtechchennai@gmail.com'],  
        #     fail_silently=False,
        # )
        return redirect('admin_dashboard')      
    context = {
        'branch': request.user.branch,
        'department': request.user.department
    }    
    if request.user.department == 'ADMIN-MANAGEMENT WORK TEAM':
        template_name = f"logins/incharge_dashboard_{request.user.branch.lower()}.html"
    else:
        template_name = f"logins/employee_dashboard_{request.user.branch.lower()}.html"

    return render(request, template_name, context)
def user_logout(request):
    logout(request)
    return redirect('login')

def admin_dashboard(request):
    user_registrations = User.objects.all().order_by('username')
    BRANCHES = ['NAGERCOIL']
    work_status_records = WorkStatus.objects.all()
    DEPARTMENT_CHOICES = [
    
    'hardware project development team',
    
    'Admin team',
]
    context = {
        'user_registrations': user_registrations,
        'departments': DEPARTMENT_CHOICES,
        'branches': BRANCHES,
    }
    return render(request, 'logins/admin_dashboard.html', context)

@login_required(login_url='login')
def workstatus_branch_list(request):
    branches = ['NAGERCOIL']
    return render(request, 'workstatus/branch_list.html', {'branches': branches})
@login_required(login_url='login')
def workstatus_department_list(request, branch):
    user = request.user

    all_departments = [
        # 'JOURNAL TEAM',
        # 'RESEARCH WORK DEVELOPMENT TEAM',
        # 'SOFTWARE PROJECT DEVELOPMENT TEAM',
        'HARDWARE PROJECT DEVELOPMENT TEAM',
        # 'TECHNICAL TEAM',
        'ADMIN TEAM',
    ]

    if user.is_superuser:
        # ✅ Superuser sees all departments
        departments = all_departments

    elif getattr(user, "is_team_leader", False):
        # ✅ Team Leader sees only their own department
        departments = [user.department]

    else:
        # ✅ Employees have no access here
        return redirect("dashboard")

    return render(request, "workstatus/department_list.html", {
        "branch": branch,
        "departments": departments,
    })
@login_required(login_url='login')
def workstatus_records_view(request, branch, department):
    query = request.GET.get('q', '')
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')

    groups = WorkStatusGroup.objects.filter(
        branch=branch,
        department=department
    ).prefetch_related('statuses').select_related('user')

    # Search filter
    if query:
        groups = groups.filter(
            Q(user__username__icontains=query) |
            Q(statuses__WORK_CODE__icontains=query) |
            Q(S_NO__icontains=query)
        ).distinct()

    # Date range filter
    if from_date and to_date:
        parsed_from_date = parse_date(from_date)
        parsed_to_date = parse_date(to_date)
        if parsed_from_date and parsed_to_date:
            groups = groups.filter(DATE__range=[parsed_from_date, parsed_to_date])

    elif from_date:  # Only from_date provided
        parsed_from_date = parse_date(from_date)
        if parsed_from_date:
            groups = groups.filter(DATE__gte=parsed_from_date)

    elif to_date:  # Only to_date provided
        parsed_to_date = parse_date(to_date)
        if parsed_to_date:
            groups = groups.filter(DATE__lte=parsed_to_date)

    groups = groups.order_by('DATE', 'user__username')

    return render(request, 'workstatus/workstatus_records.html', {
        'branch': branch,
        'department': department,
        'groups': groups,
        'from_date': from_date,
        'to_date': to_date,
        'query': query,
    })


# EMPLOYEE DASHBOARD VIEWS
@login_required
def work_status_group_list(request):
    groups = WorkStatusGroup.objects.filter(user=request.user).prefetch_related('statuses').order_by('-DATE')
    
    current_year = datetime.now().year
    years = [year for year in range(current_year, current_year - 10, -1)]

    return render(request, 'workstatus/work_status_group_list.html', {
        'groups': groups,
        'years': years,
    })

@login_required
def create_work_status_group(request):
    if request.method == 'POST':
        form = WorkStatusGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.branch = request.user.branch
            group.department = request.user.department
            group.save()
            return redirect('work_status_group_list')
    else:
        form = WorkStatusGroupForm()

    return render(request, 'workstatus/add_edit_work_status_group.html', {
        'form': form,
        'action': 'Add'
    })

@login_required
def edit_work_status_group(request, group_id):
    group = get_object_or_404(WorkStatusGroup, id=group_id)

    if request.method == 'POST':
        form = WorkStatusGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('work_status_group_list')
    else:
        form = WorkStatusGroupForm(instance=group)

    return render(request, 'workstatus/add_edit_work_status_group.html', {
        'form': form,
        'action': 'Edit'
    })

@login_required
def delete_work_status_group(request, group_id):
    group = get_object_or_404(WorkStatusGroup, id=group_id)
    group.delete()
    return redirect('work_status_group_list')

@login_required
def add_work_status(request, group_id):
    group = get_object_or_404(WorkStatusGroup, id=group_id)

    if request.method == 'POST':
        form = WorkStatusForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.group = group

            # Replace blank date fields with '-'
            if not status.STARTING_DATE:
                status.STARTING_DATE = None
            if not status.ENDING_DATE:
                status.ENDING_DATE = None

            status.save()
            return redirect('work_status_group_list')
    else:
        form = WorkStatusForm()

    return render(request, 'workstatus/add_edit_work_status.html', {
        'form': form,
        'group': group,
        'action': 'Add'
    })

@login_required
def edit_work_status(request, status_id):
    status = get_object_or_404(WorkStatus, id=status_id)
    group = status.group

    if request.method == 'POST':
        form = WorkStatusForm(request.POST, instance=status)
        if form.is_valid():
            status = form.save(commit=False)
            status.group = group
            # Replace blank date fields with '-'
            if not status.STARTING_DATE:
                status.STARTING_DATE = None
            if not status.ENDING_DATE:
                status.ENDING_DATE = None

            status.save()
            return redirect('work_status_group_list')
    else:
        form = WorkStatusForm(instance=status)

    return render(request, 'workstatus/add_edit_work_status.html', {
        'form': form,
        'group': group,
        'action': 'Edit'
    })


@login_required
def delete_work_status(request, status_id):
    status = get_object_or_404(WorkStatus, id=status_id)
    status.delete()
    return redirect('work_status_group_list')


@login_required
def download_work_status_report(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    groups = WorkStatusGroup.objects.filter(user=request.user).prefetch_related('statuses')
    if month and year:
        groups = groups.filter(DATE__year=year, DATE__month=month)
    groups = groups.order_by('DATE')

    if not groups.exists():
        return HttpResponse("No records found.", status=404)

    wb = Workbook()
    ws = wb.active
    ws.title = "Work Status Report"

    thin = Side(border_style="thin", color="000000")
    border = Border(top=thin, left=thin, right=thin, bottom=thin)
    data_font = Font(name="Bookman Old Style")
    ws.row_dimensions[1].height = 60
    ws.row_dimensions[2].height = 30
    logo_path = os.path.join(settings.BASE_DIR, "static", "images", "logo.png")
    if os.path.exists(logo_path):
        logo = XLImage(logo_path)
        logo.width, logo.height = 90, 50
        ws.add_image(logo, "A1")

    ws.merge_cells('A1:G2')
    ws['A1'].value = "ATHITH MITHRA"
    ws['A1'].font = Font(bold=True, color="FF0000", size=18, name="Bookman Old Style")
    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 40

    ws.merge_cells('A3:B3')
    ws['A3'] = "NAME"
    ws['A3'].font = Font(bold=True, name="Bookman Old Style")
    ws.merge_cells('C3:D3')
    ws['C3'] = getattr(request.user, 'employee_name', '')
    ws['C3'].font = Font(bold=True, name="Bookman Old Style")

    ws.merge_cells('A4:B4')
    ws['A4'] = "EMPLOYEE ID"
    ws['A4'].font = Font(bold=True, name="Bookman Old Style")
    ws.merge_cells('C4:D4')
    ws['C4'] = request.user.username
    ws['C4'].font = Font(bold=True, name="Bookman Old Style")

    ws['E3'] = "BRANCH"
    ws['E3'].font = Font(bold=True, name="Bookman Old Style")
    ws.merge_cells('F3:G3')
    ws['F3'] = getattr(request.user, 'branch', '')
    ws['F3'].font = Font(bold=True, name="Bookman Old Style")

    ws['E4'] = "DEPARTMENT"
    ws['E4'].font = Font(bold=True, name="Bookman Old Style")
    ws.merge_cells('F4:G4')
    ws['F4'] = getattr(request.user, 'department', '')
    ws['F4'].font = Font(bold=True, name="Bookman Old Style")
    for row in range(3, 5):
        for col in range(1, 8):
            ws.cell(row=row, column=col).border = border

    
    ws.merge_cells(start_row=5, start_column=1, end_row=6, end_column=1)
    ws.merge_cells(start_row=5, start_column=2, end_row=6, end_column=2)
    ws.merge_cells(start_row=5, start_column=3, end_row=5, end_column=7)

    ws['A5'] = "S.NO"
    ws['B5'] = "DATE"
    ws['C5'] = "WORK STATUS"

    for cell_ref in ['A5', 'B5', 'C5']:
        cell = ws[cell_ref]
        cell.font = Font(bold=True, name="Bookman Old Style")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.fill = PatternFill(start_color="B7DEE8", end_color="B7DEE8", fill_type="solid")
        cell.border = border

    sub_headers = ["WORK CODE", "WORK DETAILS", "STARTING DATE", "ENDING DATE", "STATUS"]
    for idx, header in enumerate(sub_headers, start=3):
        cell = ws.cell(row=6, column=idx, value=header)
        cell.font = Font(bold=True, name="Bookman Old Style")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.fill = PatternFill(start_color="B7DEE8", end_color="B7DEE8", fill_type="solid")
        cell.border = border

    ws.row_dimensions[5].height = 25
    ws.row_dimensions[6].height = 25
    for row in [5, 6]:
        for col in range(1, 8):
            ws.cell(row=row, column=col).border = border

    current_row = 7
    for i, group in enumerate(groups, start=1):
        statuses = list(group.statuses.all())
        first_row = current_row

        for status in statuses:
            ws.cell(row=current_row, column=1, value=group.S_NO)
            ws.cell(row=current_row, column=2, value=group.DATE.strftime('%d-%m-%Y') if group.DATE else '')
            ws.cell(row=current_row, column=3, value=status.WORK_CODE)
            ws.cell(row=current_row, column=4, value=status.WORK_DETAILS)
            ws.cell(row=current_row, column=5, value=status.STARTING_DATE.strftime('%d-%m-%Y') if status.STARTING_DATE else '-')
            ws.cell(row=current_row, column=6, value=status.ENDING_DATE.strftime('%d-%m-%Y') if status.ENDING_DATE else '-')
            ws.cell(row=current_row, column=7, value=status.WORK_STATUS)

            for col in range(1, 8):
                cell = ws.cell(row=current_row, column=col)
                cell.font = data_font
                cell.border = border
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True) if col != 4 else Alignment(horizontal="left", vertical="top", wrap_text=True)

            current_row += 1

        last_row = current_row - 1
        if last_row > first_row:
            ws.merge_cells(start_row=first_row, start_column=1, end_row=last_row, end_column=1)
            ws.merge_cells(start_row=first_row, start_column=2, end_row=last_row, end_column=2)

    col_widths = [10, 15, 20, 40, 23, 23, 38]
    for i, width in enumerate(col_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"WORK_STATUS_REPORT_{request.user.username}_{month or 'All'}_{year or 'All'}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response