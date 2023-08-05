import os
from setuptools import setup, find_packages
from django_angular_url import __version__

DESCRIPTION = 'Manage Django URLs for AngularJS'

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
]


def read(fname):
    readme_file = os.path.join(os.path.dirname(__file__), fname)
    return os.popen('[ -x "$(which pandoc 2>/dev/null)" ] && pandoc -t rst {0} || cat {0}'.format(readme_file)).read()


setup(
    name='django-angular-url',
    version=__version__,
    author='Rafael Torres',
    author_email='',
    description=DESCRIPTION,
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url='https://github.com/rafitorres/django-angular-url',
    license='MIT',
    keywords=['django', 'angularjs'],
    install_requires=[
        'django>=1.11',
    ],
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=[]),
    include_package_data=True,
)
