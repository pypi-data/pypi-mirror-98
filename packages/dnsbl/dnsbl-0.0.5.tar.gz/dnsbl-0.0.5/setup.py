from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='dnsbl',
  version='0.0.5',
  description='Module that checks the given ips blacklisting status',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Aswin venkat',
  author_email='aswin.venkat@cybersecurityworks.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='dnsbl', 
  packages=find_packages(),
  install_requires=['futures','dnspython'] 
)