# _*_ coding: utf-8 _*_
#!/usr/bin/env python3
from typing import Tuple, Dict, Union, Text, List, Callable
# 处理差异 数据

class DiffUtils(object):

    @staticmethod
    def intersection_data(list1: List, list2: List) -> List:
        '''
        相交数据 / 两个列表都存在的元素 / 两个列表相同的元素 / 取出相同的元素 >>>
            list1 = [1,2,3,4,5, '李白','你好']
            list2 = [4,5,6,7,'李白','hello']
            >>>
            [4, 5, '李白']
        :param list1:
        :param list2:
        :return:
        '''
        return [x for x in list1 if x in list2]

    @staticmethod
    def differ_data(list1: List, list2: List) -> List:
        '''
        两个列表中不同的元素 >>>
            list1 = [1,2,3,4,5, '李白','你好']
            list2 = [4,5,6,7,'李白','hello']
            >>>
            [1, 2, 3, '你好', 6, 7, 'hello']
        :param list1:
        :param list2:
        :return:
        '''
        return [L for L in (list1 + list2) if L not in [x for x in list1 if x in list2]]

    @staticmethod
    def alone_data(list1: List, list2: List) -> List:
        '''
        单独存在 / 在list1列表中而不在list2列表中
            list1 = [1,2,3,4,5, '李白','你好']
            list2 = [4,5,6,7,'李白','hello']
            >>>
            [1, 2, 3, '你好']
        :param list1:
        :param list2:
        :return:
        '''
        # 单独存在
        if isinstance(list1, List) and isinstance(list2, List):
            return [x for x in list1 if x not in list2]

    @staticmethod
    def reveal_duplication_data(list: List, frequency: bool = False) -> Union[List, Dict]:
        '''
        展示列表重复的元素 >>>
            [1,2,2,3,4,5, '李白','李白', '你好']
            >>>
            [2, '李白']

        当 frequency == True 时 > 展现重复元素和重复次数 >>>
            [1,2,2,3,4,5, '李白','李白', '你好']
            >>>
            {2: 2, '李白': 2}

        :param list:
        :param frequency: default false
        :return:
        '''

        from collections import Counter
        if isinstance(list, List):
            if frequency == False:
                return [key for key, value in dict(Counter(list)).items() if value > 1]
            else:
                return {key: value for key, value in dict(Counter(list)).items() if value > 1}

    @staticmethod
    def de_duplication_data(args: List) -> List:
        '''
        对列表去重 >>>
            list1 = [1,2,2,3,4,5, '李白','李白', '你好']
            >>>
            [1, 2, 3, 4, 5, '你好', '李白']
        :param list:
        :return:
        '''
        if isinstance(args, List):
            return list(set(args))

if __name__ == '__main__':
    list1 = [1,2,2,3,4,5, '李白','李白', '你好']
    list2 = [4,5,6,7,'李白','hello']
    str = 'sdf'
    a = DiffUtils()
    result = a.differ_data(list1,list2)
    print(result)

