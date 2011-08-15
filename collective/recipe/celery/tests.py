import sys
import tempfile
import shutil
from doctest import ELLIPSIS, NORMALIZE_WHITESPACE, REPORT_UDIFF
from doctest import DocFileSuite

from zc.buildout.testing import buildoutTearDown
from zc.buildout.testing import install_develop
from zc.buildout.testing import normalize_path
from zc.buildout.testing import bdist_egg
from zc.buildout.tests import easy_install_SetUp
from zope.testing import renormalizing


def setUp(test):
    easy_install_SetUp(test)
    create_celery_egg(test)
    install_develop('collective.recipe.celery', test)


def create_celery_egg(test):
    """Create a dummy celery egg for testing.
       The included scripts simply print the content of the celeryconfig
       module.
    """
    from zc.buildout.testing import write
    dest = test.globs['sample_eggs']
    tmp = tempfile.mkdtemp()
    try:
        write(tmp, 'README.txt', '')
        write(tmp, 'celery.py',
              'import celeryconfig\n'
              'def main():\n'
              ' print "\\n".join(["%s=%s" % (opt, repr(getattr(celeryconfig, '
              'opt))) for opt in dir(celeryconfig) if opt[0].isalpha()])\n')
        write(tmp, 'setup.py',
              "from setuptools import setup\n"
              "setup(name='celery', py_modules=['celery'],"
              " entry_points={'console_scripts': ['celeryd = celery:main', "
                                                 "'celeryctl = celery:main']},"
              " zip_safe=True, version='2.3.1')\n")
        bdist_egg(tmp, sys.executable, dest)

    finally:
        shutil.rmtree(tmp)

def test_suite():
    return DocFileSuite(
           'README.txt',
           setUp=setUp, tearDown=buildoutTearDown,
           optionflags=ELLIPSIS | NORMALIZE_WHITESPACE | REPORT_UDIFF,
           checker=renormalizing.RENormalizing([normalize_path]),)