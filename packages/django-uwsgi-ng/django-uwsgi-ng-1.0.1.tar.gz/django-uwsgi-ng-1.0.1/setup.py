import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from django_uwsgi import __version__


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='django-uwsgi-ng',
    version=__version__,
    description='uWSGI stuff for Django projects',
    long_description=open('README.rst').read(),
    url='https://edugit.org/AlekSIS/libs/django-uwsgi-ng',
    author='Eugene MechanisM',
    author_email='eugene@mechanism.pro',
    maintainer='Dominik George',
    maintainer_email='dominik.george@teckids.org',
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        'Topic :: Communications :: Email',
        'Framework :: Django',
    ],
    keywords='uwsgi, django, mail, cache, template',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    extras_require={
        'uwsgi': ['uwsgi'],
    },
)
