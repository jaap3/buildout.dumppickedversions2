import os
from setuptools import setup

version = '1.1'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = '\n'.join((
    read('README.rst'),
    'Detailed Documentation',
    '======================',
    read('buildout', 'dumppickedversions2', 'dumppickedversions2.rst'),
    read('CHANGES.rst'),
    read('CONTRIBUTORS.rst'),
))


setup(name='buildout.dumppickedversions2',
      version=version,
      description='Dump buildout 2 picked versions.',
      long_description=long_description,
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
      ],
      license='MIT',
      keywords='buildout extension dump picked versions',
      author='Jaap Roes',
      author_email='jaap@eight.nl',
      url='https://github.com/eightmedia/buildout.dumppickedversions2',
      packages=['buildout', 'buildout.dumppickedversions2',],
      namespace_packages=['buildout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['zc.buildout>=2.0.1'],
      extras_require={'test': ['zope.testing']},
      entry_points={
          'zc.buildout.extension': [
              'default = buildout.dumppickedversions2:install'
          ],
          'zc.buildout.unloadextension': [
              'default = buildout.dumppickedversions2:uninstall'
          ]
      },
)
