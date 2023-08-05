from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    ]

long_description = 'Potofox trains Machine Learning models to build and train Deep Neural Networks.'

setup(
      name='Potofox',
      version='0.0.1',
      description='a Deep Learning library',
      long_description=long_description,
      url='https://github.com/spe301/Potosnail',
      author='Spencer Holley',
      author_email ='aacjpw@gmail.com',
      liscence='MIT',
      classifiers=classifiers,
      keywords='',
      packages=find_packages(),
      py_modules=['potofox'],
      install_requires=['pandas>=1.1.3', 'numpy>=1.18.0', 'Potosnail>=0.2.3'])