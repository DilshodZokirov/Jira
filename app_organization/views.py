import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET, require_safe
from django.views.generic import TemplateView, UpdateView

from Jira.auth import has_group
from app_accounts.models import Employee
from app_project.models import Project, ProjectMember
from app_uploads.utils import upload
from .forms import OrgForm, OrgUpdateForm
from .models import Organization, OrgMembers
from django.urls import reverse_lazy, reverse

from .service import create_org


class OrgCreate(TemplateView):
    template_name = 'create_organizations.html'

    def get(self, request, *args, **kwargs):
        form = OrgForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = OrgForm(request.POST, request.FILES)
        employee = Employee.objects.get(user=request.user.id)
        if form.is_valid():
            try:
                create_org(form, user=request.user, employee=employee)
                return redirect('home')
            except Exception as e:
                logging.error(e)
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


# # update view for details
# def update_view(request, id):
#     # dictionary for initial data with
#     # field names as keys
#     context = {}
#
#     # fetch the object related to passed id
#     obj = get_object_or_404(Or, id=id)
#
#     # pass the object as instance in form
#     form = OrgUpdateForm(request.POST or None, instance=obj)
#
#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect("/" + id)
#
#     # add form dictionary to context
#     context["form"] = form
#
#     return render(request, "update_view.html", context)

def searched(request):
    search = request.GET.get('search')
    if search is None:
        # organization = Organization.objects.filter(pk=org_pk)
        name = Employee.objects.all()
    else:
        # organization = Organization.objects.filter(pk=org_pk)
        name = Employee.objects.filter(user__username__icontains=search)

    return render(request, 'searched.html', {'search': search,
                                             'name': name,
                                             # 'organization': organization
                                             })


def OrgUpdateView(request, org_pk):
    context = {}
    org = get_object_or_404(Organization, pk=org_pk)
    if request.method == "POST":
        form = OrgUpdateForm(request.POST, request.FILES, instance=org)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = OrgUpdateForm(instance=org)
        context['form'] = form
    return render(request, 'organization_edit.html', context)


def OrgDetail(request, org_id):
    contact = get_object_or_404(Organization, pk=org_id)
    product = Project.objects.filter(organization=contact)
    user = Employee.objects.all()
    prj_mem = OrgMembers.objects.filter(org=contact, add=True)

    # if user.pk==prj_mem
    context = {'contact': contact,
               'product': product,
               'users': user,
               'project_members': prj_mem}
    return render(request, 'organization_detail.html', context=context)


# todo Rollarni to'g'irlashim kerak
def add_member(request, org_pk, user_pk):
    other_user = get_object_or_404(Employee, user=user_pk)
    created_user = User.objects.get(pk=request.user.id)
    org = get_object_or_404(Organization, pk=org_pk)
    orgs, created = OrgMembers.objects.get_or_create(
        org=org,
        user=other_user,
        created_by=created_user,
        add=True
    )
    try:
        if other_user.pk != created_user.pk:
            orgs.user.add = True
            orgs.save()
        else:
            return redirect('organization:add_employee')
        return redirect('home')
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('home'))


def delete_member(request, org_pk, user_pk):
    other_user = get_object_or_404(Employee, user=user_pk)
    created_user = User.objects.get(pk=request.user.id)
    org = get_object_or_404(Organization, pk=org_pk)
    orgs = OrgMembers.objects.filter(user=other_user, org=org).first()
    if orgs:
        orgs.delete()
    orgs, created = OrgMembers.objects.get_or_create(
        org=org,
        user=other_user,
        created_by=created_user,
        add=False
    )
    try:
        if other_user.pk != created_user:
            orgs.save()
        return HttpResponseRedirect(reverse('home'))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('home'))


def connect_organization(request):
    orgmem = OrgMembers.objects.filter(user_id=request.user.id)
    context = {'orgmem': orgmem}
    return render(request, 'orgmember.html', context=context)


def update_role(request, org_pk, role_pk, user_pk):
    other_user = get_object_or_404(Employee, user=user_pk)
    role = Group.objects.get(pk=role_pk)
    created_user = User.objects.get(pk=request.user.id)
    org = get_object_or_404(Organization, pk=org_pk)
    orgs = OrgMembers.objects.filter(user=other_user, org=org).first()
    # borg = OrgMembers.objects.get(user=created_user, role=role, org=org)
    # lorg = OrgMembers.objects.get(user=other_user.user.id, role=role, org=org)
    if orgs:
        orgs.delete()
    orgs, created = OrgMembers.objects.update_or_create(
        org=org,
        user=other_user,
        role=role,
        created_by=created_user,
        add=True
    )
    try:
        if other_user.pk != created_user.id:
            orgs.save()
            messages.success(request, 'Role muvoffaqiyatli  o\'zgardi')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'Sizda bunday imkoniyat yo\'q')
            return redirect('home')
    except User.DoesNotExist:
        return redirect('organization:employee_list')


def org_delete_page(request, org_id: int):
    organization = Organization.objects.get(pk=org_id)
    return render(request, 'organization_delete.html', {'organization': organization})


def org_delete(request, org_id: int):
    organization = Organization.objects.get(pk=org_id)
    if organization.created_by:
        organization.delete()
    else:
        raise Exception('Oka siz yaratmaganszu qanaqa qilib uchirasz')
    return redirect('home')


def add_members(request, org_pk):
    context = {}
    orgs = Organization.objects.filter(pk=org_pk)
    orgmem = OrgMembers.objects.filter(org=org_pk)
    context['orgs'] = orgs
    context['orgmem'] = orgmem
    employee = Employee.objects.all()
    context['employee'] = employee
    # if not employee.filter(user_id=request.user.id):
    #     context['employee'] = employee
    return render(request, 'add_members.html', context=context)


def members(request, org_pk):
    orgs = OrgMembers.objects.filter(org=org_pk, add=True)
    context = {
        'orgs': orgs,
    }
    return render(request, 'members.html', context=context)


def employee_roles(request, org_pk, user_id):
    roles = OrgMembers.objects.filter(org=org_pk, user=user_id)
    group = Group.objects.all()
    context = {
        'roles': roles,
        'group': group
    }
    return render(request, 'role.html', context=context)
