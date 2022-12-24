from setuptools import setup, find_packages

setup(name='dataProcessing',
      version='0.1',
      url='https://github.com/ajcltm/dataProcessing',
      license='jnu',
      author='ajcltm',
      author_email='ajcltm@gmail.com',
      description='',
      packages=find_packages(exclude=['test']),
      zip_safe=False,
      setup_requires=['requests>=1.0'],
      test_suite='test.test_dataProcessing')