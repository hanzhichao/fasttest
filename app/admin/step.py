from adminsortable.admin import SortableTabularInline
from django import forms
from django_cascading_dropdown_widget.widgets import CascadingModelchoices, DjangoCascadingDropdownWidget

from app.admin.base import BaseTabularInline
from app.models.library import Library, Method
from app.models.step import SetupStep, Step, TeardownStep, TestStep


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        exclude = []
        # django-cascading-dropdown-widget 插件 的级联下拉配置
        # ---选择操作库--- 后 ---选择操作方法---
        widgets = {
            # step中的操作方法的外键字段名
            "method": DjangoCascadingDropdownWidget(
                choices=CascadingModelchoices(
                    {"model": Library, "related_name": "methods"},  # library反向查找methods的related_name
                    {"model": Method, "fk_name": "library"})),  # method关联library的字段名
        }


class TestStepInline(BaseTabularInline, SortableTabularInline):
    form = StepForm
    model = TestStep
    exclude = ['type', 'order']


class SetupStepInline(BaseTabularInline, SortableTabularInline):
    form = StepForm
    model = SetupStep
    exclude = ['type', 'order']


class TeardownStepInline(BaseTabularInline, SortableTabularInline):
    form = StepForm
    model = TeardownStep
    exclude = ['type', 'order']
