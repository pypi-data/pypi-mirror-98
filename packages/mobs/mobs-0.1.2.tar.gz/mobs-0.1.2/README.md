### 
```python
python setup.py check 校验 setup 写错了没有
python setup.py build 编译打包
python setup.py sdist 运行成功会在主目录下主动生成dist目录用来存放打包好的压缩包
python setup.py install  安装完成可以用来测试你的工具
# 上线发布
pip install twine
windows -> C:\Users\Administrator创建~.pypirc文件
[distutils]
index-servers = pypi
 
[pypi]
repository:https://pypi.python.org/pypi
username:
password:


twine upload dist/*

```

 代码库注册到 PyPI 
python setup.py register

------------
#pip install twine
pip install --upgrade twine setuptools wheel

python setup.py sdist build

python setup.py bdist_egg
python setup.py sdist bdist_wheel  ##
上传好打包的pip安装包
twine upload dist/mobs-0.1.1.tar.gz ##
pip install twine -i https://pypi.douban.com/simple/ 
pip install --upgrade mobs
# 更新包
pip install --upgrade mobs
# PYPI测试服
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-your-username

# 如何将自己的Python包发布到PyPI上
https://cloud.tencent.com/developer/article/1757852

https://blog.csdn.net/qq_36078992/article/details/109828412?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.baidujs&dist_request_id=1328626.12944.16153895514589037&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.baidujs

https://www.pythonheidong.com/blog/article/624110/3ac1cdd6c145574b12dd/

https://blog.csdn.net/Greenovia/article/details/79412063

https://www.cnpython.com/qa/411658

https://www.jb51.net/article/180223.htm

https://www.pythonf.cn/read/41178