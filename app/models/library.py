import importlib

from django.db import models

from fasttest import settings
from . import BaseModel


def load_libs(config: dict) -> dict:
    """
    根据配置中的初始化参数加载库对象
    eg: config = {'Http': {'base_url': 'http://localhost:8080'}}
    """
    libs = {}
    config = config or {}
    for lib_config in settings.TEST_LIBRARIES:
        for class_name, module_path in lib_config.items():
            module = importlib.import_module(module_path)
            lib_class = getattr(module, class_name)
            init_args = config.get(class_name, {})
            lib = lib_class(**init_args)
            libs[class_name] = lib
    return libs


class Library(BaseModel):
    args = models.JSONField("初始化参数格式", blank=True, null=True, default=dict)

    def get_lib(self, config: dict = None):
        libs = load_libs(config)
        return libs.get(self.name)

    class Meta:
        verbose_name = '操作库'
        verbose_name_plural = '操作库'


class Method(BaseModel):
    library = models.ForeignKey(Library, verbose_name='所属操作库', related_name='methods', on_delete=models.CASCADE)
    args = models.JSONField("参数格式", blank=True, null=True, default=dict)

    def get_method(self, config):
        lib = self.library.get_lib(config)
        method = getattr(lib, self.name)
        return method

    def __str__(self):
        return '%s.%s' % (self.library.name, self.name)

    class Meta:
        verbose_name = '操作方法'
        verbose_name_plural = '操作方法'
