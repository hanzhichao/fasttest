import importlib
import os
import re
import sys
from collections import ChainMap
from functools import reduce
from io import StringIO

import matplotlib.pyplot as plt

from fasttest import settings





def gen_pass_rate_chart(pass_num, fail_num, error_num, output_file):
    labels, sizes, colors = ['Passed'], [pass_num], ['green']
    if fail_num > 0:
        labels.append('Failed')
        sizes.append(fail_num)
        colors.append('red')
    if error_num > 0:
        labels.append('Errors')
        sizes.append(fail_num)
        colors.append('yellow')
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.savefig(output_file)
    return output_file




def get_celery_worker_status():
    from fasttest import celery_app
    i = celery_app.control.inspect()
    availability = i.ping()
    stats = i.stats()
    registered_tasks = i.registered()
    active_tasks = i.active()
    scheduled_tasks = i.scheduled()
    result = {
        'availability': availability,
        'stats': stats,
        'registered_tasks': registered_tasks,
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks
    }
    return result


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
