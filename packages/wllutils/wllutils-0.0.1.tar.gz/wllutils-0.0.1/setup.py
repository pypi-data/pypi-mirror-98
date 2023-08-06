#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
import os

# 提供一些有用的信息
URL = 'https://github.com/Wei-Liulei/utils'
NAME = 'wllutils'                                     # Python 包的名称，即在 pip install 时后面跟的包名
VERSION = '0.0.1'                                             # 包的版本，每次上传到 PyPI 都需要改变这个版本号，否则只会往存储空间增加新内容，无法达到预期
DESCRIPTION = 'utils of wll'                   # 关于该包的剪短描述
if os.path.exists('README.md'):                               # 如果需要，可以加入一段较长的描述，比如读取 README.md，该段长描述会直接显示在 PyPI 的页面上
    with open('README.md', encoding='utf-8') as f:
        LONG_DESCRIPTION = f.read()
else:
    LONG_DESCRIPTION = DESCRIPTION
AUTHOR = 'weiliulei'                                               # 留下大名
AUTHOR_EMAIL = '18500964455@163.com'                              # 留下邮箱
LICENSE = 'MIT'                                               # 定义合适自己的许可证，实在不知道，那就 MIT 吧
PLATFORMS = [                                                 # 支持的平台，如果所有平台都支持，可以填 all
    'linux',
]
REQUIRES = [                                                  # 很多时候，我自己写的包都要依赖第三方，所以可以把依赖包定义在这里，这样的 pip install 自己包的时候，顺便把这些依赖包都装上了
    'pandas',
    'numpy',
    'tqdm',
]
# CONSOLE_SCRIPT = 'my-cmd=my_pkg.my_cmd:main'                  # 如果想在 pip install 之后自动生成一个可执行命令，就靠它了: 
#                                                               # <command>=<package_name>.<python_file_name>:<python_function>
#                                                               # 值得注意的是：
#                                                               # python_file_name 是不能用"-"的，需要用"_"，但 command 可以用"-"
#                                                               # my_cmd.py 也很简单，正常写即可，方法名也不一定是 main

# 需要的信息就在 setup() 中加上，不需要的可以不加
setup(
    name=NAME,
    version=VERSION,
    description=(
        DESCRIPTION
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=find_packages(),
    platforms=PLATFORMS,
    url=URL,
    install_requires=REQUIRES,
    # entry_points={
    #     'console_scripts': [CONSOLE_SCRIPT],
    # }
)