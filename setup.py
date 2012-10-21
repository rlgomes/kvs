"""
setup.py
"""
from setuptools import setup, find_packages

setup (
    name='kvs',
    version='0.0.1',
    author='Rodney Gomes',
    author_email='rodneygomes@gmail.com',
    url='',
    test_suite="tests",
    keywords = ['keyvalue', 'storage'],
    py_modules = [ ],
    scripts = ['kvs/kvsserver.py'],

    license='Apache 2.0 License',
    description='simple key value store',
    long_description=open('README.md').read(),
    packages = find_packages(exclude='tests'),
    install_requires = [ 
                        'twisted',
                       ],

    entry_points = {
        'console_scripts' : [
            'kvs_start = kvsserver:main',
        ],                                                                      
    },                
)
