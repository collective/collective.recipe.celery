from setuptools import setup, find_packages
import os

version = '1.0'

tests_require = ['zope.testing', 'z3c.recipe.scripts']

setup(name='collective.recipe.celery',
      version=version,
      description="A buildout recipe to install and configure Celery",
      long_description=open("README.txt").read()
                       + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read()
                       + "\n" +
                       open(os.path.join("collective", "recipe", "celery",
                                         "README.txt")).read(),
      classifiers=[
        'Framework :: Buildout :: Recipe',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='',
      author='Thomas Buchberger',
      author_email='t.buchberger@4teamwork.ch',
      url='https://github.com/collective/collective.recipe.celery',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zc.buildout',
          'zc.recipe.egg',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points = {
        'zc.buildout': ['default = collective.recipe.celery:Recipe']},
      )
