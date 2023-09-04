import os
import re
import sys
from collections import ChainMap
from functools import reduce
from io import StringIO

import matplotlib.pyplot as plt

DOLLAR_VARIABLE = re.compile('\${?([\w.]+)}?')
PURE_DOLLAR_VARIABLE = re.compile('^\${?([\w.]+)}?$')


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


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


class Context:
    def __init__(self, variables=None):
        variables = variables or {}
        self.variables = ChainMap(variables, os.environ)

    @staticmethod
    def do_dot(item, key: str):
        """单个content.url取值"""
        if hasattr(item, key):
            return getattr(item, key)
        if key.isdigit():
            key = int(key)
        try:
            return item[key]
        except Exception as ex:
            return key

    def repl_func(self, matched):
        if matched:
            text = matched.group(1)
            return str(self.get_field(text))

    def get_field(self, expr: str):
        """解析形如content.result.0.id的取值"""
        if '.' in expr:
            value = expr.split('.')
            field = self.variables.get(value[0])
            return reduce(lambda x, y: self.do_dot(x, y), value[1:], field)
        else:
            return self.variables.get(expr)

    def get(self, expr: str):
        if isinstance(expr, str) and DOLLAR_VARIABLE.match(expr):
            matched = PURE_DOLLAR_VARIABLE.match(expr)
            if matched:
                return self.get_field(matched.group(1))
            return re.sub(DOLLAR_VARIABLE, self.repl_func, expr)
        return self.variables.get(expr, expr)

    def set(self, key, value):
        if isinstance(value, str):
            value = self.get(value)
        self.variables.update({key: value})
