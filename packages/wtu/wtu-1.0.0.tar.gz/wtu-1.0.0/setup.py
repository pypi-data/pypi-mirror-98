#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="wtu",
    version="1.0.0",
    author="Syaoran",
    license='MIT License',
    author_email="SyaoranCheung@outlook.com",
    description="WTU gadget",
    long_description=open('./README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=open("./requirements.txt", 'r').read().split("\n"),  # 常用
    # include_package_data=True,  # 自动打包文件夹内所有数据
    # 如果需要包含多个文件可以单独配置 MANIFEST.in
    # package_data={
    #    'puggibot': ['source/*.txt', "source/*.json"],
    # },
    # 如果需要支持脚本方法运行，可以配置入口点
    # entry_points={
    #    'console_scripts': [
    #        'puggibot = puggibot:run'
    #    ]
    #}
)
