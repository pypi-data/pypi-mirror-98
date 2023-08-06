import os
from setuptools import setup


os.chdir(os.path.abspath(os.path.dirname(__file__)))


req = [
    'd3m',
]
setup(name='datamart',
      version='2021.3.17',
      py_modules=['datamart'],
      install_requires=req,
      description="Datamart API",
      author="DARPA Datamart Program",
      maintainer="Remi Rampin",
      maintainer_email='remi.rampin@nyu.edu',
      url='https://gitlab.com/ViDA-NYU/datamart/datamart',
      project_urls={
          'Homepage': 'https://gitlab.com/datadrivendiscovery/datamart-api',
          'Source': 'https://gitlab.com/datadrivendiscovery/datamart-api',
          'Tracker': 'https://gitlab.com/datadrivendiscovery/datamart-api/issues',
      },
      long_description="Datamart API",
      license='Apache-2.0',
      keywords=['datamart', 'd3m'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Information Analysis'])
