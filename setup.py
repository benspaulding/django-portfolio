import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-portfolio',
    version='0.8.1',
    description='Portfolio management for web workers.',
    url='https://github.com/benspaulding/django-portfolio/',
    author='Ben Spaulding',
    author_email='ben@benspaulding.us',
    license='BSD',
    download_url='http://github.com/benspaulding/django-portfolio/tarball/v0.8.1',
    long_description=read('README.rst'),
    packages=['portfolio', 'portfolio.tests'],
    package_data={
        'portfolio': [
            'locale/*/LC_MESSAGES/*',
            'templates/portfolio/*',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
