import logging

from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404

from Jira.auth import has_group
from app_accounts.models import Employee
from app_organization.models import Organization, OrgMembers
from app_project.forms import PrjForm
from app_project.models import Project, ProjectMember
from app_task.models import Task, TaskMember
from app_uploads.utils import upload


@has_group(groups=[1, 2, 3])
def CreatePrj(request, pk):
    org = Organization.objects.get(pk=pk)
    form = PrjForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            data = form.cleaned_data
            title = data.get('title')
            description = data.get('description')
            image = upload(form.files.get('image'))
            project = Project(title=title, description=description, image=image, created_by=request.user,
                              organization=org)
            project.save()
            user = Employee.objects.get(user_id=request.user.id)
            orgmem = OrgMembers.objects.get(user=user, org=org)
            orgs = ProjectMember(user=user, project=project, role=orgmem.role, created_by=request.user)
            orgs.save()
            return redirect('home')
        except Exception as e:
            logging.error(e)
            return render(request, 'create_projects.html', {'form': form})
    else:
        return render(request, 'create_projects.html', {'form': form})


def PrjDetail(request, prj_id):
    project = get_object_or_404(Project, pk=prj_id)
    task = Task.objects.filter(project=project)
    task_mem = ProjectMember.objects.all()
    return render(request, 'detail_projects.html', {'project': project, 'tasks': task, 'task_members': task_mem})


def prj_delete_page(request, prj_id: int):
    project = Project.objects.get(pk=prj_id)
    return render(request, 'delete_projects.html', {'project': project})


def prj_delete(request, prj_id: int):
    prj = Organization.objects.get(pk=prj_id)
    prj.delete()
    return redirect('home')


def add_member(request, prj_id, user_pk, role_id):
    created_user = User.objects.get(pk=request.user.id)
    employee = get_object_or_404(Employee, user=user_pk)
    role = Group.objects.get(id=role_id)
    prj = get_object_or_404(Project, pk=prj_id)

    project, created = ProjectMember.objects.get_or_create(
        user=employee,
        role=role,
        project=prj,
        created_by=created_user,
        add=True
    )
    try:
        if employee.pk != created_user:
            project.save()
        return redirect('organization:org_detail', prj.organization.pk)
    except User.DoesNotExist:
        return redirect('organization:org_detail', prj.organization.pk)


def delete_member(request, prj_id, user_pk):
    other_user = get_object_or_404(Employee, user=user_pk)
    created_user = User.objects.get(pk=request.user.id)
    prj = get_object_or_404(Project, pk=prj_id)
    project, created = ProjectMember.objects.get_or_create(
        user=other_user,
        project=prj,
        created_by=created_user,
        add=True
    )
    try:
        if other_user.pk != created_user:
            project.delete()
        return redirect('project:prj_member_list', prj_id=prj.id, org_id=prj.organization.id)
    except User.DoesNotExist:
        return redirect('project:prj_member_list', prj_id=prj.id, org_id=prj.organization.id)


def prj_members(request, prj_id, org_id):
    project = ProjectMember.objects.filter(project=prj_id, add=True)
    org = OrgMembers.objects.filter(org=org_id, add=True)
    context = {
        'projects': project,
        'organizations': org
    }
    return render(request, 'project_members.html', context=context)

# def add(request, user_id):
#     user = Employee.objects.get(user_id=user_id)
#     return render(request, 'add.html', context=context)
