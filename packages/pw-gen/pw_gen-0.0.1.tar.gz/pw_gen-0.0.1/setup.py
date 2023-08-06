from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='pw_gen',
  version='0.0.1',
  description='A library for generating secure passwords',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/lunAr-creator/password_generator',
  author='Soma Benfell',
  author_email='lunArcreator3@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='password',
  packages=find_packages(),
  install_requires=['']
)
