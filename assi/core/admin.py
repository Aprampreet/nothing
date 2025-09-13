from django.contrib import admin
from .models import Project, DevelopmentTask, DesignTask


class DevelopmentTaskInline(admin.TabularInline):
    model = DevelopmentTask
    extra = 1
    fields = ["title", "due_date", "priority", "status", "programming_language"]
    readonly_fields = ["created_at", "updated_at"]


class DesignTaskInline(admin.TabularInline):
    model = DesignTask
    extra = 1
    fields = ["title", "due_date", "priority", "status", "design_tool"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "status",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
    ]
    list_filter = ["status", "start_date", "end_date", "created_at"]
    search_fields = ["title", "description", "user__username"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [DevelopmentTaskInline, DesignTaskInline]


@admin.register(DevelopmentTask)
class DevelopmentTaskAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "title",
        "priority",
        "status",
        "programming_language",
        "repository_url",
        "due_date",
    ]
    list_filter = ["status", "priority", "due_date"]
    search_fields = ["title", "project__title", "programming_language"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(DesignTask)
class DesignTaskAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "title",
        "priority",
        "status",
        "design_tool",
        "asset_link",
        "due_date",
    ]
    list_filter = ["status", "priority", "due_date"]
    search_fields = ["title", "project__title", "design_tool"]
    readonly_fields = ["created_at", "updated_at"]
