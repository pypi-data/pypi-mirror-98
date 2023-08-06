from setuptools import setup, find_packages
import sys

# 版本信息
version = ''
with open('VERSION', 'r', encoding='utf-8') as file:
    version = file.readline()
# 描述信息
long_description = ""
with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()
# setup
setup(
    name="roi-device",
    version=version,
    description="roi iot device , support all iot cloud platform in future",
    author="labelnet",
    author_email="labelnet@smartahc.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/roi-device/",
    keywords=['roi'],
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'aliyun-iot-linkkit==1.2.2',
        'pycryptodome==3.7.2'
    ],
    python_requires='>=3.5'
)
