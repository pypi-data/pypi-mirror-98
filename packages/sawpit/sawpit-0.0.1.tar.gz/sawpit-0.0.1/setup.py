from setuptools import setup, find_packages


LONG_DESCRIPTION = open('README.md').read()

setup(name='sawpit',
      version='0.0.1',
      description='Work in progress fork of pywsitest',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      url='https://github.com/jamsidedown/sawpit',
      author='Rob Anderson',
      author_email='opensource@robanderson.dev',
      license='MIT',
      classifiers=[
          'Intended Audience :: Developers',
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Natural Language :: English'
      ],
      keywords='websocket integration test testing',
      packages=find_packages(exclude=('tests',)),
      install_requires=[
          'websockets',
          'requests'
      ],
      zip_safe=False,
      python_requires='>=3.7')
