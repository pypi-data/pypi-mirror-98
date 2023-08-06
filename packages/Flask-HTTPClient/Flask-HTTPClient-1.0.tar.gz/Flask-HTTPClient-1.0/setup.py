"""
Flask-HTTPClient
-------------

This is the description for that library
"""
from setuptools import setup

with open('README.md','r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-HTTPClient',
    version='1.0',
    url='https://github.com/haojunyu/flask-httpclient',
    license='MIT',
    author='haojunyu',
    author_email='haojunyu2012@gmail.com',
    description='HTTP Client extension for Flask',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['flask_httpclient'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'requests',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
