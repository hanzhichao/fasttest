class Assert:

    def eq(self, actual, expected):
        assert actual == expected, f'断言失败: 实际值 {actual} 不等于 期望值 {expected}'

    def contains_by(self, actual, expected):
        assert actual in expected, f'断言失败: 期望值 {expected} 不包含 实际值 {actual}'

    def contains(self, actual, expected):
        assert expected in actual, f'断言失败: 实际值 {actual} 不包含 期望值 {expected}'

    def istrue(self, actual):
        assert actual is True, f'断言失败: 实际值 {actual} 不为True'

    def nottrue(self, actual):
        assert actual is not True, f'断言失败: 实际值 {actual} 为True'

    def isnull(self, actual):
        assert actual is None, f'断言失败: 实际值 {actual} 不为None'

    def notnull(self, actual):
        assert actual is not None, f'断言失败: 实际值 {actual} 为None'
