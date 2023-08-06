from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='fordfulkerson_prueba',
  version='0.0.1',
  description='Implementación del método Fork Fulkerson',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Equipo 2',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='max flow', 
  packages=find_packages(),
  install_requires=['collections'] 
)
