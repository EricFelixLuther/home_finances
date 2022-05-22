from django.contrib import admin

from account.models import Operation, OperationCategory


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    ordering = ('-date', 'user', 'category', 'title')
    list_display = ('date', 'title', 'amount', 'user', 'category')
    search_fields = list_display


@admin.register(OperationCategory)
class OperationCategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    search_fields = list_display
