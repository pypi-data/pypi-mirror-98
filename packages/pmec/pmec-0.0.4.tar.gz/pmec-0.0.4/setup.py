from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.7'
]
 
setup(
  name='pmec',
  version='0.0.4',
  description='fetching data from pmec',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://www.pmec.ac.in',  
  author='SOUMYA RANJAN SIA',
  author_email='1801109334_cse@pmec.ac.in',
  license='MIT', 
  classifiers=classifiers,
  keywords=['beautifulsoap','python','pmec','cse'], 
  packages=find_packages(),
  install_requires=[''] 
)