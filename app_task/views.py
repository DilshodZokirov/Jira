import logging

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from app_accounts.models import Employee
from app_organization.models import OrgMembers
from app_project.models import Project
from app_task.forms import TaskForm, CommentForm
from app_task.models import Task, Comment, TaskMember
from app_uploads.utils import upload


# Create your views here.


def CreateTask(request, pk):
    prj = Project.objects.get(pk=pk)
    form = TaskForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            data = form.cleaned_data
            title = data.get('title')
            description = data.get('description')
            image = upload(form.files.get('image'))
            project = Task(title=title, description=description, image=image, created_by=request.user,
                           project=prj)
            project.save()
            return redirect('project:detail_prj', pk)
        except Exception as e:
            logging.error(e)
            return render(request, 'create_task.html', {'form': form})

    else:
        return render(request, 'create_task.html', {'form': form})


#
# def PrjDetail(request, prj_id):
#     project = get_object_or_404(Project, pk=prj_id)
#     task = Task.objects.filter(project=project)
#     return render(request, 'detail_projects.html', {'project': project, 'tasks': task})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Task, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        try:
            data = form.cleaned_data
            text = data.get('text')
            project = Comment(post=post, text=text, created_by=request.user)
            project.save()
            return redirect('project:detail_prj', pk)
        except Exception as e:
            logging.error(e)
            return render(request, 'create_task.html', {'form': form})
    else:
        return render(request, 'add_comment.html', {'form': form})


def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('project:detail_prj', pk=comment.post.pk)


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('project:detail_prj', pk=comment.post.pk)


def TaskDetail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    comment = Comment.objects.filter(post=task)
    return render(request, 'detail_tasks.html', {'tasks': task, 'comments': comment})


def task_add_member(request, task_id, user_pk):
    other_user = get_object_or_404(Employee, pk=user_pk)
    created_user = User.objects.get(pk=request.user.id)
    task = get_object_or_404(Task, pk=task_id)
    tasks, created = TaskMember.objects.get_or_create(
        user=other_user,
        task=task,
        created_by=created_user,
        add=True
    )
    try:
        if other_user.pk != created_user:
            # project.user.add = True
            tasks.save()
        return redirect('project:detail_prj', task.project.id)
    except User.DoesNotExist:
        return redirect('project:detail_prj', task.project.id)


def task_delete_member(request, task_id, user_pk):
    other_user = get_object_or_404(Employee, pk=user_pk)
    created_user = User.objects.get(pk=request.user.id)
    task = get_object_or_404(Task, pk=task_id)
    task, created = TaskMember.objects.get_or_create(
        user=other_user,
        task=task,
        created_by=created_user,
        add=True
    )
    try:
        if other_user.pk != created_user:
            # project.user.add = True
            task.delete()
        return redirect('project:detail_prj', task)
    except User.DoesNotExist:
        return redirect('organization:org_detail', task)


def task_members(request, task_id):
    task = TaskMember.objects.filter(task=task_id)
    context = {
        'tasks': task,
    }
    return render(request, 'task_members.html', context=context)
