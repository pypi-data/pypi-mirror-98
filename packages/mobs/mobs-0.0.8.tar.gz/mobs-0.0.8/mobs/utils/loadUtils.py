# _*_ coding: utf-8 _*_
#!/usr/bin/env python3
# 加载文件
import os
import xlrd

import yaml
import json
import csv
from mobs.utils.takes import resolve_dict
from mobs.utils.exceptions import FileFormatError, JSONDecodeError, CSVNotFound, FileNotFound, FileFormatNotSupported,FolderNotFound


from typing import Tuple, Dict, Union, Text, List, Callable, Any, Mapping



BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 正则表达式匹配规则
PATTERN_YML = os.path.join(BASE_PATH, 'config', 'pattern.yaml')
#print(PATTERN_YML)

class Config:

    @staticmethod
    @resolve_dict(name='pattern', key='zh_CN')
    def get_yaml_conf(yaml_file=PATTERN_YML):
        return FileUtils.load_file(yaml_file)



class FileUtils(object):

    @staticmethod
    def _get_file_suffix(filePath):
        suffix = filePath.split('.', 1)[1]
        return suffix
    @staticmethod
    def _check_format(filePath, content):
        '''
        校验内容
        :param content:
        :return:
        '''
        if not content:
            errMsg = u"File content is empty! \"{}\"".format(filePath) # 文件内容是空的！
            raise FileFormatError(errMsg)
        elif not isinstance(content, (list, dict)):
            errMsg = u"File content format invalid!" # 文件内容格式无效！
            raise  FileFormatError(errMsg)

    @staticmethod
    def _load_text_file(filePath):
        txt_content = []
        with open(filePath, 'r', encoding='utf-8-sig') as file_object:
            while True:
                content = file_object.readline()
                if not content:
                    break
                line = content.strip('\n')
                txt_content.append(line)
        FileUtils._check_format(filePath, txt_content)
        return txt_content

    @staticmethod
    def _load_yaml_file(filePath):
        with open(filePath, 'r', encoding='utf-8') as file_object:
            yml_content = yaml.load(file_object, Loader=yaml.CLoader)
            #yml_content = yaml.safe_load(file_object)
            FileUtils._check_format(filePath, yml_content)
            return yml_content

    @staticmethod
    def _load_json_file(filePath):
        with open(filePath, 'r', encoding='utf-8') as file_object:
            try:
                json_content = json.load(file_object)
            except JSONDecodeError:
                errMsg = u"JsonDecodeError:Json file format error! \"{}\"".format(filePath)
                raise FileFormatError(errMsg)
            FileUtils._check_format(filePath, json_content)
            return json_content


    @staticmethod
    def _load_csv_file(filePath):
        csv_content = []
        with open(filePath, encoding='utf-8') as file_object:
            reader = csv.DictReader(file_object)
            for row in reader:
                csv_content.append(row)
        return csv_content

    @staticmethod
    def load_file(filePath):

        if not os.path.isfile(filePath):
            raise FileNotFound(u"File is not exist \"{}\"".format(filePath))
        file_suffix = os.path.splitext(filePath)[1].lower()
        if file_suffix == '.txt':
            return FileUtils._load_text_file(filePath)
        elif file_suffix == '.json':
            return FileUtils._load_json_file(filePath)
        elif file_suffix in ['.yaml', '.yml']:
            return FileUtils._load_yaml_file(filePath)
        elif file_suffix == '.csv':
            return FileUtils._load_csv_file(filePath)
        else:
            # 其它文件后缀
            errMsg = u"File format not supported \"{}\"".format(filePath)

            raise FileFormatNotSupported(errMsg)

    @staticmethod
    def load_folder_files(folderPath: Text, recursive: bool = True) -> List:
        '''

        :param folderPath:
        :param recursive: 是否递归(是否加载下级目录文件)
        :return: file_list >>> 文件路径 ; fileList>>> 文件名
        '''
        if not os.path.isdir(folderPath):
            raise FolderNotFound(u"Folder does not exist \"{}\"".format(folderPath))

        if isinstance(folderPath, (list, set)):
            files = []
            for path in set(folderPath):
                files.extend(FileUtils.load_folder_files(path, recursive))
            return files
        if not os.path.exists(folderPath):
            raise FolderNotFound(u"Folder does not exist \"{}\"".format(folderPath))
        file_list = []
        #fileList = []
        for dirPath, dirNames, fileNames in os.walk(folderPath):
            fileNames_list = []
            for fileName in fileNames:
                # 过滤掉yaml文件和json文件
                if not fileName.endswith(('.yml', '.yaml', '.json', '.txt', '.xlsx')):
                    continue
                fileNames_list.append(fileName)
                #fileList.append(fileName)
            for fileName in fileNames_list:
                filePath = os.path.join(dirPath, fileName)
                file_list.append(filePath)
            if not recursive:
                break
        return file_list






    @staticmethod
    def load_sub_folder(folderPath: Text) -> List:
        files_list = []
        folder_files = os.listdir(folderPath)
        for i in range(0, len(folder_files)):
            path = os.path.join(folderPath, folder_files[i])
            if os.path.isdir(path):
                files_list.extend(FileUtils.load_sub_folder(path))
            if os.path.isfile(path):
                files_list.append(path)
        return files_list

    @staticmethod
    def load_file_name(filePath: Text, recursive: bool = False) -> List:
        '''
            获取目录 或者 文件的文件名
        :param filePath: 目录路径 或者 文件路径
        :param recursive: 是否递归下级目录 True > 递归
        :return:
        '''
        # 路径 文件  文件夹
        result = []
        if os.path.isdir(filePath):
            files = FileUtils.load_folder_files(filePath, recursive=recursive)
            for file in files:
                data = os.path.splitext(file)[0]
                if '\\' in data:
                    temp = data.rsplit('\\', 1)[1]
                else:
                    temp = data.rsplit('/', 1)[1]
                result.append(temp)
        if os.path.isfile(filePath):
            # 文件带路径
            if '\\' in filePath:
                data = filePath.rsplit('\\', 1)[1]
                temp = data.rsplit('.', 1)[0]
                result.append(temp)
            elif '/' in filePath:
                data = filePath.rsplit('/', 1)[1]
                print(data)
                temp = data.rsplit('.', 1)[0]
                print(temp)
                result.append(temp)

        return result

class ReadExcel:

    def __init__(self,excel_file):
        if not os.path.isfile(excel_file):
            # file path not exist
            raise CSVNotFound(excel_file)
        self.workbook = xlrd.open_workbook(excel_file)

    def get_all_sheetnames(self):
        """
        获取所有sheet的名称
        :return: list
        """
        self.all_sheetnames = self.workbook.sheet_names()
        return self.all_sheetnames

    def get_index_sheetnames(self, num):
        """
        根据索引号num，获取sheet名称
        :param num:索引号
        :return:string
        """
        self.all_sheetindexs = self.workbook.sheet_names()[num]
        return self.all_sheetindexs

    def get_sheet_content_index(self, num):
        """
        根据索引获取sheet内容，索引从0开始
        :param num:
        :return:
        """
        self.sheet_content = self.workbook.sheet_by_index(num)
        return self.sheet_content

    def get_sheet_content_name(self, sheetName):
        """
        根据sheet名称获取sheet内容
        :param sheetName:
        :return:
        """
        self.sheet_content = self.workbook.sheet_by_name(sheetName)
        return self.sheet_content

    def get_sheet_name(self, num):
        """
        根据索引号获取sheetname
        :param num:
        :return:
        """
        self.sheet_name = self.get_sheet_content_index(num).name
        return self.sheet_name

    def get_sheet_nrow(self, num):
        """
        获取行数
        :param num: 索引号
        :return:
        """
        self.sheet_row = self.get_sheet_content_index(num).nrows
        return self.sheet_row

    def get_sheet_ncol(self, num):
        """
        获取列数
        :param num: 索引号
        :return:
        """
        self.sheet_col = self.get_sheet_content_index(num).ncols
        return self.sheet_col

    # 获取整行或整列的值
    def get_sheet_row_values(self, num, row):
        """
        根据索引号num，以及行数row 获取整行的值
        :param num: 索引号获取sheet
        :param row: 指定行数获取 row + 1 行的值
        :return:
        """
        self.sheet_row_value = self.get_sheet_content_index(num).row_values(row)
        return self.sheet_row_value

    def get_sheet_col_values(self, num, col):
        """
        根据索引号num，以及列数col 获取整列的值
        :param num: 索引号获取sheet
        :param col: 指定列数获取 col + 1 列的值
        :return:
        """
        self.sheet_col_value = self.get_sheet_content_index(num).col_values(col)
        return self.sheet_col_value

    # 获取单元格
    def get_sheet_cell_value(self, num, rowx, colx):
        """
        根据索引号num，行数rowx，列数colx 获取单元格的内容
        :param num: 索引号获取sheet
        :param rowx: 指定要获取单元格的行数
        :param colx: 指定要获取单元格的列数
        :return:
        """
        self.sheet_cell_value = self.get_sheet_content_index(num).cell(rowx, colx).value
        return self.sheet_cell_value

    def get_sheet_cell_value_1(self, num, rowx, colx):
        """
        获取单元格
        :param num:
        :param rowx:
        :param colx:
        :return:
        """
        self.sheet_cell_value = self.get_sheet_content_index(num).cell_value(rowx, colx)
        return self.sheet_cell_value

    def get_sheet_cell_value_2(self, num, rowx, colx):
        """
        获取单元格
        :param num:
        :param rowx:
        :param colx:
        :return:
        """
        self.sheet_cell_value = self.get_sheet_content_index(num).row(rowx)[colx].value
        return self.sheet_cell_value

    def get_sheet_cell_content_type(self, num, rowx, colx):
        """
        获取单元格内容的数据类型
        Tips：python 读取excel 单元格的内容返回有5种类型
        [0 empty, 1 string,2 number,3 date, 4 boolean, 5 error]
        :param num:
        :param rowx:
        :param colx:
        :return:
        """
        self.sheet_cell_type = self.get_sheet_content_index(num).cell(rowx,colx).ctype
        return self.sheet_cell_type

    def get_sheet_all_content(self, sheetName):
        """
        根据sheet名称获取所有内容（行数/列数/内容），并将每个单元格放进 list
        :param sheetName:
        :return:
        """
        worksheet = self.get_sheet_content_name(sheetName)
        self.row = worksheet.nrows
        self.list = []
        for self.row in range(self.row):
            self.rowdate = worksheet.row_value(self.row) # i行的list
            for self.col,self.value in enumerate(self.rowdate):
                self.result = "(" + str(self.row) + "," + str(self.col) + "," + str(self.value) + ")"
                self.list.append(self.result)
        return self.list

    def get_sheet_rowx_content(self, num, rowx):
        """
        读取一整行的数据
        根据num获取sheet，以及行数获取整行的数据
        :param num:
        :param rowx:
        :return:
        """
        worksheet = self.get_sheet_content_index(num)
        self.row = [str(worksheet.cell_value(rowx, i)) for i in range(0, worksheet.ncols)]
        return ','.join(self.row)

    def get_sheet_colx_content(self, num, colx):
        """
        读取一整列的数据
        根据索引号获取sheet，以及列数获取整列的数据
        :param num:
        :param colx:
        :return: string
        """
        worksheet = self.get_sheet_content_index(num)
        self.col = [str(worksheet.cell_value(i, colx)) for i in range(1, worksheet.nrows)] # 取1，则不读首行
        return self.col

if __name__ == '__main__':
    conf = Config()
    te = FileUtils.load_file('D:\CodeBase\mobslala\mobs\config\pattern.yaml')

    print(conf.get_yaml_conf())
