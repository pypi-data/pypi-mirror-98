from setuptools import setup, Extension

setup(name='python-pytun',
      author='montag451',
      author_email='montag451@laposte.net',
      maintainer='montag451',
      maintainer_email='montag451@laposte.net',
      url='https://github.com/montag451/pytun',
      description='Linux TUN/TAP wrapper for Python',
      long_description=open('README.rst').read(),
      version='2.4.1',
      ext_modules=[Extension('pytun', ['pytun.c'])],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: C',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Networking'])
