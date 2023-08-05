'''Setup'''

from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='handmadeML',
      version="1.0",
      author='Thomas Mathieu',
      author_email='thomas.mathieu@m4x.org',
      description="'Personal machine/deep learning implementation inspired by sklearn and keras'",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/bdepebhe/handmadeML',
      packages=find_packages(),
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
      python_requires='>=3.6',
      install_requires=requirements,
      test_suite='tests',
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      scripts=['scripts/handmadeML-run'],
      zip_safe=False)
