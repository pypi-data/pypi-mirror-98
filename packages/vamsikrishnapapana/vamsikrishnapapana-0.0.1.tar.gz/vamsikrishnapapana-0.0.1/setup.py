from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='vamsikrishnapapana',
  version='0.0.1',
  description='A simple library that contains my details',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Vamsi Krishna Papana',
  author_email='vamsikrishnapapana@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='vamsi', 
  packages=find_packages(),
  install_requires=[''] 
)
