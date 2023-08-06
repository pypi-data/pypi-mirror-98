#!/usr/bin/python
# -*- coding: UTF-8 –*-

import setuptools
with open(r'__version__.txt') as f:
    long_version = f.read()
with open(r'requirements.txt') as f1:
    r_package = f1.readlines()

setuptools.setup(
    name="jquote_api",
    version=long_version,
    author="jxl",
    author_email="1013359736@qq.com",
    description="A small jxl package",
    long_description="这是用于获取股票行情数据/财务数据/行业数据的第三方库",
    long_description_content_type="text/markdown",
    url="https://blog.csdn.net/u011439313/article/details/113445053?spm=1001.2014.3001.5501",
    packages=setuptools.find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=r_package,
    platforms=["all"],
    classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
)

    #python_requires='>=3.6',

