from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='sagbprojections',
  version='0.0.4',
  description='A module to query SAGB NBA daily fantasy projections',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Rohit Tanikella',
  author_email='rohit.tanikella@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='NBA',
  packages=find_packages(),
  install_requires=['pandas']
 )
