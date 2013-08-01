import os

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-portfolio',
    version='0.9.2',
    description='Portfolio management for web workers.',
    url='https://github.com/benspaulding/django-portfolio/',
    author='Ben Spaulding',
    author_email='ben@benspaulding.us',
    license='BSD',
    download_url='http://github.com/benspaulding/django-portfolio/tarball/v0.9.2',
    long_description=read('README.rst'),
    packages=['portfolio', 'portfolio.tests'],
    package_data={
        'portfolio': [
            'locale/*/LC_MESSAGES/*',
            'templates/portfolio/*',
        ],
    },
    install_requires=[
        'Django>=1.4.2,<1.6',
        # FIXME: How does one do an or?
        # 'PIL',  # or
        # 'Pillow',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
