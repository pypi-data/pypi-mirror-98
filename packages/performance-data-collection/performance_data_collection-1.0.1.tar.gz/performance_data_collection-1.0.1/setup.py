from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='performance_data_collection',  # 包名
      version='1.0.1',  # 版本号
      description='Collect performance data for PC applications',
      long_description=long_description,
      author=['chengxaiokai', 'zhoujunjie'],
      author_email='747469442@qq.com',
      url='https://gitee.com/chen-xiaokai/windows-performance-collection.git',
      install_requires=['pyecharts', 'psutil', 'pandas', 'pyecharts', 'xlrd', 'xlwt', 'openpyxl'],
      license='Windows MacOS',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
