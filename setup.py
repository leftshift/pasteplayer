from setuptools import setup

with open("README.md", "r") as f:
    long_descr = f.read()

setup(name='pasteplayer',
      version='1.0',
      description='A thin mpv wrapper for on-the-fly playlist editing',
      long_description=long_descr,
      author='uberardy',
      author_email='github@ardy.io',
      license='GPLv3',
      url='https://github.com/leftshift/pasteplayer',
      py_modules=['pasteplayer'],
      install_requires=['python-mpv'],
      entry_points={
          'console_scripts': ['pasteplayer = pasteplayer:main']
      }
)
