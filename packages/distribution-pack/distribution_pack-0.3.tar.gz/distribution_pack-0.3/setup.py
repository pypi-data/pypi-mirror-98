from setuptools import setup


def readme():
    with open('README.rst') as f:
        return '\n{}'.format(f.read())


def description():
    desc = "Gaussian and Binomial distributions"
    return desc

setup(name='distribution_pack',
      version='0.3',
      description=description(),
      packages=['distribution_pack'],
      author='Igor Santos',
      author_email='ssantos.igor@hotmail.com',
      zip_safe=False,
      install_requires=[
            'seaborn==0.11.0',
            'plotly==4.14.1',
            'pandas==1.1.3',
            'numpy==1.19.2',
            'matplotlib==3.3.2'
      ],
      include_package_data=True,
      long_description=readme()
      )
