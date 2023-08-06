# coding=utf8
# 	python setup.py sdist bdist_wheel
#   twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

from setuptools import setup, find_packages

setup(
    name="aiotcloud",
    version="2.0.0",
    description='''Ver2.0.0 添加AiCam相机支持''',
    author='sangxin',
    include_package_data = True,
    author_email='2876424407@qq.com',
    url="https://github.com/aiotcloud-tech/python-aiot-sdk",
    maintainer='sangxin',
    maintainer_email='2876424407@qq.com',
    packages=['aiotcloud'],
    package_data={'aiotcloud': ['fonts/*', 'rshell/*']},
    install_requires=[
        'paho-mqtt',
        'pyreadline',
        'pyudev >= 0.16',
        'pyserial',
        'six',
        'playsound',
        'baidu-aip',
        'opencv-python',
        'opencv-contrib-python'
    ]
)
