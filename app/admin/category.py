from adminsortable.admin import NonSortableParentAdmin, SortableTabularInline
from django.contrib import admin

from app.admin.base import BaseModelAdmin, BaseTabularInline
from app.models.category import Category


class CategoryInline(BaseTabularInline, SortableTabularInline):
    model = Category
    exclude = ['order']


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin, NonSortableParentAdmin):
    admin_order = 2
    list_display = ['id', '__str__', 'description', 'level', 'testcases_cnt']
    inlines = [CategoryInline]
    ordering = ('parent', 'order')
    fields = ('parent',
              'name', 'description',
              'order'
              )

    @admin.display(description='用例数量')
    def testcases_cnt(self, obj):
        return obj.all_testcases.count()
