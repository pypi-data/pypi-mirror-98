from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='RevolutionSelling',
  version='0.1',
  description='a pyrogram bot cloner',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Invisible Medusa',
  author_email='invisiblemedusa10@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Clone', 
  packages=find_packages(),
  install_requires=[''] 
)
