# _*_ coding: utf-8 _*_
#!/usr/bin/env python3
# 提取数据
import re
import sys,os
from mobs.utils.loadUtils import FileUtils, Config
from loguru import logger
from mobs.utils.takes import execute_time
from typing import Tuple, Dict, Union, Text, List, Callable

pattern = {
        'in_brackets': r"(?<=\().*?(?=\))" ,  # 提取 (xxx) >>> 括号内的内容
        ## "萨芬)会及时答复(胜多)负少("  >>> r"(?<=\)).*?(?=\()"

    }


class ExtractUtils(object):
    config =  Config

    @execute_time
    def extract_zh_cn(self, args: Union[Text, List]) -> List:
        '''
        extract list or str >>> zh_CN
        :param args:
        :return:
        '''

        pattern = self.config.get_yaml_conf()
        zhe_cn: List = []
        if not isinstance(args, (str, list)):
            return zhe_cn
        elif isinstance(args, list):
            zhe_cn = [re.compile(pattern).findall(x) for x in args]
        elif isinstance(args, str):
            zhe_cn = re.compile(pattern).findall(args)
        logger.info(zhe_cn)
        return zhe_cn

    @execute_time
    def extract_zh_cn_rt(self, args: Union[Text, List]) -> List:
        '''
        extract list or str >>> zh_CN
        :param args:
        :return:
        '''

        pattern = r'[\u4e00-\u9fa5]+'
        zhe_cn: List = []
        if not isinstance(args, (str, list)):
            return zhe_cn
        elif isinstance(args, list):
            zhe_cn = [re.compile(pattern).findall(x) for x in args]
        elif isinstance(args, str):
            zhe_cn = re.compile(pattern).findall(args)
        logger.info(zhe_cn)
        return zhe_cn

    @staticmethod
    def extract_content_in_brackets(data: Text) -> List:
        '''
        提取英文括号内的内容
        "你好！(今天)有(空)吗?"     >>> ['今天', '空']
        :param data:
        :return:
        '''
        content = re.findall(pattern['in_brackets'], data, re.S)
        return content

    @staticmethod
    def extract_content(list1: List, list2: List) -> List:
        '''
        list1列表的元素 在 list2列表中 > 两个列表相同的元素
        :param list1:
        :param list2:
        :return:
        '''
        #return list(set(list1).intersection(set(list2)))
        return [i for i in list1 if i in list2]

    @staticmethod
    def rescall_line_num(key: str, txt_file) -> List:
        '''
        获取key与下一个key的间隔行数，返回列表的最后一个元素是文件的最后一行行数 >>>

        Args:
            txt_file (str): txt file path, The first column is the number of rows,
            txt file content is like below:
        Examples:
            #>>> cat txt_file
            1 id: 0f52ed0e5ed_01
            2 Scores: (#C #S #D #I)
            3 REF:    你 好 哪 位
            4 HYP:    你 好 哪 位
            5 Eval:
            6
            7 SpeaKer sentences 88: 1ae   #utts: 2
            8 id: 0f52ed0e5ed_02
            9 Scores: (#C #S #D #I)
            10 REF:    *** 是 的 *** 好
            11 HYP:    唉 是 的 你 好
            12 Eval:   I    I

            >>> # rescall_line_num('id', txt_file)
            [1, 8, 12]

        :param key: str 根据这个字符串作为参考
        :param txt_file: txt 文件路径
        :return: list of parameters 返回列表
        '''
        init_data = FileUtils()._load_text_file(txt_file)
        count = len(init_data)
        # 步长，每个id间隔的行数
        step = 0
        # 步长列表
        list_step = []
        for line in init_data:
            step += 1
            if key in line:
                list_step.append(step)
        # 最后一个id到最后一个行的间隔行数
        list_step.append(count)
        return list_step

    @staticmethod
    def operate_pra(key: str, txt_file):
        '''
        根据id与下一个id间隔行数，做分隔处理
        :param txt_file:
        :return:
        '''
        list_step = ExtractUtils.rescall_line_num(key, txt_file)
        print(list_step)
        # 根据相邻的id间隔行数打印文本
        list_content = []
        for i in range(0, len(list_step) - 1):
            start_num = list_step[i]
            end_num = list_step[i + 1]
            with open(txt_file, 'r', encoding='utf-8-sig') as f:
                for line_x in f.readlines()[start_num - 1:end_num]:
                    print(line_x)
                    list_content.append(line_x.strip('\n'))
                print('==' * 20)
        return list_content

if __name__ == '__main__':
    path = r"test\test_data\test_01.txt"


    b = ExtractUtils()
    #print(b.extract_content_in_brackets("你好！(今天)有(空)吗?"))
    temp = b.extract_zh_cn(['你好sdfs十多分88吗?','asd','安定4','asd安定'])
    temp2 = b.extract_zh_cn_rt(['你好sdfs十多分88吗?', 'asd', '安定4', 'asd安定'])
    print(temp)
    print(temp2)

