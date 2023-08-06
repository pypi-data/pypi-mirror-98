from setuptools import setup

setup(name='PyQIFParser',
      version='0.1',
      description='A(nother) Python-based Parser for Quicken / Lexware Finance Manager QIF files.',
      url='https://github.com/hhessel/PyQIF-Parser',
      author='Uwe Ziegenhagen / Packaged by Henrik Hessel',
      author_email='hhessel@web.de',
      license='MIT',
      packages=['PyQIFParser'],
      python_requires=">=3.6",
      install_requires=[
       "pandas", "numpy"
      ],
      zip_safe=False)