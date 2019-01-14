import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='zoho-python',
      version='0.1.5',
      description='API wrapper for Zoho APIs written in Python',
      long_description=read('README.md'),
      url='https://github.com/cortop/zoho-python',
      author='@cortop',
      author_email='cortop@gmail.com',
      license='GPL',
      packages=['zoho'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
