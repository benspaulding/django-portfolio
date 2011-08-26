from distutils.core import setup

setup(name='portfolio',
      version='0.1',
      description='Web designer portfolio app for Django',
      author='Ben Spaulding',
      author_email='ben@benspaulding.com',
      url='https://code.benspaulding.com/svn/apps/portfolio/trunk/portfolio/',
      packages=['portfolio',],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Content Management'],
      )