from __future__ import (absolute_import, division, print_function)
import versioneer

try:
    from setuptools import setup
except ImportError:
    try:
        from setuptools.core import setup
    except ImportError:
        from distutils.core import setup


setup(name='pypvserver',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author='klauer',
      author_email=None,
      license="BSD (3-clause)",
      url="https://github.com/klauer/pypvserver",
      packages=['pypvserver'],
      # package_data={'pypvserver': ['files/*']},
      install_requires=['numpy', 'pcaspy>=0.6.0'],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
      ],
      )
