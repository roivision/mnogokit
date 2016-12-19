import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'VERSION')) as f:
    VERSION = f.read()

setup(name='mnogokit',
      version=VERSION,
      description='MongoDB maintenance scripts',
      long_description=README,
      author='',
      author_email='',
      url='',
      keywords='Mongo backup restore tools',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite="tests",
      entry_points="""\
      [console_scripts]
        mnogokit = mnogokit.cli:run
      """,
      )
