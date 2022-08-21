from django.contrib import admin

from account.models import Operation, OperationCategory, Tag


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    ordering = ('-date', 'user', 'category', 'title')
    list_display = ('date', 'title', 'amount', 'user', 'category', 'tags_list')
    search_fields = ('date', 'title', 'amount', 'user', 'category')

    def tags_list(self, obj):
        return ", ".join(obj.tags.all().values_list("name"))


@admin.register(OperationCategory)
class OperationCategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    search_fields = list_display


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)
    search_fields = list_display
