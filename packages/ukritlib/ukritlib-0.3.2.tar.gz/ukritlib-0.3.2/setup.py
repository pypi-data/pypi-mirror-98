from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='ukritlib',
      version='0.3.2',

      long_description=readme(),
      long_description_content_type="text/markdown",

      description='The funniest joke in the world',
      url='http://github.com/ukritfongsomboon/ukritlib',
      author='ukrit Fongsomboon',
      author_email='ukrit.fb@gmail.com',
      license='MIT',
      packages=['ukritlib'],
      zip_safe=False)
