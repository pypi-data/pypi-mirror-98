from setuptools import setup

setup(
    name='mysql_tools',
    version='0.0.1',
    description='mysql_tools',
    author='xmzhang',
    author_email='25337942@qq.com',
    url='https://github.com/Shimon-Cheung',
    py_modules=['mysql_tools'],
    install_requires=['pymysql==0.9.3', 'DBUtils==1.3', 'loguru==0.5.3']
)