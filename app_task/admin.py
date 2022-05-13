from django.contrib import admin
from .models import Task, Comment, TaskMember


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    inlines = [CommentInLine]


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
admin.site.register(TaskMember)
# Register your models here.
