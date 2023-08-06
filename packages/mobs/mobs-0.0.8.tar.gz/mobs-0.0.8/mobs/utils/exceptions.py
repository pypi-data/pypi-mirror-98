# _*_ coding: utf-8 _*_
#!/usr/bin/env python3
class BaseError(Exception):
    pass

class FileFormatError(BaseError):
    pass

class NotFoundError(BaseError):
    pass

class FileNotFound(FileNotFoundError, NotFoundError):
    pass

class FileFormatNotSupported(FileNotFoundError, NotFoundError):
    pass

class JSONDecodeError(NotFoundError):
    pass

class CSVNotFound(NotFoundError):
    pass

class FolderNotFound(NotFoundError):
    pass

# 解析字典错误
class ResolveDictError(NotFoundError):
    pass

