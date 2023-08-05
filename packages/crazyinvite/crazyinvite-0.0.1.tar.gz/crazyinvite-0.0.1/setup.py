from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='crazyinvite',
  version='0.0.1',
  description='A very crazy invite app',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Wissam crazy',
  author_email='geathwissam@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords = [
        'aminoapps',
        'amino-py',
        'amino',
        'amino-bot',
        'narvii',
        'api',
        'python',
        'python3',
        'python3.x',
        'Crazy',
        'official'
    ],
  packages=find_packages(),
  install_requires=[''] 
)